$('.add-to-wishlist').click(function (e) {
    e.preventDefault();

    var productId = $(this).data('product');

    $.ajax({
        type: "POST",
        url: "/add-to-wishlist",
        data: {
            'product_id': productId,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            console.log('Product added to wishlist', response);
            var icon = response.success ? 'success' : 'warning';

            Swal.fire({
                title: response.message,
                icon: icon,
            });
            document.getElementById("wishlist-counter").innerText = response.wishlist_counter

        },
        error: function (xhr, status, error) {
            console.error('Error adding product to wishlist:', error);
        }
    });
});

$('.wishlist_item_delete').click(function (e) {
    e.preventDefault();

    var id = $(this).data('wishlist_items');
    var delete_icon = this

    $.ajax({
        type: "GET",
        url: "/remove-wishlistitem",
        data: {
            product_id: id,
        },
        success: function (data, response) {
            if (data) {
                document.getElementById("wishlist-counter").innerText = data.wishlist_count;
                delete_icon.parentNode.parentNode.remove()
                location.reload();
            }
        },
        error: function (xhr, status, error) {
            console.error('Error deleting the item:', error);
        }
    });
});

$('.add-to-wishlist-cart').click(function (event) {
    event.preventDefault();

    var productId = $(this).data('wishlist_items');
    var addToCartBtn = this

    $.ajax({
        url: '/add-to-cart',
        type: 'POST',
        data: {
            'product_id': productId,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            console.log('Product added to cart:', response);
            alertify.success(response.message);
            document.getElementById("cart-counter").innerText = response.cart_counter
            addToCartBtn.parentNode.parentNode.remove()
            location.reload();
        },
        error: function (xhr, status, error) {
            console.error('Error adding product to cart:', error);
        }
    });
});