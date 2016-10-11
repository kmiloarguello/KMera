var express = require("express"); //busca dentro de node_modules -> Express y trae main

var app = express();

app.get('/', function (req, res){
    res.send('Hola Camilo');
})
// Create localhost server
// app.listen(3000, function (err){
//     if(err) return console.log("Huubo error"), process.exit(1);
    
//     console.log('Server on 3000')
//})


//Create server on cloud 9
app.listen(process.env.PORT, process.env.IP);
