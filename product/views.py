from constants import FAILURE_PAYMENT_TEMPLATE, RETURN_PRODUCT_TEMPLATE, UPDATE_ORDER_STATUS_TEMPLATE, \
    ORDER_STATUS_FIELDS, VIEW_ORDER_VENDOR_TEMPLATE, INVOICE_TEMPLATE, ADMIN_FUNCTIONALITY_TEMPLATE, \
    DETAILS_ORDER_TEMPLATE, VIEW_PURCHASES_TEMPLATE, SUCCESS_PAYMENT_TEMPLATE, ADDRESS_QUANTITY_PAGE_TEMPLATE, \
    ADDRESS_PAGE_TEMPLATE, VIEW_CHECKOUT_TEMPLATE, UPDATE_PRODUCT_TEMPLATE, ADD_PRODUCT_TEMPLATE, \
    UPDATE_BRAND_NAME_TEMPLATE, ADD_CATEGORY_TEMPLATE, FILTER_RESULT_TEMPLATE, FAVOURITES_TEMPLATE, WISHLIST_TEMPLATE, \
    ADD_TO_CART_TEMPLATE, HOME_TEMPLATE, SEARCH_TEMPLATE
from .models import Product, Cart, WishList, Brand, Favourites, Review, Category, Order, Invoice, SearchedNotify
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from store.models import Customer
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseNotFound
from django.db.models import Count
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from product.custom_mixins import UserIsCustomerMixin, UserIsSellerMixin
import logging

logger = logging.getLogger('django')
custom_logger = logging.getLogger('custom_logger')
warn_and_above_logger = logging.getLogger('warn_and_above_logger')


class FailureView(LoginRequiredMixin, UserIsCustomerMixin, TemplateView):
    """Redirects to Payment Failure page"""
    template_name = FAILURE_PAYMENT_TEMPLATE


class ReturnStatus(LoginRequiredMixin, UserIsCustomerMixin, View):
    """To view the return status of the order"""

    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        invoice.reason = request.POST.get('return')
        invoice.want_return = True
        invoice.save()
        return redirect('orders')


class ReturnProductView(LoginRequiredMixin, UserIsCustomerMixin, TemplateView):
    """To return the product"""
    template_name = RETURN_PRODUCT_TEMPLATE


