const port = 8000;
const express = require('express');
const bodyParser = require('body-parser');
const cors = require("cors")


const Mybuffer1 = Buffer.alloc(100000,encoding='base64');
const Mybuffer2 = Buffer.alloc(100000,encoding='base64');
const Mybuffer3 = Buffer.alloc(100000,encoding='base64');
var bufferStack=[];
var ibuf = 0;


var buffers = [];
buffers.push(Mybuffer1);
buffers.push(Mybuffer2);
buffers.push(Mybuffer3);


const app = express();
app.use(cors());


app.get("/view", (req, res) => {

    if(bufferStack<2){
    res.sendStatus(500);
    }
    var size = buffers[0].readUInt32BE(0);
    headers ={
    'Content-Type': 'image/jpeg',
    'Content-Length': ''+size
    }

    var b= Buffer.alloc(size,encoding='base64')
    buffers[0].copy(b,0,4,size);

    res.writeHead(200,headers);
    res.end(b );

});

app.post("/upload",
 bodyParser.raw({ type: ["image/jpeg"], limit: "5mb" }),
 (req, res) => {
    try{
        const imgBuffer =  Buffer.from(req.body.toString(), 'base64');
        
        buffers[ibuf].writeUInt32BE(imgBuffer.length,0);
        imgBuffer.copy(buffers[ibuf],4,0,imgBuffer.length);
        bufferStack.push(ibuf);
        ibuf++;
        if(bufferStack.length> 2){
            bufferStack.splice(0,1);
            ibuf = 0;
        }
        res.sendStatus(200);
    }catch(error){
        res.sendStatus(500);
    }
 });

app.listen(port, () =>
 console.log(`JpegStreamer backend listening on port ${port}`)
);