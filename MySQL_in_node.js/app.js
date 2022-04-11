const express = require('express')
const app = express()
const apiRouter = require('./routers/api')
const requestlog = (req, res, next) => {
    console.log('reqested url', req.originalUrl, '-', new Date())
    next()
}
var moment = require('moment');
require('moment-timezone');
moment.tz.setDefault("Asia/Seoul");
require('dotenv').config()

app.set('view engine', 'ejs')
app.set('views', './views')

app.use(express.urlencoded({ extended: false }))
app.use(express.json())
app.use(requestlog)

app.use('/api', [apiRouter])

app.get('/', (req, res) => {
    res.json({ msg: 'hi' })
})
console.log(process.env.PORT)
app.listen(process.env.PORT, (req, res) => {
    console.log(`${process.env.PORT}로 연결되었다.`)
    console.log(moment().format('YYYY-MM-DD HH:mm:ss'));
})