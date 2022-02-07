import { exec as ex } from 'child_process';
import { promisify } from 'util';
import multer from 'multer';
// const multer  = require('multer')
const upload = multer({ dest: 'uploads/' })

const exec = promisify(ex);

const fileReader = router => {
    router.post('/', async (req, res) => {

        // const {out, err} = await exec(`touch ${}`);
        const {out, err} = await exec('echo Hello')

        console.log(out);
        console.error(err);

        return res.json({
            'message': 'Hello, World! eiei'
        });
    });


    router.post('/upload', upload.single('photos'), async (req, res, next) => {
          // req.files is array of `photos` files
          // req.body will contain the text fields, if there were any
          return res.json({
              'message': 'Upload completed'
          });
    });

    return router;
};

export default fileReader;
