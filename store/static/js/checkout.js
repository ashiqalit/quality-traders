$('.pay_with_razorpay').click(function (e) {
    e.preventDefault();
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    var selectedAddress = $('input[name="selected_address"]:checked');
    var payment_mode = $(this).val();
    var grandTotalText = $('.grand_total').text();
    var grandTotalNumeric = parseFloat(grandTotalText.replace('₹', ''));
    var neworder = $(this).data('neworder');
    console.log(neworder)
    // console.log(payment_mode)
    // console.log(selectedAddress.val())
    
    if (!selectedAddress.val()) {
        swal.fire({
            icon:'error',
            title:'Select an address',
            timer:1000
        })
        return false
    }
    else {
        $.ajax({
            method: "GET",
            url: "proceed-to-pay",
            data: {
                csrfmiddlewaretoken: csrftoken,
                address_id: selectedAddress.val(),
                grand_total: grandTotalNumeric, 
            },
            success: function (response) {
                // console.log("Response:", response);
                var address = response.address
                var options = {
                    "key": "rzp_test_1DBm3kToLW56S3", // Enter the Key ID generated from the Dashboard
                    "amount": Math.round(response.grand_total * 100), // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "Quality Traders", //your business name
                    "description": "We serve you good",
                    "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.svgrepo.com%2Fsvg%2F52605%2Fbill&psig=AOvVaw1GgGA5LKFC3Fn_MUhuJFlo&ust=1712034347561000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCNCat5ufoIUDFQAAAAAdAAAAABAE",
                    // "order_id": response.order.id,
                    "handler": function (responseb) {
                        alert(responseb.razorpay_payment_id);
                        data1 = {
                            "selected_address": selectedAddress.val(),
                            "payment_mode": payment_mode,
                            "payment_id": responseb.razorpay_payment_id,
                            csrfmiddlewaretoken: csrftoken,
                        }
                        $.ajax({
                            method: "POST",
                            url: "checkout",
                            data: data1,    
                            success: function (responsec) {
                                Swal.fire({
                                    icon: "success",
                                    title: responsec.status,
                                    timer: 1500
                                }).then((result) => {
                                    window.location.href = 'view-order/' + responsec.t_no;
                                })
                            }
                        });
                    },
                    "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                        "name": address.fname + " " + address.lname, //your customer's name
                        "email": address.email,
                        "contact": address.phone  //Provide the customer's phone number for better conversion rates 
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.on('payment.failed', function (response){
                    // alert(response.error.code);
                    alert(response.error.description);
                    // alert(response.error.source);
                    // alert(response.error.step);
                    // alert(response.error.reason);
                    // alert(response.error.metadata.order_id);
                    // alert(response.error.metadata.payment_id);
            });
                rzp1.open();
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", error); // Log any AJAX errors for debugging
            }


        });

    }
}
);

