# Templates

## Product App
FAILURE_PAYMENT_TEMPLATE = "product/failure_payment.html"
SUCCESS_PAYMENT_TEMPLATE = "product/success_payment.html"
RETURN_PRODUCT_TEMPLATE = "product/return.html"
UPDATE_ORDER_STATUS_TEMPLATE = "product/update_order_status.html"
VIEW_ORDER_VENDOR_TEMPLATE = "product/view_order_vendor.html"
INVOICE_TEMPLATE = "product/invoice.html"
ADMIN_FUNCTIONALITY_TEMPLATE = "product/admin_func.html"
DETAILS_ORDER_TEMPLATE = "product/detail_order.html"
VIEW_PURCHASES_TEMPLATE = "product/view_purchased.html"
ADDRESS_QUANTITY_PAGE_TEMPLATE = "product/buy_address.html"
ADDRESS_PAGE_TEMPLATE = "product/only_address.html"
VIEW_CHECKOUT_TEMPLATE = "product/view_checkout.html"
UPDATE_PRODUCT_TEMPLATE = "product/update_product.html"
ADD_PRODUCT_TEMPLATE = "product/add_product.html"
UPDATE_BRAND_NAME_TEMPLATE = "product/update_brand_name.html"
ADD_CATEGORY_TEMPLATE = "product/add_category.html"
FILTER_RESULT_TEMPLATE = "product/filter_result.html"
FAVOURITES_TEMPLATE = "product/favourites.html"
WISHLIST_TEMPLATE = "product/wishlist.html"
ADD_TO_CART_TEMPLATE = "product/add_to_cart.html"
HOME_TEMPLATE = "product/home.html"
SEARCH_TEMPLATE = "product/search.html"

## User App
CHANGE_PASSWORD_TEMPLATE = "store/change_password.html"
PROFILE_TEMPLATE = "store/profile.html"
ABOUT_TEMPLATE = "store/about.html"
FEEDBACK_TEMPLATE = "store/feedback.html"
REGISTER_BRAND_TEMPLATE = "store/register_brand.html"
REGISTER_USER_TEMPLATE = 'store/register.html'




# Iterators

ORDER_STATUS_FIELDS = ["status", "is_picked", "is_returned"]
ORDER_UPDATE_STATUS_CHOICES = [
    ("Initialized", "Initialized"),
    ("Packed", "Packed"),
    ("Shipped", "Shipped"),
    ("Reached Distribution Centre", "Reached Distribution Centre"),
    ("Delivered", "Delivered")
]
GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)

# Messages
PASSWORD_CHANGED_SUCCESSFULLY_MESSAGE = "Successfully Changed Your Password"
BRAND_SUCCESSFULLY_CREATED_MESSAGE = "Successfully created brand"
ACCOUNT_CREATED_SUCCESSFULLY_MESSAGE = "Successfully created account."
INVALID_DATA_MESSAGE = "Invalid data. Please try again."