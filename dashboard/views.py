# Standard library
from datetime import datetime, timedelta
from collections import defaultdict

# Third party
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, admin
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models import Sum
from django.views.decorators.cache import never_cache

# Local application
from store.models import (
    Category,
    Product,
    Sub_category,
    Brand,
    Order,
    OrderItem,
    ReturnRequest,
    Wallet,
    WalletTransaction,
    Coupon,
    Product,
    Offer,
)

from .filters import (
    UserFilter,
    CategoryFilter,
    ProductFilter,
    SubCategoryFilter,
    BrandFilter,
    CouponFilter,
    OfferFilter,
)
from .forms import (
    CategoryForm,
    ProductForm,
    SubCategoryForm,
    BrandForm,
    OrderForm,
    CouponForm,
    OfferForm,
)


def superuser_check(user):
    return user.is_superuser


# Create your views here.
@user_passes_test(superuser_check)
def dashboard(request):
    if "username" not in request.session:
        return redirect("dashboard_login")
    # top 10 products
    top_products = Product.objects.annotate(order_count=Count("orderitem")).order_by(
        "order_count"
    )[:10]
    # top 10 categories
    categories = Category.objects.all()
    category_order_counts = {}
    for category in categories:
        products_in_category = category.product_set.all()
        total_order_count = products_in_category.aggregate(
            total_order_count=Sum("orderitem__quantity")
        )["total_order_count"]
        total_order_count = total_order_count or 0
        category_order_counts[category] = total_order_count
    top_categories = sorted(
        category_order_counts.items(), key=lambda x: x[1], reverse=True
    )[:10]
    # top 10 brands
    brands = Brand.objects.all()
    brand_order_counts = {}
    for brand in brands:
        products_in_brand = brand.product_set.all()
        total_order_count = products_in_brand.aggregate(
            total_order_count=Sum("orderitem__quantity")
        )["total_order_count"]
        total_order_count = total_order_count or 0
        brand_order_counts[brand] = total_order_count
    top_brands = sorted(brand_order_counts.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]
    # order based on year, month, day
    sales_from = request.GET.get("sales_from")
    sales_to = request.GET.get("sales_to")

    if sales_from and sales_to:
        # Add one day to sales_to to include it in the range
        sales_to_modified = datetime.strptime(sales_to, "%Y-%m-%d") + timedelta(days=1)
        orders = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(
                created_at__range=[sales_from, sales_to_modified],
            )
        )
    elif sales_from:
        orders = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(
                created_at__gte=sales_from,
            )
        )
    elif sales_to:
        orders = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(
                created_at__lte=sales_to,
            )
        )
    else:
        orders = Order.objects.all().order_by("-created_at")

    # initialize a dictionary to store the order_count per date
    order_counts_dict = defaultdict(int)
    # order counts per date
    order_count_per_date = orders.values("created_at__date").annotate(
        order_count=Count("id")
    )
    # extract date and order counts
    for entry in order_count_per_date:
        date = entry["created_at__date"].strftime("%Y-%m-%d")
        order_counts_dict[date] += entry["order_count"]

    dates = list(order_counts_dict.keys())
    order_counts = list(order_counts_dict.values())
    # dates = [entry['created_at__date'].strftime('%Y-%m-%d') for entry in order_count_per_date]
    # order_counts = [entry['order_count'] for entry in order_count_per_date]
    context = {
        "top_products": top_products,
        "top_categories": top_categories,
        "top_brands": top_brands,
        "dates": dates,
        "order_counts": order_counts,
    }
    return render(request, "dashboard/other/index.html", context)


@never_cache
def admin_login(request):
    if "username" in request.session:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user_ = auth.authenticate(username=username, password=password)

        if user_ is not None:
            if not user_.is_superuser:
                messages.info(request, "You do not have admin privileges")
                return redirect("dashboard_login")
            auth.login(request, user_)
            request.session["username"] = username
            return redirect("dashboard")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("dashboard_login")
    else:
        return render(request, "dashboard/auth/admin_signin.html")


@user_passes_test(superuser_check)
def logout(request):
    if "username" in request.session:
        request.session.flush()
    auth.logout(request)
    return redirect("dashboard_login")


