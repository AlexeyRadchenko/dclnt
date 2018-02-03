/**
 * Created by alexey on 20.12.17.
 */
$( document ).ready(function() {

    var submitForm = function () {
        var form_data = new FormData($('.form-signin')[0]);
        $.ajax({
            url: "/management/login/",
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

    $('#signinbutton').click(function (e) {
        e.preventDefault();
        submitForm();

    });

});