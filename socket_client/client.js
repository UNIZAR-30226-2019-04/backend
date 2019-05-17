
const
	io=require("socket.io-client"),
	ioClient = io.connect("http://localhost:5000");

ioClient.on("seq-num",(msg) => console.info(msg));