# user............................................................
@user_passes_test(superuser_check)
def list_user(request):
    users = User.objects.all()
    _filter = UserFilter(request.GET, queryset=users)
    filtered_users = _filter.qs
    context = {"all_users": filtered_users}
    return render(request, "dashboard/other/userlist.html", context)


@user_passes_test(superuser_check)
def update_user_status(request):
    if request.method == "POST":
        try:
            user_id = request.POST.get("userId")
            user = User.objects.get(id=user_id)
            ischecked = request.POST.get("ischecked") == "true"
            user.is_active = ischecked
            user.save()
            message = "User activated" if ischecked else "User blocked"
            return JsonResponse({"status": "success", "message": message})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invalid user ID"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})


# categories.............................................................................
@user_passes_test(superuser_check)
def list_categories(request):
    categories = Category.objects.all()
    myFilter = CategoryFilter(request.GET, queryset=categories)
    filterd_categories = myFilter.qs
    context = {"all_categories": filterd_categories, "myFilter": myFilter}
    return render(request, "dashboard/other/categorylist.html", context)


@user_passes_test(superuser_check)
def create_categories(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("read_category")
    else:
        form = CategoryForm()
    return render(request, "dashboard/other/addcategory.html", {"form": form})


@user_passes_test(superuser_check)
def update_category(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("read_categories")
    else:
        form = CategoryForm(instance=category)
    context = {
        "user": category,
        "form": form,
        "pk": category.pk,
    }
    return render(request, "dashboard/other/editcategory.html", context)


@user_passes_test(superuser_check)
def drop_category(request):
    if request.method == "POST":
        category_id = request.POST.get("categoryId")
        category = Category.objects.get(id=category_id)
        category.delete()
        return JsonResponse({"success": True})
        # return redirect('read_categories')
    return JsonResponse({"success": False})


# coupons..................................................................................
@user_passes_test(superuser_check)
def list_coupons(request):
    coupons = Coupon.objects.all()
    myfilter = CouponFilter(request.GET, queryset=coupons)
    filtered_coupons = myfilter.qs
    context = {"all_coupons": filtered_coupons, "myfilter": myfilter}
    return render(request, "dashboard/other/couponlist.html", context)


@user_passes_test(superuser_check)
def create_coupon(request):
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("read_coupons")
    else:
        form = CouponForm()
    return render(request, "dashboard/other/addcoupon.html", {"form": form})


@user_passes_test(superuser_check)
def update_coupon(request, pk):
    coupon = Coupon.objects.get(id=pk)
    form = CouponForm(instance=coupon)
    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect("read_coupons")
    context = {"form": form, "pk": coupon.pk}
    return render(request, "dashboard/other/editcoupon.html", context)


@user_passes_test(superuser_check)
def drop_coupon(request):
    if request.method == "POST":
        coupon_id = request.POST.get("couponId")
        coupon = Coupon.objects.get(id=coupon_id)
        coupon.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


# Offers...................................................................................
@user_passes_test(superuser_check)
def list_offers(request):
    offers = Offer.objects.all().order_by('-name')
    myfilter = OfferFilter(request.GET, queryset=offers)
    filtered_offers = myfilter.qs
    context = {"all_offers": filtered_offers, "myfilter": myfilter}
    return render(request, "dashboard/other/offerlist.html", context)

@user_passes_test(superuser_check)
def create_offer(request):
    if request.method == "POST":
        form = OfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("read_offers")
    else:
        form = OfferForm()
    return render(request, "dashboard/other/addoffer.html", {"form": form})

@user_passes_test(superuser_check)
def update_offer(request, pk):
    offer = Offer.objects.get(id=pk)
    form = OfferForm(instance=offer)
    if request.method == "POST":
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect("read_offers")
    context = {"form": form, "pk": offer.pk}
    return render(request, "dashboard/other/editoffer.html", context)

@user_passes_test(superuser_check)
def drop_offer(request):
    if request.method == "POST":
        offer_id = request.POST.get("offerId")
        offer = Offer.objects.get(id=offer_id)
        offer.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})
# products.................................................................................
@user_passes_test(superuser_check)
def list_products(request):
    products = Product.objects.all().order_by("name")
    myFilter = ProductFilter(request.GET, queryset=products)
    filterd_products = myFilter.qs
    discounted_total = 0
    for product in products:
        if product.offer or product.sub_category.offer:
            discounted_price, total_offer_price = product.get_discounted_price()
            product.final_price = discounted_price
            product.total_offer = total_offer_price
        product.availability = "Out of stock" if product.quantity == 0 else "In stock"
        product.save()
    context = {"all_products": filterd_products, "myFilter": myFilter}
    return render(request, "dashboard/other/productlist.html", context)


