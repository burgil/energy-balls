import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();
app.use(express.json());
const port = 80;
// app.use('/files', express.static(path.join(__dirname, '..'))); // This is where the files were stored locally.
app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname, '/index.html'));
});
app.listen(port);
console.log('Server started at http://localhost:' + port);
