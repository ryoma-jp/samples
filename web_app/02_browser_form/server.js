'use strict';

const express = require('express');
const bodyParser = require('body-parser');

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
app.use(express.static('./'));

// App: Get
app.get('/', (req, res) => {
	res.send('Hello World');
});

// App: Post
app.use(bodyParser.urlencoded({
	extended: true
}));
app.use(bodyParser.json());
app.post('/', (req, res) => {
	console.log(req.body);
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);

