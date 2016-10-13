/* HOMEPAGE */
var page = require("page");
var empty = require("empty-element");
var template = require("./template.js");
var title = require("title");
var request = require("superagent");
var header = require("../header");
var axios = require("axios");

page('/', header , asyncload ,function(ctx, next) {
    title('KMera');
    var main = document.getElementById('main-container');
    
    empty(main).appendChild(template(ctx.pictures));
})

function loadPictures(ctx, next){
    request
        .get('/api/pictures')
        .end(function(err, res){
          if(err) return console.log('error');
          ctx.pictures = res.body;
          next();
    });
}

function loadPicturesAxios(ctx, next){
    axios
        .get('/api/pictures')
        .then(function(res){
          ctx.pictures = res.data;
          var pic = ctx.pictures[0];
          return axios.get(`/api/pictures/${pic.id}`)
        })
        .then(function(res){
              ctx.pictures = res.data;
              next();
        })
        .catch( function(err){
            console.log(err);
        })
}

function loadPicturesFetch(ctx, next){
    fetch('/api/pictures')
        .then( function (res){ return res.json(); })
        .then( function (pictures){ 
            ctx.pictures = pictures;
            next(); 
        })
        .catch(function(err){
            console.log(err)
        })
}

async function asyncload(ctx,next){
    try{
        ctx.pictures  = await fetch('/api/pictures').then(res => res.json());
        next();
    }
    catch(error){
        return console.log(error);
    }
}