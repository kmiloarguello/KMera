var express = require("express"); //busca dentro de node_modules -> Express y trae main
var multer  = require('multer');
var ext = require("file-extension");

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './uploads')
  },
  filename: function (req, file, cb) {
    cb(null, +Date.now() + '.' + ext(file.originalname))
  }
})

var upload = multer({ storage: storage }).single('picture');

var app = express();

app.set('view engine','pug'); //Preprocese vistas y renderize con pug

app.use(express.static('public'));


app.get('/', function (req, res){
    res.render('index', { title: 'KMera' });
})

app.get('/signup', function (req, res){
    res.render('index',{ title: 'KMera - Signup' });
})

app.get('/signin', function (req, res){
    res.render('index', { title: 'KMera - Signin' });
})

app.get('/api/pictures', function (req, res, next) {
    var pictures = [
    {
        user: { 
            username: 'kmiloarguello',
            avatar: 'https://avatars2.githubusercontent.com/u/13356409?v=3&s=466'
        },
        url: 'me_Toronto.jpg',
        likes: 1,
        liked: true,
        createAt: new Date().getTime()
    },
    {
        user: { 
            username: 'julianaruiz_18',
            avatar: 'https://igcdn-photos-h-a.akamaihd.net/hphotos-ak-xap1/t51.2885-19/s150x150/11208137_960356917356807_1028677243_a.jpg'
        },
        url: 'juliiii.jpg',
        likes: 100,
        liked: true,
        createAt: new Date().setDate(new Date().getDate() - 10)
    }
    ];
    
    setTimeout(function(){ res.send(pictures); },2000);
    
});

app.post('/api/pictures', function(req, res){
    upload(req, res, function(err){
        if (err){ 
            return res.send(500, "Error uploading file");
        }
        res.send('File uploaded');
    })
})
// Create localhost server
// app.listen(3000, function (err){
//     if(err) return console.log("Huubo error"), process.exit(1);
    
//     console.log('Server on 3000')
//})

//Create server on cloud 9
app.listen(process.env.PORT, process.env.IP);
