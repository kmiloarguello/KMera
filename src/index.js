
// CODIGO DEL CLIENTE
var page = require("page"); 

var main = document.getElementById('main-container');

page('/', function(ctx, next){
    main.innerHTML = 'home'; // Home
})

page('/signup',function(ctx, next) {
    main.innerHTML = 'signup'; // Signup
})

page();