@user_passes_test(superuser_check)
def create_products(request):
    # product - request.model.product
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("read_products")
    else:
        form = ProductForm()
    return render(request, "dashboard/other/addproduct.html", {"form": form})


@user_passes_test(superuser_check)
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    default_image_path = "ecommerce/p-img/default-product-image.jpg"

    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("read_products")
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
        "product": product,
        "pk": product.pk,
        "default_image_path": default_image_path,
    }
    return render(request, "dashboard/other/editproduct.html", context)


# Delete product image
@user_passes_test(superuser_check)
def delete_product_image(request, pk):
    if request.method == "POST":
        product = Product.objects.get(id=pk)
        if product.image:
            product.image.delete()
            product.image = "ecommerce/p-img/default-product-image.jpg"
            product.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {"success": False, "error": "No image found for product"}
            )
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})


@user_passes_test(superuser_check)
def drop_product(request):
    if request.method == "POST":
        product_id = request.POST.get("productId")
        product = Product.objects.get(id=product_id)
        product.delete()
        return JsonResponse({"success": True})
        # return redirect('read_categories')
    return JsonResponse({"success": False})


# subcategories.............................................................
@user_passes_test(superuser_check)
def list_subcategories(request):
    subcategories = Sub_category.objects.all()
    myFilter = SubCategoryFilter(request.GET, queryset=subcategories)
    filterd_categories = myFilter.qs
    context = {"all_categories": filterd_categories, "myFilter": myFilter}
    return render(request, "dashboard/other/subcategorylist.html", context)


@user_passes_test(superuser_check)
def create_subcategories(request):
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create_subcategory")
    else:
        form = SubCategoryForm()
    return render(request, "dashboard/other/subaddcategory.html", {"form": form})


@user_passes_test(superuser_check)
def update_subcategory(request, pk):
    subcategory = Sub_category.objects.get(id=pk)
    form = SubCategoryForm(instance=subcategory)
    if request.method == "POST":
        form = SubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect("read_subcategories")
    else:
        form = SubCategoryForm(instance=subcategory)
    context = {
        "user": subcategory,
        "form": form,
        "pk": subcategory.pk,
    }
    return render(request, "dashboard/other/editsubcategory.html", context)


@user_passes_test(superuser_check)
def drop_subcategory(request):
    if request.method == "POST":
        subcategory_id = request.POST.get("subcategoryId")
        subcategory = Category.objects.get(id=subcategory_id)
        subcategory.delete()
        return JsonResponse({"success": True})
        # return redirect('read_categories')
    return JsonResponse({"success": False})


# brands.............................................................
@user_passes_test(superuser_check)
def list_brands(request):
    brands = Brand.objects.all()
    myFilter = BrandFilter(request.GET, queryset=brands)
    filterd_brands = myFilter.qs
    context = {"all_brands": filterd_brands, "myFilter": myFilter}
    return render(request, "dashboard/other/brandlist.html", context)


@user_passes_test(superuser_check)
def create_brands(request):
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("read_brands")
    else:
        form = BrandForm()
    return render(request, "dashboard/other/addbrand.html", {"form": form})


@user_passes_test(superuser_check)
def update_brand(request, pk):
    brand = Brand.objects.get(id=pk)
    default_image_path = "ecommerce/p-img/default-product-image.jpg"
    
    form = BrandForm(instance=brand)
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES,instance=brand)
        if form.is_valid():
            form.save()
            return redirect("read_brands")
    else:
        form = BrandForm(instance=brand)
    context = {
        "brand": brand,
        "form": form,
        "pk": brand.pk,
        "default_image_path": default_image_path,
    }
    return render(request, "dashboard/other/editbrand.html", context)

# Delete brand image
@user_passes_test(superuser_check)
def delete_brand_image(request, pk):
    if request.method == "POST":
        brand = Brand.objects.get(id=pk)
        if brand.image:
            brand.image.delete()
            brand.image = "ecommerce/p-img/default-product-image.jpg"
            brand.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse(
                {"success": False, "error": "No image found for product"}
            )
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})

