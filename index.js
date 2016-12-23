'use strict';

let conf;

try {
  conf = require('./pushbullet.conf.json');
} catch(err) {
  console.log(err);
  console.error('A valid `./conf.json` file must exist');
  process.exit(1);
}

const {TOKEN, CHANNEL, PORT} = conf;

function sendPush({title, body}) {
  const req = {
    host: 'api.pushbullet.com',
    path: '/v2/pushes',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Access-Token': TOKEN
    }
  };

  const r = require('https').request(req);
  r.write(JSON.stringify({
    channel_tag: CHANNEL,
    type: 'note',
    title,
    body
  }));

  r.end();
}

require('http').createServer((req, res) => {
  if (req.url !== '/') {
    res.writeHead(404);
    res.end();
    return;
  }

  let body = '';
  req.on('data', data => body += data);
  req.on('end', function () {
    sendPush(JSON.parse(body));
  });

  res.end();
}).listen(process.env.PORT || PORT || 9998);
