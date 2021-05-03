/*
  This is an example of a remote process client
  that interacts with a valid AI Service.

  Concretely, this is how Teacher Moment's DCSS
  application server will interact with third
  party services.
*/
const {
  performance
} = require('perf_hooks');
const io = require('socket.io-client');
const readline = require('readline');
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: '> '
});

// The developer token
const token = '8070cb2467d22a15dabafd5f5128cacc04af86f1';
const transports = ['websocket'];
const endpoint = process.env.NODE_ENV && process.env.NODE_ENV === 'production'
  ? 'ws://dcss-caa-production.herokuapp.com'
  : 'http://localhost:4000';

const agent = {
  id: 1,
  name: 'Confusion Analysis Agent',
  configuration: {
    source: 'cli'
  }
};

const chat = {
  id: 2
};

const user = {
  id: 4,
  name: 'Remote Process User'
};

const auth = {
  agent,
  chat,
  token,
  user,
};

const options = {
  transports,
  auth
};

console.log('endpoint', endpoint);
console.log('options', options);

const socket = io(endpoint, options);

socket.on('response', ({value, result}) => {
  console.log(result);
  console.log(`The participant's response ${result ? 'did' : 'did not'} sound confused.`);
});

socket.on('interjection', ({message}) => {
  console.log(`Agent says: "${message}"`);
});

rl.prompt();

rl.on('line', (line) => {
  const value = line.trim();
  if (value === 'end') {
    socket.emit('end', auth);
    return;
  }

  // Hit <enter> to execute
  socket.emit('request', {
    value: 'https://teacher-moments-staging.herokuapp.com/api/media/audio/2660/466c0c30-bd69-4a35-9dd3-b04bbdcf02b5/380/0ec33c6c-9102-4206-bc35-d6e06a85fcb7.mp3'
  });
  rl.prompt();
}).on('close', () => {
  console.log('Goodbye!');
  process.exit(0);
});
