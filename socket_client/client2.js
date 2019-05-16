var io = require('socket.io-client');
var socket = io.connect('http://34.90.77.95:5000/mychat', {reconnect: true});

    socket.on('connect', function() {
console.log("conected");
        socket.emit('mensaje', {data: "HOLAAAAAAAA"});
    });
