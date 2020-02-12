"use strict";
exports.__esModule = true;
var express = require("express");
var register_1 = require("./register");
var info_1 = require("./info");
var router = express.Router();
exports.router = router;
router.get('/', function (req, res, next) {
    if (req.session.userinfo) {
        res.redirect("/info");
    }
    else {
        res.redirect("/static/register.html");
    }
});
router.use('/register', register_1.register);
router.use('/info', info_1.infoRouter);
//# sourceMappingURL=index.js.map