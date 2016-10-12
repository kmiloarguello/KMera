/* SIGN UP */
var page = require("page");
var empty = require("empty-element");
var template = require("./template.js")

page('/signup',function(ctx, next) {// Signup
    var main = document.getElementById('main-container');
    empty(main).appendChild(template);
})