
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

$('.address_delete').click(function (e) {
    e.preventDefault();

    var id = $(this).attr("pid").toString();
    var address = this

    $.ajax({
        type: "GET",
        url: "remove-address",
        data: {
            address_id: id,
        },
        success: function (response, data) {
            if (response) {
                address.parentNode.parentNode.remove()
                alertify.success(response.message)
                if (response.address_count) {
                    document.getElementById("address_count").innerText = response.address_count;
                  }
                else{
                    document.getElementById("address_count").innerText = '0';
                }
            }

        },
        error: function (xhr, status, error) {
            console.error('Error deleting the address:', error);
        }
    });
});

// Cancel order
$('.order_cancel').click(function (e) {
    e.preventDefault();

    var id = $(this).attr("pid").toString();
    var orderStatusCell = $('#order_status_' + id);

    $.ajax({
        type: "GET",
        url: "/cancel-order",
        data: {
            order_id: id,
        },
        success: function (response, data) {
            if (response) {
                orderStatusCell.text(response.order.status);
                alertify.success(response.message)
            }

        },
        error: function (xhr, status, error) {
            console.error('Error deleting the address:', error);
        }
    });
});


