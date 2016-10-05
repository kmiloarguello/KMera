// JS
/*  global $ */
$(function () {
    //metodo getter
    var a = $('<a>', {
        href: 'http://camiloarguello.co',
        target: '_blank',
        html: 'Ir a CamiloArguello.Co'
    })
    $('#app-body').append(a);
    //metodo setter
    a.attr('href','http://google.ca')
    a.html("go ahead")
    
    
});
