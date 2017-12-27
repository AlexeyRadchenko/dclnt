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
});