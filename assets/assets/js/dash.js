$('.cancel-order-dash').click(function () {
    var orderId = $(this).data('order-id');
    var statusCell = $(this).closest('tr').find('.order-status');

    $.ajax({
        type: "POST",
        url: cancelOrderUrl,
        data: {
            order_id: orderId,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            if (response.success) {
                statusCell.text('Cancelled');
                alert('Order cancelled successfully.');
            } else {
                alert('Failed to cancel order.');
                console.log(response.error)
            }
        },
        error: function (xhr, status, error) {
            console.error('Error cancelling order:', error);
        }
    });
});