@user_passes_test(superuser_check)
def drop_brand(request):
    if request.method == "POST":
        brand_id = request.POST.get("brandId")
        brand = Brand.objects.get(id=brand_id)
        brand.delete()
        return JsonResponse({"success": True})
        # return redirect('read_categories')
    return JsonResponse({"success": False})


# orders...........................................................................
@user_passes_test(superuser_check)
def list_orders(request):
    sales_from = request.GET.get("sales_from")
    sales_to = request.GET.get("sales_to")

    if "today" in request.GET:
        today = str(datetime.now().date())
        sales_from = today
        sales_to = today

    if "yesterday" in request.GET:
        yesterday = str(datetime.now().date() - timedelta(days=1))
        sales_from = yesterday
        sales_to = yesterday

    if "last_seven" in request.GET:
        sales_from = str(datetime.now().date() - timedelta(days=7))
        sales_to = str(datetime.now().date())

    if "last_thirty" in request.GET:
        thirty_days_ago = str(datetime.now().date() - timedelta(days=30))
        sales_from = thirty_days_ago
        sales_to = str(datetime.now().date())

    if "last_month" in request.GET:
        # Calculate the first day of the previous month
        first_day_of_last_month = datetime.now().date() - relativedelta(months=1)
        first_day_of_last_month = first_day_of_last_month.replace(day=1)
        # Calculate the last day of the previous month
        last_day_of_last_month = first_day_of_last_month + relativedelta(day=31)
        # Adjust the last day to the actual last day of the month
        # last_day_of_last_month = last_day_of_last_month - timedelta(days=last_day_of_last_month.day)

        sales_from = str(first_day_of_last_month)
        sales_to = str(last_day_of_last_month)

    if "this_week" in request.GET:
        # Get today's date
        today = datetime.now().date()
        # Calculate the start of the current week (Monday)
        start_of_week = today - timedelta(days=today.weekday())
        # Calculate the end of the current week (Sunday)
        end_of_week = start_of_week + timedelta(days=6)

        sales_from = str(start_of_week)
        sales_to = str(end_of_week)

    if "this_month" in request.GET:
        # Get today's date
        today = datetime.now().date()
        # Calculate the first day of the current month
        first_day_of_month = today.replace(day=1)
        # Calculate the last day of the current month
        if today.month == 12:
            last_day_of_month = today.replace(
                year=today.year + 1, month=1, day=1
            ) - timedelta(days=1)
        else:
            last_day_of_month = today.replace(month=today.month + 1, day=1) - timedelta(
                days=1
            )

        sales_from = str(first_day_of_month)
        sales_to = str(last_day_of_month)

    if sales_from and sales_to:
        # Add one day to sales_to to include it in the range
        sales_to_modified = datetime.strptime(sales_to, "%Y-%m-%d") + timedelta(days=1)
        orders = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(
                created_at__range=[sales_from, sales_to_modified],
            )
        )
    elif sales_from:
        orders = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(
                created_at__gte=sales_from,
            )
        )
    elif sales_to:
        orders = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(
                created_at__lte=sales_to,
            )
        )
    else:
        orders = Order.objects.all().order_by("-created_at")
    context = {"orders": orders}
    return render(request, "dashboard/other/orderlist.html", context)


@user_passes_test(superuser_check)
def edit_order(request, pk):
    order = Order.objects.get(id=pk)
    # form = OrderForm(instance=order)
    wallet = Wallet.objects.get(user=request.user)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            if order.status == 4 and order.payment != 2:
                order.payment = 2
                order.save()
            return redirect("read_orders")
        else:
            messages.info(request, "Form invalid")
    else:
        form = OrderForm(instance=order)
    context = {
        "order": order,
        "form": form,
        "pk": order.pk,
    }
    return render(request, "dashboard/other/editorder.html", context)


