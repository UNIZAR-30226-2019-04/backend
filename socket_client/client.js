
const
	io=require("socket.io-client"),
	ioClient = io.connect("http://34.90.77.95:5000");

ioClient.emit("mensaje",{mensaje: "hola"});
