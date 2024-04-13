$(document).ready(function () {
    // console.log("script loaded")
    $(".filter-checkbox").change(function (e) { 
        e.preventDefault();

        console.log('A checkbox have been clicked')

        let filter_object = {}

        $(".filter-checkbox-input").each(function () { 
            let filter_key = $(this).data("filter")
            let filter_value = $(this).val()

            // console.log("Filter key is:", filter_key)
            // console.log("Filter value is:", filter_value)
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        });
        console.log("Filter object is: ", filter_object)
        $.ajax({
            url: "/filter-products",
            data: filter_object,
            dataType: "json",
            beforeSend: function(){
                console.log("Sending data...")
            },
            success: function (response) {
                console.log(response)
                console.log('Data filtered successfully')
                $("#filtered-product").html(response.data)
            },
        });
    });
});
