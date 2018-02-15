//https://uxsolutions.github.io/bootstrap-datepicker/
$( document ).ready(function() {

    String.prototype.format = String.prototype.f = function(){
        var args = arguments;
        return this.replace(/\{(\d+)\}/g, function(m,n){
            return args[n] ? args[n] : m;
        });
    };


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

    $( ".nav-sidebar a" ).click(function() {
        console.log();
        var tub_num = $(this).attr('href')[1];
        $('#counters-tabs-'+tub_num).empty();
        //$('#kv_num').empty();
        $("div.save_form#{0} > H1".f(tub_num)).empty();
        //$('div.save_form#'+tub_num+' > H1'.f(tub_num)).empty();
    });


    $('.kv_button').click(function () {
        var index = $(this).parent().attr("id").toString();
        //var street_number = $('li.active > a').text().split(', ');
        var apartment = $(this).val();
        var account = $(this).find('span').text();
        //console.log(apartment, "div.save_form#"+index, account);
        $("div.save_form#{0} > H1".f(index)).html("Квартира "+apartment);
        $("div.save_form#{0} > div > div".f(index)).load("/api_v0/get_account_data/", {account:account, doing:'get'},
            function (responseText, textStatus, XMLHttpRequest) {
            if (textStatus == "success") {
                 //console.log('all good');
            }
            if (textStatus == "error") {
                 //console.log('not good');
            }
          }
        );
    });

    var LogOut = function () {
        $.ajax({
            url: "/management/user/",
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (msg) {
            window.location = msg['ok'];
        });
    };

    $('#log_out').click(function (e) {
        e.preventDefault();
        LogOut();
    });

    $(".date_select").datepicker({
        format: "mm.yyyy",
        startView: 1,
        minViewMode: 1,
        language: "ru",
        autoclose: true,
        todayHighlight: true,
        todayBtn: "linked",
        toggleActive: true
    });
});