@user_passes_test(superuser_check)
def cancel_order(request):
    if request.method == "GET":
        try:
            order_id = request.GET["order_id"]
            order = get_object_or_404(Order, id=order_id)
            # Start transaction to ensure atomicity
            with transaction.atomic():
                # Change order status to 'Cancel'
                order.status = 6
                order.save()

                # Increment product quantities
                order_items = order.orderitem_set.all()
                for order_item in order_items:
                    product = order_item.product
                    product.quantity += order_item.quantity
                    product.save()

                try:
                    wallet = Wallet.objects.get(user=request.user)
                except:
                    wallet = Wallet.objects.create(user=request.user)
                # Set the amount based on payment mode
                # if order.payment_mode == 'Razorpay':
                #     amount = int(order.grand_total)
                # else:
                #     amount = order.grand_total
                if order.payment_mode != "COD":
                    wallet_transaction = WalletTransaction.objects.create(
                        wallet=wallet,
                        order=order,
                        amount=order.grand_total,
                        status="Order cancel amount credited",
                    )
                    wallet_transaction.save()

            return JsonResponse(
                {"message": "Order Cancelled", "order": order.serialize()}
            )
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order does not exists"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=505)


@user_passes_test(superuser_check)
def return_requests_list(request):
    pending_return_requests = ReturnRequest.objects.filter(status=1)
    context = {
        "pending_return_requests": pending_return_requests,
    }
    return render(request, "dashboard/other/returnrequests.html", context)


@user_passes_test(superuser_check)
def approve_return_request(request, return_request_id):
    return_request = ReturnRequest.objects.get(id=return_request_id)
    return_request.status = 2
    return_request.order.status = 7
    return_request.order.save()
    return_request.save()

    # Returning paid amount to wallet
    order = return_request.order
    try:
        wallet = Wallet.objects.get(user=request.user)
    except:
        wallet = Wallet.objects.create(user=request.user)
    wallet_transaction = WalletTransaction.objects.create(
        wallet=wallet,
        order=order,
        amount=order.grand_total,
        status="Order return amount credited",
    )
    wallet_transaction.save()

    # Increment product quantities
    order_items = order.orderitem_set.all()
    for order_item in order_items:
        product = order_item.product
        product.quantity += order_item.quantity
        product.save()

    return redirect("read_return_requests")


@user_passes_test(superuser_check)
def reject_return_request(request, return_request_id):
    if request.method == "POST":
        return_request = ReturnRequest.objects.get(id=return_request_id)
        return_request.status = 3
        return_request.order.status = 8
        return_request.order.save()
        rejection_message = request.POST.get("rejection_message")
        return_request.rejection_message = rejection_message
        return_request.save()
        return redirect("read_return_requests")
    else:
        return HttpResponseNotAllowed(["POST"])


# Take pdf sales report
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


@user_passes_test(superuser_check)
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):

        sales_from = request.GET.get("sales_from")
        sales_to = request.GET.get("sales_to")

        if sales_to:
            sales_to_datetime = datetime.strptime(sales_to, "%Y-%m-%d")
            sales_to_modified = sales_to_datetime + timedelta(days=1)
        else:
            # If sales_to is empty, set it to current datetime
            sales_to_modified = datetime.now()

        if not sales_from:
            sales_from = datetime.now() - timedelta(days=3 * 365)

        orders = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(created_at__range=[sales_from, sales_to_modified])
        )

        # Calculate total amount of the sale of the selected range
        total_amount = sum(item.grand_total for item in orders)
        total_discount = sum(round(float(item.total_discount), 2) for item in orders)
        total_amount_without_discount = sum(item.total_price for item in orders)
        offer_amount = sum(item.offer_discount_price for item in orders)
        coupon_amount = sum(item.coupon_discount_price for item in orders)

        data = {
            "company": "Quality Traders",
            "address": "Perinthalmanna Road, Pulamanthole",
            "city": "Malappuram",
            "state": "Kerala",
            "zipcode": "679309",
            "orders": orders,
            "phone": "9999999999",
            "email": "qualitytraders@gmail.com",
            "website": "www.qualitytraders.com",
            "total_amount": total_amount,
            "offer_amount": offer_amount,
            "coupon_amount": coupon_amount,
            "total_discount": total_discount,
            "total_amount_without_discount": total_amount_without_discount,
        }

        pdf = render_to_pdf("dashboard/other/salesreport.html", data)
        return HttpResponse(pdf, content_type="application/pdf")

        # force download

        # response = HttpResponse(pdf, content_type="application/pdf")
        # filename = f"Sales Report (datetime.now()).pdf"
        # content = "attachment; filename=%s" % (filename)
        # response['Content-Disposition'] = content
        # return response


# Download Excel sales report
import xlwt


