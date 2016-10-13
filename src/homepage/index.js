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
            url: 'me_Toronto.jpg',
            likes: 1,
            liked: true,
            createAt: new Date()
        },
        {
            user: { 
                username: 'julianaruiz_18',
                avatar: 'https://igcdn-photos-h-a.akamaihd.net/hphotos-ak-xap1/t51.2885-19/s150x150/11208137_960356917356807_1028677243_a.jpg'
            },
            url: 'juliiii.jpg',
            likes: 100000,
            liked: true,
            createAt: new Date().setDate(new Date().getDate() - 10)
        }
    ];
    
    empty(main).appendChild(template(pictures));
})