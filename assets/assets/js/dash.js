$('.cancel-order-dash').click(function (e) {
    var orderId = $(this).data('order-id');
    var statusCell = $(this).closest('tr').find('.order-status');
    var buttonsCell = $(this).closest('tr').find('.buttons');

    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, cancel it!",
        confirmButtonClass: "btn btn-primary",
        cancelButtonClass: "btn btn-danger ml-1",
        buttonsStyling: false
    }).then(function (result) {
        if (result.value) {
            e.preventDefault(e);
            // User confirmed the delete action
            $.ajax({
                type: "GET",
                url: "/dashboard/cancel_order",
                data: {
                    order_id: orderId,
                    // csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (response) {
                    if (response) {
                        // statusCell.text('Cancel');

                        Swal.fire({
                            title: response.message,
                            icon: "success"
                          }).then(function (result) {
                            if (result.isConfirmed) {  // Check if user clicked "OK"
                              window.location.href = "/dashboard/orders"; // Redirect to read_orders URL
                            }
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
        }
    });
});

// Preview image that going to upload as product image
$(document).ready(function () {
    var imageInput = $('input[type="file"]');
    var imagePreview = $('#uploadedImagePreview');

    imageInput.on('change', function () {
        var file = this.files[0];
        if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
                imagePreview.attr('src', e.target.result);
            }
            reader.readAsDataURL(file);
        } else {
            imagePreview.attr('src', '{% static "assets/img/icons/upload.svg" %}');
        }
    });
});

// Ask confirmation to delete a product image, and assigning the default image.
$(document).ready(function () {
    $("#deleteImageModal").click(function (e) {
        var defaultImageURL = "{% static 'ecommerce/p-img/default-product-image.jpg' %}";
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Yes, delete it!",
            confirmButtonClass: "btn btn-primary",
            cancelButtonClass: "btn btn-danger ml-1",
            buttonsStyling: false
        }).then(function (result) {
            if (result.value) {
                e.preventDefault();
                // User confirmed the delete action
                var data = {
                    'csrfmiddlewaretoken': csrf_token
                };
                // Send AJAX request to delete endpoint
                $.ajax({
                    url: deleteUrl,
                    type: 'POST',
                    data: data,
                    dataType: 'json',
                    success: function (response) {
                        if (response.success) {
                            $("#product-image").attr("src", defaultImageURL)
                            Swal.fire({
                                type: "success",
                                title: "Deleted!",
                                text: "Your image has been deleted.",
                                confirmButtonClass: "btn btn-success"
                            }).then(function () {
                                location.reload();
                            })
                        } else {
                            Swal.fire({
                                type: "error",
                                title: "Error",
                                text: "Failed to delete the image.",
                                confirmButtonClass: "btn btn-danger"
                            });
                        }
                    },
                    error: function () {
                        Swal.fire({
                            type: "error",
                            title: "Error",
                            text: "Failed to communicate with the server.",
                            confirmButtonClass: "btn btn-danger"
                        });
                    }
                });
            }
        });
    });
});