$( document ).ready(function() {

    var ID = function () {
    // Math.random should be unique because of its seeding algorithm.
    // Convert it to base 36 (numbers + letters), and grab the first 9 characters
    // after the decimal.
    return '_' + Math.random().toString(36).substr(2, 9);
    };


    var submitUploadForm = function (id) {
        var form_data = new FormData($('#file-upload-form')[0]);
        form_data.append('id', id);
        //console.log(form_data);
        $.ajax({
            url: "/api_v0/upload/",
            data: form_data,
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (msg) {
            //console.log(msg);
            if (msg['file_load'] === 'ok'){
                //setTimeout(progressbarUpdate(0);
                progressbarUpdate(id, 0);
            }
            else
            {
                console.log(msg);
            }
        });
    };

    var submitDownloadForm = function (id) {
        var form_data = new FormData($('#file-download-form')[0]);
        //console.log();
        form_data.append('id', id);
        form_data.append('date', $('.date_select').find('input').val());
        //console.log(form_data);
        $.ajax({
            url: "/api_v0/download/",
            data: form_data,
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (msg) {
            //console.log(msg);
            if (msg['file_unload'] === 'ok'){
                //setTimeout(progressbarUpdate(0);
                progressbarUpdate(id, 1);
            }
            else
            {
                console.log(msg);
            }
        });
    };


    var progressbarUpdate = function(id, form_type){
        $.getJSON({
            url:'/api_v0/progressbar_update/',
            data:{
                'percent':0,
                'id':id,
                'status:':'loading'
            }
        }).done(function (data) {
            console.log(data);
            var ProgressBar = NaN;
            if (form_type === 0) {
                ProgressBar = $('.progress-bar#upload')
            } else if (form_type === 1){
                ProgressBar = $('.progress-bar#download')
            }

            if (data['percent'] <= 100 && data['status'] === 'loading') {

                ProgressBar.css(
                'width', data['percent']+'%').attr(
                    'aria-valuenow', data['percent']).text(data['percent']+'%');

                setTimeout(function() {
                    progressbarUpdate(id, form_type);
                }, 500);
                //progressbarUpdate(id);
            }else if (data['status'] === 'done'){
                ProgressBar.css(
                'width', data['percent']+'%').attr(
                    'aria-valuenow', data['percent']).text(data['percent']+'%');
                if (data['url']) {
                    $('#download_link').append('<p><a href=\"'+data['url']+'\">'+data['file_name']+'</a></p>')
                }
            }else{
                console.log(data)
            }

        });



    };

    $('#upload-btn').click(function (e) {
        e.preventDefault();
        $('.progress-bar#upload').css(
                'width', 0+'%').attr(
                    'aria-valuenow', 0).text(0+'%');
        var id = ID();
        submitUploadForm(id);



    });

    $('#Download-Button').click(function (e) {
        e.preventDefault();
        $('.progress-bar#download').css(
                'width', 0+'%').attr(
                    'aria-valuenow', 0).text(0+'%');
        var id = ID();
        submitDownloadForm(id);



    });





});