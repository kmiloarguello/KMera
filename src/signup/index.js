/* SIGN UP */
var page = require("page");
var empty = require("empty-element");
var template = require("./template.js");
var title = require("title");

page('/signup',function(ctx, next) {
    title('KMera - Signup');
    var main = document.getElementById('main-container');
    empty(main).appendChild(template);
})