'use strict';

// Modules
const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const axios = require('axios');

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';
const user_dir_root = 'users';

// Variables
var user_info = 'user_info.json';

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
	var user_dir = path.join(user_dir_root, req.body.name);
	var user_info_file = path.join(__dirname, user_dir, user_info);
	
	// create user directory
	console.log(user_dir);
	console.log(user_info_file);
	console.log(__dirname);
	fs.mkdir(user_dir, {recursive: true}, (err) => {
		if (err) throw err;
	});

	// create user information file after user directory is created
	var ms = 1;
	var count = 0;
	var count_th = 100;	// timeout threshold: 100ms
	var interval_id = setInterval(function () {
		if (fs.existsSync(user_dir)) {
			clearInterval(interval_id);
			fs.writeFile(user_info_file, JSON.stringify(req.body, null, '\t'), (err)=> {
				if (err) throw err;
			});
			console.log('[INFO] save user_info done');

			// back to top page after submit
			const options = {
				method: 'GET',
				url: `http://${HOST}:${PORT}`,
			};
			axios.get(`http://${HOST}:${PORT}`)
				.then(function (response) {
//					console.log(response.data);	// for debug
					res.send(response.data);
				});
		} else {
			count++;
			if (count > count_th) {
				// timeout
				console.log('[ERROR] Create directory failed: ' + user_dir);
				throw Error('[ERROR] Timeout');
			}
		}
	}, ms);
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);

