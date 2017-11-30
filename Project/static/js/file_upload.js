$( document ).ready(function() {

    var ID = function () {
    // Math.random should be unique because of its seeding algorithm.
    // Convert it to base 36 (numbers + letters), and grab the first 9 characters
    // after the decimal.
    return '_' + Math.random().toString(36).substr(2, 9);
    };


    var submitForm = function (id) {
        var form_data = new FormData($('#file-upload-form')[0]);
        form_data.append('id', id);
        //console.log(form_data);
        $.ajax({
            url: "/",
            data: form_data,
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (msg) {
            console.log(msg);
            if (msg['file_load'] === 'ok'){
                //setTimeout(progressbarUpdate(0);
                progressbarUpdate(id);
            }
        });
    };


    var progressbarUpdate = function(id){
        $.getJSON({
            url:'/progressbar_update/',
            data:{
                'percent':0,
                'id':id,
                'status:':'loading'
            }
        }).done(function (data) {
            console.log(data);
            if (data['percent'] <= 100 && data['status'] === 'loading') {
                $('.progress-bar').css(
                'width', data['percent']+'%').attr(
                    'aria-valuenow', data['percent']).text(data['percent']+'%');
                /*
                setTimeout(function() {
                    progressbarUpdate(data['percent']);
                }, 10);*/
                progressbarUpdate(id);
            }

        });



    };

    $('#upload-btn').click(function (e) {
        e.preventDefault();
        var id = ID()
        submitForm(id);



    });

});