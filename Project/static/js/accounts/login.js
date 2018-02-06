$( document ).ready(function() {

    var submitForm = function () {
        var form_data = new FormData($('.form-signin')[0]);
        $.ajax({
            url: "/accounts/login/",
            data: form_data,
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (msg) {
            if (msg['ok']){
                console.log(msg);
                window.location = msg['ok'];
            }else
            {
                console.log(msg);
            }
        });
    };

    $('.btn').click(function (e) {
        e.preventDefault();
        submitForm();

    });

});
