from django.urls import path
from .views import DetailProductView, SearchProduct, CartView, AddToCart, WishListView, AddToWishList, \
    RemoveFromWishList, RemoveFromCart, UpdateCart, AddToFavourites, FavouriteView, RemoveFromFavourites, \
    AddReviewView, CategoryView, FilterProduct, OrderDetailsView, PurchasedView, OnlyAddress, \
    AddCategory, UpdateBrandName, AddProductView, ProductView, UpdateProductView, \
    DetailPurchasedView, DownloadInvoice, ViewOrdersVendor, UpdateOrderStatus, \
    ViewCheckout, FailureView, CreateCheckoutSession, PaymentSuccessView, CreateCheckoutSessionCart, \
    PaymentSuccessViewCart, ReturnProductView, ReturnStatus



urlpatterns = [
    path('search/', SearchProduct.as_view(), name='product-search'),
    path('<int:pk>/', DetailProductView.as_view(), name='product-detail'),

    path('<int:pk>/add_to_cart/', AddToCart.as_view(), name="add-to-cart"),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', UpdateCart.as_view(), name="update-cart"),
    path('<int:pk>/remove_from_cart/', RemoveFromCart.as_view(), name="remove-from-cart"),

    path('<int:pk>/add_to_wishlist/', AddToWishList.as_view(), name="add-to-wishlist"),
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('<int:pk>/remove_from_wishlist/', RemoveFromWishList.as_view(), name="remove-from-wishlist"),

    path('<int:pk>/add_to_favourites/', AddToFavourites.as_view(), name='add-to-favourites'),
    path('favourites/', FavouriteView.as_view(), name='favourites'),
    path('<int:pk>/remove_from_favourites/', RemoveFromFavourites.as_view(), name='remove-from-favourites'),

    path('<int:pk>/review/', AddReviewView.as_view(), name='add-review'),
    path('category/<str:category>/', CategoryView.as_view(), name='view-category'),
    path('filter/', FilterProduct.as_view(), name='price-filter'),

    # admin/seller/vendor functionalities
    path('add_category/', AddCategory.as_view(), name="add-category"),
    path('update_brand/<int:pk>/', UpdateBrandName.as_view(), name="update-brand_name"),
    path('add_product/<int:pk>/', AddProductView.as_view(), name="add-product"),
    path('update_product/<int:pk>/', UpdateProductView.as_view(), name='update-product'),

    # ask for address after clicking checkout
    path('checkout/', OnlyAddress.as_view(), name='buy-now-cart'),
    # checkout page after entering address
    path('checkout/address/', CreateCheckoutSessionCart.as_view(), name='checkout-address'),
    # payment success
    path('success_cart/', PaymentSuccessViewCart.as_view(), name='success-cart'),

    # ask for quantity, address when clicked on buy-now
    path('<int:pk>/buy_now/', OrderDetailsView.as_view(), name='buy-now'),
    # checkout page after entering address, quantity
    path('api/checkout-session/<int:pk>/', CreateCheckoutSession.as_view(), name='api_checkout_session'),
    # payment success
    path('success/', PaymentSuccessView.as_view(), name='success'),

    path('orders/', PurchasedView.as_view(), name='orders'),
    path('orders/<int:pk>/', DetailPurchasedView.as_view(), name='detail-orders'),
    path('download_invoice/<int:pk>/', DownloadInvoice.as_view(), name="download-invoice"),
    path('', ProductView.as_view(), name='view-product'),
    path('view_orders/', ViewOrdersVendor.as_view(), name="view-order"),
    path('update_order_status/<int:pk>/', UpdateOrderStatus.as_view(), name="update-product-status"),
    path('return/<int:pk>/',ReturnProductView.as_view() ,name='return-product'),
    path('return_status/<int:pk>/', ReturnStatus.as_view(), name='return-status'),
    # done
    path('view_checkout/', ViewCheckout.as_view(), name='view-checkout'),



    path('failure/', FailureView.as_view(), name='failure'),


]

# path('create_session/', CreateCheckoutSession.as_view(), name='create-session'),
# path('<int:pk>/add_address/', AddAddressView.as_view(), name='buy-address'),
# path('<int:pk>/buy_now/', OrderDetailsView.as_view(), name='buy-now'),
# path('checkout/address/', AddAddressOnlyView.as_view(), name='checkout-address'),
# path('update-order-status/<int:pk>/', UpdateOrderStatusOverall.as_view(), name="update-order-status"),