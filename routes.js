const path = require('path')
const Promise = require('bluebird');
const cp = Promise.promisifyAll(require('child_process'));

module.exports = (app) => {
    app.get('/', (req, res) => {
        res.sendFile(path.join(__dirname, 'index.html'))
    })
    app.post('/', (req, res) => {
        cp.execAsync(`python3 parse.py ${req.body.url}`)
            .then((data) => {
                res.send(data)
            })
            .catch((err) => {
                console.log(err)
            })
    })
}