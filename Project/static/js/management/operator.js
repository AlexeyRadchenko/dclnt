$( document ).ready(function() {
    /*$('.nav-tabs a').click(function(){
        $(this).tab('show');
    });

    $('ul.li.active').removeClass('active');
    $('a[href="' + location.pathname + '"]').closest('li').addClass('active');

    */

    /*menu handler*/
    var removeActive = function() {
        $('nav.a').parents( "li, ul" ).removeClass("active");
    };

    $( "nav.li" ).click(function() {
        removeActive();
        $(this).addClass( "active" );
    });

    removeActive();
    $( "a[href='" + location.hash + "']" ).parent( "li" ).addClass( "active" );

    /*var myRedirect = function(redirectUrl, arg, value) {
        var form = $('<form action="' + redirectUrl + '" method="post">' +
        '<input type="hidden" name="'+ arg +'" value="' + value + '"></input>' + '</form>');
        $('body').append(form);
        $(form).submit();
    };
    myRedirect('/management/login/')*/

    var submitForm = function () {
        //var form_data = new FormData($('.form-signin')[0]);
        $.ajax({
            url: "/management/user/",
            //data: form_data,
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (msg) {
            window.location = msg['ok'];
        });
    };

    $('#log_out').click(function (e) {
        e.preventDefault();
        submitForm();
    });
});
