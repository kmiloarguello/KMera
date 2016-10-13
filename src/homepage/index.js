/* HOMEPAGE */
var page = require("page");
var empty = require("empty-element");
var template = require("./template.js");
var title = require("title");

page('/', function(ctx, next) {
    title('KMera');
    var main = document.getElementById('main-container');
    
    var pictures = [
        {
            user: { 
                username: 'kmiloarguello',
                avatar: 'https://avatars2.githubusercontent.com/u/13356409?v=3&s=466'
            },
            url: 'office.jpg',
            likes: 14,
            liked: true
        },
        {
            user: { 
                username: 'kmiloarguello',
                avatar: 'https://avatars2.githubusercontent.com/u/13356409?v=3&s=466'
            },
            url: 'office.jpg',
            likes: 46,
            liked: true
        }
    ];
    
    empty(main).appendChild(template(pictures));
})