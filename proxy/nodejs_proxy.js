var http = require('http')
var net = require('net')
var url = require('url')

function on_request(req, res) {
    var urlparse = url.parse(req.url);
    
    var options = {
        host : urlparse.host,
        port : urlparse.port || 80,
        path : urlparse.path ,
        method : req.method ,
        headers : req.headers 
    };
    
    var forwardreq = http.request(options, function(backres) {
        res.writeHead(backres.statusCode, backres.headers);
        backres.pipe(res);        
    });
    // for posible POST content
    req.pipe(forwardreq);
};

function on_connect(req, cltsock) {
    var srvurl = url.parse('http://' + req.url)
    var srvsock = net.connect(srvurl.port, srvurl.hostname, ()=> {
       cltsock.write('HTTP/1.1 200 Connection Established\r\n\r\n');
       srvsock.pipe(cltsock);
       cltsock.pipe(srvsock);
    });
};

http.createServer().on('request', on_request).on('connect', on_connect).listen(8000, '0.0.0.0')