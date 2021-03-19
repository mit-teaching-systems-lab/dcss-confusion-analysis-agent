let fs;

try {
  // Node 14.x
  fs = require('fs/promises');
} catch (error) {
  // Node 12.x
  fs = require('fs').promises;
}

const util = require('util');
const exec = util.promisify(require('child_process').exec);

async function isConfused(token, url) {
  const { stdout, stderr } = await exec(`python3 ./confusion.py --token ${token} --url ${url}`);
  if (stderr) {
    return stderr;
  }
  console.log(stdout);
  return stdout.toString('utf8') === 'True';
}

const express = require('express');
const SocketIO = require('socket.io');
const PORT = process.env.PORT || 4000;

const files = {
  '/': '/index.html',
};

const app = express();

app.get('*', async (req, res) => {
  let file = files['/'];
  if (files[req.path]) {
    file = files[req.path];
  }
  const contents = await fs.readFile(`${__dirname}${file}`, 'utf8');
  res.send(contents.replace('/***PORT***/', `${PORT}`));
});

const server = app.listen(PORT, () => console.log(`Listening on ${PORT}`));
const io = SocketIO(server);

const cache = {};
const count = 0;

io.on('connection', (socket) => {
  const {
    agent,
    chat,
    token,
    user
  } = socket.handshake.auth;

  socket.join(user.id);

  console.log('Received agent:', agent);
  console.log('Received chat:', chat);
  console.log('Received token:', token);
  console.log('Received user:', user);
  console.log('socket.id', socket.id);

  if (!cache[user.id]) {
    cache[user.id] = {
      agent,
      chat,
      user,
      count,
      rx: [],
      tx: []
    };
    // Only send the welcome message when this is the
    // first time the specific user is connecting.
    //
    // Send the response to the specified private
    // channel for this client socket connection.

    const key = agent.configuration.source === 'web'
      ? '&lt;enter&gt;'
      : '<enter>';

    const message = `Hello, I will analyze your media file. Press the ${key} key to make a remote request using the developer token and mp3 url`;
    io.to(user.id).emit('interjection', { message });
  }

  /*
    THIS IS THE IMPORTANT PART FOR CONSTRUCTING AN AGENT THAT
    TEACHER MOMENTS CAN INTERACT WITH
  */
  socket.on('request', async payload => {
    console.log('request', payload);
    if (!cache[user.id]) {
      // The session has been ended!
      return;
    }

    // "Process" the incoming data
    const result = await isConfused(token, payload.value);

    const response = {
      ...payload,
      result
    };

    // Send the response to the specified private
    // channel for this client socket connection.
    io.to(user.id).emit('response', response);
  });

  socket.on('end', ({ auth, chat, user }) => {
    if (cache[user.id]) {
      io.to(user.id).emit('interjection', {
        message: 'Goodbye!'
      });
      cache[user.id] = null;
    }
  });
  /*
    END
  */
});
