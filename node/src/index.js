import express from 'express';

import fileReaderRouter from './router/fileReaderRouter.js';

const app = express();
const PORT = process.env.PORT || 3000;

app.use('/file', fileReaderRouter(express.Router()));

app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
});
