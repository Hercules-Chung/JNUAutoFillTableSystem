"use strict";
exports.__esModule = true;
var express = require("express");
var session = require("express-session");
var bodyParser = require("body-parser");
var cookieParser = require("cookie-parser");
var path = require("path");
var route_1 = require("./route");
var app = express();
exports.app = app;
app.set('views', path.join(__dirname, '../../views'));
console.log("root directory is ", path.join(__dirname, '../views'));
app.set('view engine', 'jade');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(session({
    secret: "jnuvirustable",
    cookie: { maxAge: 60 * 1000 * 30 },
    resave: true,
    saveUninitialized: false
}));
app.use(route_1.router);
app.use('/static', express.static(path.join(__dirname, '../../public')));
app.use(function (err, req, res, next) {
    console.error(err);
    res.status(500).render('error');
});
//# sourceMappingURL=app.js.map