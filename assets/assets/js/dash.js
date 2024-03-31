$('.cancel-order-dash').click(function () {
    var orderId = $(this).data('order-id');
    var statusCell = $(this).closest('tr').find('.order-status');
    var buttonsCell = $(this).closest('tr').find('.buttons');


    $.ajax({
        type: "POST",
        url: cancelOrderUrl,
        data: {
            order_id: orderId,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            if (response.success) {
                statusCell.text('Cancel');

                Swal.fire({
                    title: "Order Cancelled",
                    icon: "success"
                }).then(function () {

                    $.get(window.location.href, function (data) {
                        var cancelledMsgButton = $('<button class="me-3 btn btn-default btn-sm cancelled-msg" href="#">Cancelled</button>');
                        buttonsCell.find('.cancel-order-dash').replaceWith(cancelledMsgButton);
                    });
                });

            } else {
                Swal.fire({
                    title: "Order cancel failed",
                    icon: "error"
                });
                console.log(response.error)
            }
        },
        error: function (xhr, status, error) {
            console.error('Error cancelling order:', error);
        }
    });
});
