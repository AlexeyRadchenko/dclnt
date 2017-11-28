$( document ).ready(function() {
    var submitForm = function () {
        var form_data = new FormData($('#file-upload-form')[0]);
        //console.log(form_data);
        $.ajax({
            url: "/",
            data: form_data,
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (msg) {
            console.log(msg);
            //setTimeout(progressbarUpdate(0);
            //progressbarUpdate(0);
        });
    };

    var progressbarUpdate = function(progress){
        $.getJSON({
            url:'/progressbar_update/',
            data:{'state':progress}
        }).done(function (data) {
            console.log(data);
            if (data['data_progress'] <= 100) {
                $('.progress-bar').css(
                'width', data['data_progress']+'%').attr(
                    'aria-valuenow', data['data_progress']).text(data['data_progress']+'%');
                setTimeout(function() {
                    progressbarUpdate(data['data_progress']);
                }, 10);
                //progressbarUpdate(data['data_progress']);
            }

        });



    };

    $('#upload-btn').click(function (e) {
        e.preventDefault();
        submitForm();



    });

});