@user_passes_test(superuser_check)
def download_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        "attachment; filename=SalesReport-" + str(datetime.now()) + "-.xls"
    )
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("SalesReport")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        "Order ID",
        "User",
        "Date",
        "Time",
        # "Product",
        # "Quantity",
        "Price",
        "Payment Method",
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    sales_from = request.GET.get("sales_from")
    sales_to = request.GET.get("sales_to")

    sales_to_datetime = datetime.strptime(sales_to, "%Y-%m-%d")
    sales_to_modified = sales_to_datetime + timedelta(days=1)

    if not sales_from:
        sales_from = datetime.now() - timedelta(days=3 * 365)

    if not sales_to:
        sales_to = datetime.now()

    orders = (
        Order.objects.all()
        .order_by("-created_at")
        .filter(created_at__range=[sales_from, sales_to_modified])
        .values_list(
            "tracking_no",
            "user__username",
            "created_at__date",
            "created_at__time",
            # "orderitem__product__name",
            # "orderitem__quantity",
            "orderitem__price",
            "payment_mode",
        )
    )
    for order in orders:
        row_num += 1
        for col_num in range(len(order)):
            ws.write(row_num, col_num, str(order[col_num]), font_style)

    wb.save(response)
    return response


@user_passes_test(superuser_check)
def list_sales(request):
    # orders = Order.objects.all()
    # context = {'orders':orders}

    sales_from = request.GET.get("sales_from")
    sales_to = request.GET.get("sales_to")

    if "today" in request.GET:
        today = str(datetime.now().date())
        sales_from = today
        sales_to = today

    if "yesterday" in request.GET:
        yesterday = str(datetime.now().date() - timedelta(days=1))
        sales_from = yesterday
        sales_to = yesterday

    if "last_seven" in request.GET:
        sales_from = str(datetime.now().date() - timedelta(days=7))
        sales_to = str(datetime.now().date())

    if "last_thirty" in request.GET:
        thirty_days_ago = str(datetime.now().date() - timedelta(days=30))
        sales_from = thirty_days_ago
        sales_to = str(datetime.now().date())

    if "last_month" in request.GET:
        # Calculate the first day of the previous month
        first_day_of_last_month = datetime.now().date() - relativedelta(months=1)
        first_day_of_last_month = first_day_of_last_month.replace(day=1)
        # Calculate the last day of the previous month
        last_day_of_last_month = first_day_of_last_month + relativedelta(day=31)
        # Adjust the last day to the actual last day of the month
        # last_day_of_last_month = last_day_of_last_month - timedelta(days=last_day_of_last_month.day)

        sales_from = str(first_day_of_last_month)
        sales_to = str(last_day_of_last_month)

    if "this_week" in request.GET:
        # Get today's date
        today = datetime.now().date()
        # Calculate the start of the current week (Monday)
        start_of_week = today - timedelta(days=today.weekday())
        # Calculate the end of the current week (Sunday)
        end_of_week = start_of_week + timedelta(days=6)

        sales_from = str(start_of_week)
        sales_to = str(end_of_week)

    if "this_month" in request.GET:
        # Get today's date
        today = datetime.now().date()
        # Calculate the first day of the current month
        first_day_of_month = today.replace(day=1)
        # Calculate the last day of the current month
        if today.month == 12:
            last_day_of_month = today.replace(
                year=today.year + 1, month=1, day=1
            ) - timedelta(days=1)
        else:
            last_day_of_month = today.replace(month=today.month + 1, day=1) - timedelta(
                days=1
            )

        sales_from = str(first_day_of_month)
        sales_to = str(last_day_of_month)

    request.session["sales_from"] = sales_from
    request.session["sales_to"] = sales_to

    if sales_from and sales_to:
        # Add one day to sales_to to include it in the range
        sales_to_modified = datetime.strptime(sales_to, "%Y-%m-%d") + timedelta(days=1)
        sales_report = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(created_at__range=[sales_from, sales_to_modified], payment=2)
        )
    elif sales_from:
        sales_report = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(created_at__gte=sales_from, payment=2)
        )
    elif sales_to:
        sales_report = (
            Order.objects.all()
            .order_by("-created_at")
            .filter(created_at__lte=sales_to, payment=2)
        )
    else:
        sales_report = Order.objects.all().order_by("-created_at").filter(payment=2)
    context = {"orders": sales_report}
    return render(request, "dashboard/other/saleslist.html", context)
