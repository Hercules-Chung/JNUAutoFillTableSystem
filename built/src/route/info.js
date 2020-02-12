"use strict";
exports.__esModule = true;
var express = require("express");
var fs = require("fs");
var path = require("path");
var db_1 = require("../db");
var utils_1 = require("../utils");
var infoRouter = express.Router();
exports.infoRouter = infoRouter;
function checkLogin(req, res, next) {
    if (!req.session.userinfo)
        return res.redirect('/static/register.html');
    else
        next();
}
infoRouter.get('/infochange', checkLogin, function (req, res, next) {
    res.set({ 'Content-type': 'text/html' });
    res.send(fs.readFileSync(path.join(__dirname, "../../../public/infochange.html")).toString());
});
infoRouter.post('/infochange', checkLogin, function (req, res, next) {
    var columns = ["user", "teacherName", "class", "contactName", "contactPhone", "province", "city", "area", "road"];
    var values = [
        req.session.userinfo,
        req.body.teacher,
        req.body["class"],
        req.body.ergenContact,
        req.body.ergenPhone,
        req.body.province,
        req.body.city,
        req.body.area,
        req.body.road
    ];
    var sql = utils_1.buildUpdateQuery("UserInfo", columns, values, "where user=" + utils_1.addDoubleQuotesForValue(req.session.userinfo));
    console.log(sql);
    db_1.connection.query(sql, function (err, result, fields) {
        if (err)
            throw err;
        console.log("post fill", result);
        next(err);
    });
    res.redirect("/info");
});
infoRouter.get('/', checkLogin, function (req, res, next) {
    db_1.connection.query("select LoginData.password,LoginData.Email,UserInfo.* from LoginData left join UserInfo on LoginData.user=UserInfo.user", function (err, result, field) {
        if (err)
            throw Error();
        console.log("query info", result[0]);
        res.render('info', {
            stuNum: result[0]['user'],
            email: result[0]['Email'],
            class_: result[0]['class'],
            teacher: result[0]['teacherName'],
            contactName: result[0]['contactName'],
            contactPhone: result[0]['contactPhone'],
            province: result[0]['province'],
            city: result[0]['city'],
            area: result[0]['area'],
            road: result[0]['road']
        });
    });
});
infoRouter.get('/infofill', checkLogin, function (req, res, next) {
    res.set({ 'Content-type': 'text/html' });
    res.send(fs.readFileSync(path.join(__dirname, "../../../public/infofill.html")).toString());
});
infoRouter.post('/infofill', function (req, res, next) {
    var columns = ["user", "teacherName", "class", "contactName", "contactPhone", "province", "city", "area", "road"];
    var values = [
        req.session.userinfo,
        req.body.teacher,
        req.body["class"],
        req.body.ergenContact,
        req.body.ergenPhone,
        req.body.province,
        req.body.city,
        req.body.area,
        req.body.road
    ];
    db_1.connection.query(utils_1.buildInsertQuery("UserInfo", columns, values), function (err, result, fields) {
        if (err)
            throw err;
        console.log("post fill", result);
        next(err);
    });
    res.redirect("/info");
});
//# sourceMappingURL=info.js.map