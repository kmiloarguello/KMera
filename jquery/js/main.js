// JS
/*  global $ */
$(function () {
    $('h1').addClass('danger');
    setTimeout(function (){
        $('h1').removeClass('danger');
    },1500)
});