class UpdateOrderStatus(LoginRequiredMixin, UserIsSellerMixin, UpdateView):
    """For updating the status of the products"""
    model = Invoice
    # invoice = Invoice.objects.get()
    # print(invoice.status)
    # if Invoice.status == 'Delivered':
    fields = ['status']
    template_name = UPDATE_ORDER_STATUS_TEMPLATE
    success_url = reverse_lazy('view-order')

    def get(self, request, *args, **kwargs):
        current_object = self.get_object()
        if current_object.status == "Delivered" and current_object.want_return:
            self.fields = ORDER_STATUS_FIELDS
        return super(UpdateOrderStatus, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        current_object = self.get_object()
        if current_object.status == "Delivered" and current_object.want_return:
            self.fields = ORDER_STATUS_FIELDS
        return super(UpdateOrderStatus, self).post(request, *args, **kwargs)


class ViewOrdersVendor(LoginRequiredMixin, UserIsSellerMixin, View):
    """For viewing the orders of the brand of the vendor"""

    def get(self, request):
        brand_user = Brand.objects.get(user=request.user)
        # print(brand_user)
        invoice = Invoice.objects.filter(product__brand=brand_user)
        return render(request, VIEW_ORDER_VENDOR_TEMPLATE, {'invoice': invoice})


# cant test for this
class DownloadInvoice(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For downloading invoice"""

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        invoice = Invoice.objects.filter(order=order)
        context = {

            'all_orders': Invoice.objects.filter(order=pk), 'order': order, 'order_ids': order.id}
        pdf = RenderToPdf(INVOICE_TEMPLATE, context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % context['order_ids']

            content = "file; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


# cant test for this
def RenderToPdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class ProductView(LoginRequiredMixin, UserIsSellerMixin, View):
    """View the products to seller"""

    def get(self, request):
        return render(request, ADMIN_FUNCTIONALITY_TEMPLATE,
                      {'products': Product.objects.filter(brand=self.request.user.brand)})


class DetailPurchasedView(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For viewing the details of the purchased products"""

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        all_orders = Invoice.objects.filter(order=pk)
        return render(request, DETAILS_ORDER_TEMPLATE, {'all_orders': all_orders, 'order': order})


class PurchasedView(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For viewing the order details"""

    def get(self, request):
        return render(request, VIEW_PURCHASES_TEMPLATE, {'items': Order.get_orders_by_user(request.user)})


# cant write test for this
class PaymentSuccessView(LoginRequiredMixin, UserIsCustomerMixin, View):
    """After payment is successful"""
    template_name = SUCCESS_PAYMENT_TEMPLATE

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        prod_pk = int(request.GET.get('product'))
        product = Product.objects.get(pk=prod_pk)
        address = request.GET.get('address')
        quantity = int(request.GET.get('quantity'))

        order = get_object_or_404(Order, stripe_payment_intent=session.payment_intent)
        order.total_amount = float(product.calculate_discount) * int(quantity)
        order.address = address
        order.has_paid = True
        order.save()

        invoice = Invoice()
        invoice.order = order
        invoice.product = product
        invoice.quantity = quantity
        invoice.save()

        product.available_quantity -= quantity
        product.no_of_purchases += quantity
        product.save()

        return render(request, self.template_name)


class CreateCheckoutSession(LoginRequiredMixin, UserIsCustomerMixin, View):
    """ This view serves as an API to initialize the payment gateway."""

    @method_decorator(csrf_exempt)
    def post(self, request, pk):
        customer = Customer.objects.get(user=self.request.user)
        product = Product.objects.get(pk=pk)

        detail = request.body.decode('utf-8')
        body = json.loads(detail)

        available_items = Product.objects.get(pk=pk).available_quantity
        number_purchased = Product.objects.get(pk=pk).no_of_purchases
        address = body['address-buy']
        quantity = body['quantityy']
        '''for checking the quantity'''
        if available_items >= float(quantity):
            items_left = available_items - float(quantity)
            number_purchased += float(quantity)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(payment_method_types=['card'], line_items=[{
                'price_data': {'currency': 'inr', 'unit_amount': int(float(product.calculate_discount) * 100),
                               'product_data': {'name': product.name}, }, 'quantity': quantity}], mode='payment',
                                                     success_url=request.build_absolute_uri(reverse(
                                                         'success')) + "?session_id={CHECKOUT_SESSION_ID}&address=" + address + "&quantity=" + str(
                                                         quantity) + "&product=" + str(pk),
                                                     cancel_url=request.build_absolute_uri(reverse('failure')),

                                                     )

            Order.objects.create(customer=customer, stripe_payment_intent=session['payment_intent'], total_amount=0)
            return JsonResponse({'sessionId': session.id})
        else:
            messages.error(request, f"{product.name} not available in that quantity")
            return JsonResponse({'message': False})


class OrderDetailsView(LoginRequiredMixin, UserIsCustomerMixin, View):
    """To get the order details"""

    def get(self, request, pk):
        return render(request, ADDRESS_QUANTITY_PAGE_TEMPLATE,
                      {'pk': pk, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


# cant test for this
class PaymentSuccessViewCart(LoginRequiredMixin, UserIsCustomerMixin, View):
    """Redirect to success_payment.html page"""
    template_name = SUCCESS_PAYMENT_TEMPLATE

    '''To get the session id '''

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        '''retreives session id'''
        session = stripe.checkout.Session.retrieve(session_id)

        customer = Customer.objects.get(user=request.user)
        total_amount = 0
        order = get_object_or_404(Order, stripe_payment_intent=session.payment_intent)

        invoices = []
        cart_products = Cart.objects.filter(customer=customer)

        for i in cart_products:
            product = i
            i.product.available_quantity -= i.quantity
            i.product.save()
            total_amount += int(float(product.product.calculate_discount) * product.quantity)
            invoices.append(Invoice(product=product.product, quantity=product.quantity))

        order.has_paid = True
        order.address = request.GET.get('address')
        order.total_amount = total_amount
        order.save()
        Cart.objects.filter(customer=customer).delete()

        for i in invoices:
            i.order = order
            i.save()

        return render(request, self.template_name)


class CreateCheckoutSessionCart(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For creating checkout session while buying items from cart"""

    @method_decorator(csrf_exempt)
    def post(self, request):

        customer = Customer.objects.get(user=self.request.user)
        cart_products = Cart.objects.filter(customer=customer)

        '''json.loads() will only accept a unicode string, so you must decode request.body before json.loads()'''
        detail = request.body.decode('utf-8')
        '''get all data from json'''
        body = json.loads(detail)
        '''get address from the body'''
        address = body['address-buy']

        '''for checking the quantity'''
        for i in cart_products:
            if i.product.available_quantity >= i.quantity:

                pass
            else:
                messages.error(request, f"{i.product.name} not available in that quantity")
                return JsonResponse({'message': False})
        else:

            '''For viewing items on the checkout page with this format'''
            lis = []
            for cart_product in cart_products:
                lis.append({'price_data': {'currency': 'inr',
                                           'unit_amount': int(float(cart_product.product.calculate_discount) * 100),
                                           'product_data': {'name': cart_product.product.name}, },
                            'quantity': cart_product.quantity})

            stripe.api_key = settings.STRIPE_SECRET_KEY

            '''creating a checkout session with payment_method = card'''
            session = stripe.checkout.Session.create(payment_method_types=['card'], line_items=lis, mode='payment',
                                                     # not getting after suceess-cart
                                                     success_url=request.build_absolute_uri(reverse(
                                                         'success-cart')) + "?session_id={CHECKOUT_SESSION_ID}&address=" + address,
                                                     cancel_url=request.build_absolute_uri(reverse('failure')), )

            Order.objects.create(customer=customer, total_amount=0, stripe_payment_intent=session['payment_intent'])
            # print(session.id)
            return JsonResponse({'sessionId': session.id})


class OnlyAddress(LoginRequiredMixin, UserIsCustomerMixin, View):
    """To get the address"""

    def get(self, request):
        return render(request, ADDRESS_PAGE_TEMPLATE, {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})


class ViewCheckout(LoginRequiredMixin, UserIsCustomerMixin, TemplateView):
    """Redirects to view_checkout.html page"""
    template_name = VIEW_CHECKOUT_TEMPLATE


class UpdateProductView(LoginRequiredMixin, UserIsSellerMixin, UpdateView):
    """For updating the product"""
    model = Product
    fields = ['name', 'price', 'image', 'description', 'available_quantity', 'discount', 'category', 'volume',
              'volume_unit']
    template_name = UPDATE_PRODUCT_TEMPLATE
    success_url = reverse_lazy('grocery_store_home')


class AddProductView(LoginRequiredMixin, UserIsSellerMixin, CreateView):
    """For adding the product"""
    model = Product
    fields = ['name', 'price', 'image', 'description', 'available_quantity', 'discount', 'category', 'volume',
              'volume_unit']
    template_name = ADD_PRODUCT_TEMPLATE
    success_url = reverse_lazy('grocery_store_home')

    def form_valid(self, form):
        """for setting the brand of product"""
        form.instance.brand = Brand.objects.get(user=self.request.user)
        form.instance.no_of_purchases = 0
        return super(AddProductView, self).form_valid(form)


class UpdateBrandName(LoginRequiredMixin, UserIsSellerMixin, UpdateView):
    """For updating the brand name"""
    model = Brand
    fields = ['brand']
    template_name = UPDATE_BRAND_NAME_TEMPLATE
    success_url = reverse_lazy('grocery_store_home')


# todo
class AddCategory(LoginRequiredMixin, UserIsSellerMixin, CreateView):
    """For adding the category"""
    model = Category
    fields = ['name']
    template_name = ADD_CATEGORY_TEMPLATE
    category = Category.objects.all()
    success_url = reverse_lazy('add-category')
    extra_context = {'category': category}


class FilterProduct(View):
    """For filtering the product based on min and max price"""

    def get(self, request):
        min_val = request.GET.get('min_val') if request.GET.get('min_val') != '' else \
            Product.objects.order_by('price').values_list('price', flat=True)[0]

        max_val = request.GET.get('max_val') if request.GET.get('max_val') != '' else \
            Product.objects.order_by('-price').values_list('price', flat=True)[0]
        products = Product.objects.filter(price__gte=float(min_val), price__lte=float(max_val))
        return render(request, FILTER_RESULT_TEMPLATE, {'products': products})


class CategoryView(ListView):
    """For viewing products of the specified category"""

    def get(self, request, category):
        products = Product.objects.filter(category=Category.objects.get(name=category))
        return render(request, FILTER_RESULT_TEMPLATE, {'products': products, 'category': Category.objects.all()})


class AddReviewView(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For adding the review to the product"""

    def post(self, request, pk):
        customer = Customer.objects.get(user=request.user)
        review = self.request.POST.get('add_review')
        product = Product.objects.get(pk=pk)
        Review.objects.create(customer=customer, review=review, product=product)
        messages.success(request, "Review added successfully")
        return redirect('product-detail', pk=pk)


class AddToFavourites(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For adding brand to the Favourites"""

    def get(self, request, pk):
        brand = Brand.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        try:
            """Check if brand already in favourites"""
            Favourites.objects.get(customer=customer, brand=brand)
            messages.error(request, 'Brand Already exist in Favourites')
            custom_logger.warning(f'Brand {brand} already in {customer} favourites')
            return redirect('favourites')
        except ObjectDoesNotExist:
            """Add brand to favourites"""
            Favourites.objects.create(customer=customer, brand=brand)
            messages.success(request, "Brand added to Favourites.")
            custom_logger.info(f"Brand {brand} added successfully to {customer} favourites")
            return redirect('favourites')


class FavouriteView(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For viewing all the products of the favourite brand"""

    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        fav = Favourites.objects.filter(customer=customer.id)

        all_brands = Brand.objects.all()

        if len(fav) >= 1:
            products = Product.objects.filter(brand=fav[0].brand)
            for item in fav[1:]:
                products |= Product.objects.filter(brand=item.brand)

            return render(request, FAVOURITES_TEMPLATE, {'products': products, 'all_brands': all_brands, 'fav': fav})
        else:
            messages.error(request, "You have no favourites")
            custom_logger.error(f"{customer} has no favourites")
            return render(request, FAVOURITES_TEMPLATE, {'all_brands': all_brands, })


class RemoveFromFavourites(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For removing brand from the favourites"""

    def get(self, request, pk):
        brand = Brand.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        Favourites.objects.filter(customer=customer, brand=brand).delete()
        messages.success(request, "Brand removed from Favourites.")
        custom_logger.critical(f"{customer} removed {brand} from favourites")
        return redirect('favourites')


class AddToWishList(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For adding item to WishList"""

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        try:
            """If item already exist in wishlist"""
            WishList.objects.get(customer=customer, product=product)
            messages.warning(request, 'Item Already exist')
            warn_and_above_logger.warning(f'{product} already exists in {customer} wishlist')
            return redirect('wishlist')
        except ObjectDoesNotExist:
            """Add item to wishlist if not already exists"""
            WishList.objects.create(customer=customer, product=product)
            messages.success(request, "Item added to WishList.")
            warn_and_above_logger.info(f"{product} added succesfully to {customer} wishlist")
            return redirect('wishlist')


class WishListView(LoginRequiredMixin, UserIsCustomerMixin, ListView):
    """For viewing products that are present in the wishlist"""
    template_name = WISHLIST_TEMPLATE
    context_object_name = 'products'

    def get_queryset(self):
        """Get products based on Customer"""
        products = WishList.objects.filter(customer=Customer.objects.get(user=self.request.user))
        warn_and_above_logger.debug('view favourites')
        return products


class RemoveFromWishList(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For removing product from the Wishlist"""

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        WishList.objects.filter(customer=customer, product=product).delete()
        messages.success(request, "Item removed from WishList.")
        warn_and_above_logger.critical(f'{product} removed from {customer} wishlist')
        return redirect('wishlist')


class AddToCart(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For adding a product to the cart """

    def get(self, request, pk):

        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)

        quantity = 1
        try:
            """Check if item already exists or not"""
            Cart.objects.get(customer=customer, product=product)

            messages.error(request, 'Item Already exist in cart')
            return redirect('cart')
        except ObjectDoesNotExist:
            """Add item to cart if not already exists"""

            Cart.objects.create(customer=customer, product=product, quantity=quantity)
            messages.success(request, "Item added to Cart.")
            return redirect('cart')


class CartView(LoginRequiredMixin, UserIsCustomerMixin, ListView):
    """For viewing items in the cart"""
    template_name = ADD_TO_CART_TEMPLATE
    context_object_name = 'products'

    def get_queryset(self):
        """Get products based on Customer"""
        products = Cart.objects.filter(customer=Customer.objects.get(user=self.request.user))
        return products


class UpdateCart(LoginRequiredMixin, UserIsCustomerMixin, View):
    """For updating the Cart"""

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(customer=customer, product=product)
        cart.quantity = self.request.POST.get('quantity')
        cart.save()
        return redirect('cart')


class RemoveFromCart(LoginRequiredMixin, UserIsCustomerMixin, View):
    """ For removing product from the Cart """

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        customer = Customer.objects.get(user=request.user)
        """ get the customer, product and remove that product fom cart """
        Cart.objects.filter(customer=customer, product=product).delete()
        messages.success(request, "Item removed from Cart.")
        return redirect('cart')


class HomeView(View):
    """View the home page"""

    def get(self, request):

        if request.user.is_staff and not request.user.is_superuser:
            """Seller Panel"""
            products = Product.objects.filter(brand=self.request.user.brand)

            return render(request, ADMIN_FUNCTIONALITY_TEMPLATE, {'products': products})

        elif request.user.is_superuser:
            """Super Admin Panel"""
            return redirect('admin:index')
        else:
            """Customer Panel"""
            products = Product.objects.all()
            category = Category.objects.all()

            """View trending"""
            trending = Product.objects.order_by('-no_of_purchases').distinct()[0:5]
            all_products = trending

            review_id = Review.objects.values_list('product').annotate(product_count=Count('product')).order_by(
                '-product_count')[0:5]
            # <QuerySet [(20, 3), (21, 1), (23, 1), (22, 1)]>
            for i in review_id:
                all_products |= Product.objects.filter(pk=i[0])

            wishlist_id = WishList.objects.values_list('product').annotate(product_count=Count('product')).order_by(
                '-product_count')[0:5]
            for i in wishlist_id:
                all_products |= Product.objects.filter(pk=i[0])
            return render(request, HOME_TEMPLATE,
                          {'products': products, 'category': category, 'all_products': all_products})


class SearchProduct(View):
    """For searching a product based on name, description, brand, category"""

    def post(self, request):
        searched = request.POST['searched']
        products_name = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched) | Q(brand__brand__icontains=searched) | Q(
                category__name__icontains=searched)).distinct()

        if request.user.is_authenticated:
            product_searched_not_available = products_name.filter(available_quantity=0)
            for product in product_searched_not_available:
                SearchedNotify.objects.get_or_create(customer_name=request.user.customer, product_name=product)
        custom_logger.error(f'Searching for {searched}')

        return render(request, SEARCH_TEMPLATE, {'searched': searched, 'products_name': products_name, })


class DetailProductView(DetailView):
    """Showing the details of each product"""
    model = Product

# class AddAddressOnlyView(View):
#     def post(self, request):
#         customer = Customer.objects.get(user=self.request.user)
#         cart_products = Cart.objects.filter(customer=customer)
#         address = self.request.POST.get('address-buy')
#         total_amount = 0
#         invoices = []
#
#         '''for checking the quantity'''
#         for i in cart_products:
#             if i.product.available_quantity >= i.quantity:
#                 product = i
#                 i.product.available_quantity -= i.quantity
#                 i.product.save()
#                 total_amount += float(product.product.calculate_discount) * product.quantity
#                 invoices.append(Invoice(product=product.product, quantity=product.quantity))
#             else:
#                 break
#         else:
#             order = Order.objects.create(customer=customer, address=address, total_amount=0)
#             for i in invoices:
#                 i.order = order
#                 i.save()
#             Order.objects.filter(customer=customer, address=address, total_amount=0).update(total_amount=total_amount)
#             Cart.objects.filter(customer=customer).delete()
#             messages.success(request, "Order successful")
#             return redirect('orders')
#         return redirect('grocery_store_home')
#
#
# '''For getting the address, quantity for the single item order'''
#
#
# class AddAddressView(View):
#     def post(self, request, pk):
#         customer = Customer.objects.get(user=self.request.user)
#         product = Product.objects.get(pk=pk)
#         address = self.request.POST.get('address-buy')
#         quantity = self.request.POST.get('quantityy')
#         available_items = Product.objects.get(pk=pk).available_quantity
#
#         '''for checking the quantity'''
#         if available_items >= float(quantity):
#             items_left = available_items - float(quantity)
#             order = Order.objects.create(customer=customer, address=address,
#                                          total_amount=Product.objects.get(pk=pk).calculate_discount)
#             Invoice.objects.create(order=order, product=product, quantity=quantity)
#             number_purchased = Product.objects.get(pk=pk).no_of_purchases
#             number_purchased += float(quantity)
#             Product.objects.filter(pk=pk).update(no_of_purchases=number_purchased)
#             Product.objects.filter(pk=pk).update(available_quantity=items_left)
#             messages.success(request, "Order successful")
#             return redirect('orders')
#         else:
#             messages.success(request, "Item not available in that quantity")
#             return redirect('grocery_store_home')
