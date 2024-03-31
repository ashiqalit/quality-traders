$('.pay_with_razorpay').click(function (e) {
    e.preventDefault();
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
    var selectedAddress = $('input[name="selected_address"]:checked');
    // console.log(selectedAddress.val())
    if (!selectedAddress.val()) {
        alertify.error('Please select an address')
    }
    else {
        $.ajax({
            method: "GET",
            url: "proceed-to-pay",
            data: {
                csrfmiddlewaretoken: csrftoken,
                address_id: selectedAddress.val()
            },
            success: function (response) {
                // console.log("Response:", response);
                var address = response.address
                var options = {
                    "key": "rzp_test_1DBm3kToLW56S3", // Enter the Key ID generated from the Dashboard
                    "amount": 1 * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "Quality Traders", //your business name
                    "description": "We serve you good",
                    "image": "https://example.com/your_logo",
                    // "order_id": response, 
                    "handler": function (responseb) {
                        alert(responseb.razorpay_payment_id);
                        // alert(response.razorpay_order_id);
                        // alert(response.razorpay_signature)
                        data = {
                            "address_id": address.id,
                            "payment_mode": "Paid by Razorpay",
                            "payment_id": responseb.razorpay_payment_id,
                            csrfmiddlewaretoken: csrftoken,
                        }
                        $.ajax({
                            method: "POST",
                            url: "checkout",
                            data: data,
                            success: function (responsec) {
                                Swal.fire({
                                    icon: "success",
                                    title: responsec.status,
                                    timer: 1500
                                }).then((result) => {
                                    window.location.href = 'view-order/<str:t_no>'
                                })
                            }
                        });
                    },
                    "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information, especially their phone number
                        "name": address.fname + " " + address.lname, //your customer's name
                        "email": address.email,
                        "contact": address.phone  //Provide the customer's phone number for better conversion rates 
                    },
                    "notes": {
                        "address": "Razorpay Corporate Office"
                    },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.open();
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", error); // Log any AJAX errors for debugging
            }


        });

    }
}
);

