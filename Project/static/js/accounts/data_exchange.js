$(document).ready(function() {
    "use strict";

    var msgHandler = function (msg) {
        if (msg['ok']){
            //console.log(msg['ok']);
            $('.alert').hide();
            if (msg['el_success']){
                var block_el = $('.well#'+msg['el_success']['cid']);
                block_el.find('#counter_date').text(msg['date']+' г.');
                block_el.find('#counter_data1').text(msg['data1']+' кВт/ч');
                block_el.find('#counter_diff1').html('<b>'+msg['diff1']+'</b> кВт/ч');
                if (msg['data2']){
                    block_el.find('#counter_data2').text(msg['data2']+' кВт/ч');
                    block_el.find('#counter_diff2').html('<b>'+msg['diff2']+'</b> кВт/ч');
                }
                block_el.find(".el_success_span").text(msg['el_success']['message']);
                block_el.find('.alert-success').show();

            }else if (msg['el_error']){
                //console.log('el_error');
                var block_err_el = $('.well#'+msg['el_error']['cid']);
                block_err_el.find('.el_error_span').text(msg['el_error']['message']);
                block_err_el.find('.alert-danger').show();
            }

            if(msg['wt_success']){
                //console.log(msg['wt_success']['cid']);
                var block = $('.well#'+msg['wt_success']['cid']);
                block.find('#wcounter_date').text(msg['date']+' г.');
                block.find('#wcounter_data').html(msg['data1']+' м<sup>3</sup>');
                block.find('#wcounter_diff').html('<b>'+msg['diff1']+'</b> м<sup>3</sup>');
                var wt_success_alert = $('.wt_success_span_'+msg['wt_success']['cid']).text(msg['wt_success']['message']);
                wt_success_alert.parent().show();
            }else if (msg['wt_error']){
                var wt_error_alert = $('.wt_error_span_'+msg['wt_error']['cid']).text(msg['wt_error']['message']);
                wt_error_alert.parent().show();
            }

            if(msg['gas_success']){
                //console.log(msg['gas_success']['cid']);
                var block_gas = $('.well#'+msg['gas_success']['cid']);
                block_gas.find('#gcounter_date').text(msg['date']+' г.');
                block_gas.find('#gcounter_data').html(msg['data1']+' м<sup>3</sup>');
                block_gas.find('#gcounter_diff').html('<b>'+msg['diff1']+'</b> м<sup>3</sup>');
                var g_success_alert = $('.g_success_span_'+msg['gas_success']['cid']).text(msg['gas_success']['message']);
                g_success_alert.parent().show();
            }else if (msg['gas_error']){
                var g_error_alert = $('.g_error_span_'+msg['gas_error']['cid']).text(msg['gas_error']['message']);
                g_error_alert.parent().show();
            }
        }else
        {
            console.log('error');
        }
    };



    var submitCounterForm = function (btn) {
        //console.log('press2');
        var form_data = new FormData(btn.closest('form')[0]);
        //var account = $('#acc').text();
        //form_data.append('account', account);
        $.ajax({
            url: "/api_v0/save_account_new_data/",
            data: form_data,
            contentType: false,
            processData: false,
            type: 'POST'
        }).done(function (msg) {
            //console.log(msg);
            msgHandler(msg);
        });
    };

    $('.sender_btn').click(function (e) {
        //console.log('press1');
        e.preventDefault();
        submitCounterForm($(this));

    });
});
