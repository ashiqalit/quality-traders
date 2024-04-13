from .models import Cart, Product, Wishlist
# from .filters import ProductFilter

# navbar
def cart_count(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            cart_items = cart.cartitem_set.all()
            cart_count = sum(item.product_qty for item in cart_items)
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        cart_count = 0

    return {'cart_count': cart_count}

# def filter_context(request):
#     product = Product.objects.all()
#     myfilter = ProductFilter(request.GET, queryset=product)
#     filtered_products = myfilter.qs
#     return {'myfilter': myfilter}

def wishlist_count(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            wishlist = Wishlist.objects.get(user=user)
            wishlist_count = wishlist.wishlistitem_set.count()
        except Wishlist.DoesNotExist:
            wishlist_count = 0
    else:
        wishlist_count = 0
    return {'wishlist_count':wishlist_count}