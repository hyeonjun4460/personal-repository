const express = require('express')
const db = require('../models/index')
router = express.Router()
db.connect()
const moment = require('moment')
const { type } = require('express/lib/response')
require('moment-timezone')

router.get('/', (req, res) => {
    console.log('welcome to /api')
    db.query('SELECT * FROM topic', function (error, results, fields) {
        if (error) {
            throw error
        }
        res.render('api', { results })
    });
})

router.get('/create', (req, res) => {
    db.query(`SELECT * FROM author`, (error, results) => {
        if (error) console.log(error)
        res.render('create', { results })
    })
})

router.post('/create', (req, res) => {
    const { title, description, author } = req.body
    const date = moment().format('YYYY-MM-DD HH:mm:ss')
    console.log(date)
    console.log(author)

    db.query(`INSERT INTO topic (title, description, created, author_id) VALUES (?, ?, ?, ?)`, [title, description, date, 1], (error, results, fields) => {
        if (error) {
            throw error
        }
        res.json({ msg: '성공' })
    })
})


router.get('/:id', (req, res) => {
    const { id } = req.params
    db.query(`SELECT title, description, created, author.name, author.profile, topic.id FROM topic LEFT JOIN author ON author_id=author.id WHERE topic.id=?`, [id], (error, results, fields) => { // ?, [id] = ?뒤에 주어진 parameter로 ?를 치환. (해킹을 자동으로 막아주는 문법이라고 함)
        if (error) {
            console.log(error)
        }
        db.query(`SELECT * FROM author`, (error, results2) => {
            if (error) console.log(error)
            res.render('detail', { results, results2 })
        })

    })
})

router.patch('/:id', (req, res) => {
    const { id } = req.params
    const { title, description, author } = req.body
    db.query(`UPDATE topic SET description=?, title=?, author_id=? WHERE id=?`, [description, title, author, id], (error, results, fields) => {
        if (error) console.log(error)
        res.json({ msg: '성공' })
    })
})

router.delete('/:id', (req, res) => {
    const { id } = req.params
    db.query(`DELETE FROM topic WHERE id=?`, [id], (error, results, fields) => {
        if (error) console.log(error)
        res.json({ msg: '삭제' })
    })
})


module.exports = router