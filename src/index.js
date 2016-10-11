
// CODIGO DEL CLIENTE
var page = require("page"); 

var main = document.getElementById('main-container');

page('/', function(ctx, next){
    main.innerHTML = 'home <a href="/signup">Signup</a>'; // Home
})

page('/signup',function(ctx, next) {
    main.innerHTML = 'signup 2<a href="/">Home</a>'; // Signup
})

page();