var zerorpc = require('zerorpc');
var fs = require('fs');
var http = require('http');

// Open the zeroRPC connection to workbench
var client = new zerorpc.Client();
client.connect('tcp://127.0.0.1:4242');

// What functions are available
client.invoke('_zerorpc_list', function(error, res, more) {
    console.log(res);
});

http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'application/json'});

    // Load a file, store it in workbench and ask workbench to generate a view on it
    fs.readFile('../test_files/pe_files/baddy._exe_', function (err, data) {
        if (err) throw err;
        client.invoke('batch_work_request','view_customer', function(err, result, more) {
            if (err) throw err;
            res.end(JSON.stringify(result, null, 4));
        });
    });
}).listen(1337, '127.0.0.1');

console.log('Server running at http://127.0.0.1:1337/');
