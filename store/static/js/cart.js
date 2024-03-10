
$('.add-to-cart').click(function (event) {
    event.preventDefault();

    var productId = $(this).data('product');

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
        },
        error: function (xhr, status, error) {
            console.error('Error adding product to cart:', error);
        }
    });
});

$('.cart_quantity_up').click(function (e) {
    e.preventDefault();

    var id = $(this).attr("pid").toString();
    var qty = this.parentNode.children[1]
    // var total_cost = $('.cart_total_price').attr('class')
    

    $.ajax({
        type: "GET",
        url: "/plus-cart",
        data: {
            product_id: id,
        },
        success: function (data,response) {
            if (data) {
                qty.innerText = data.quantity
                document.getElementById("amount").innerText ='₹'+data.amount
                document.getElementById("cart-counter").innerText = data.cart_count
                // document.getElementById("amount").innerText = data.amount
            }
        },
        error: function (xhr, status, error) {
            console.error('Error increasing the quantity:', error);
        }
    });
});

$('.cart_quantity_down').click(function (e) {
    e.preventDefault();

    var id = $(this).attr("pid").toString();
    var qty = this.parentNode.children[1]
    // var total_cost = $('.cart_total_price').attr('class')

    $.ajax({
        type: "GET",
        url: "/minus-cart",
        data: {
            product_id: id,
        },
        success: function (data, response) {
            if (data) {
                qty.innerText = data.quantity
                document.getElementById("amount").innerText = '₹'+data.amount
                document.getElementById("cart-counter").innerText = data.cart_count
                // document.getElementById("amount").innerText = data.amount
            } 

        },
        error: function (xhr, status, error) {
            console.error('Error increasing the quantity:', error);
        }
    });
});

$('.cart_quantity_delete').click(function (e) {
    e.preventDefault();

    var id = $(this).attr("pid").toString();
    var qty = this
    // var total_cost = $('.cart_total_price').attr('class')

    $.ajax({
        type: "GET",
        url: "/remove-cart",
        data: {
            product_id: id,
        },
        success: function (data, response) {
            if (data) {
                document.getElementById("amount").innerText = '₹'+data.amount
                document.getElementById("cart-counter").innerText = data.cart_count
                
                qty.parentNode.parentNode.remove()
                // document.getElementById("amount").innerText = data.amount
            } 

        },
        error: function (xhr, status, error) {
            console.error('Error increasing the quantity:', error);
        }
    });
});

