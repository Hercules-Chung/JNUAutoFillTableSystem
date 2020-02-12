"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
var express = require("express");
var request = require("request-promise-native");
var des_1 = require("../utils/des");
var db_1 = require("../db");
var config_1 = require("../config");
var utils_1 = require("../utils");
var register = express.Router();
exports.register = register;
function queryAsync(sql) {
    return new Promise(function (resolve, reject) {
        db_1.connection.query(sql, function (err, result) {
            if (err)
                reject(err);
            else {
                resolve(result);
            }
        });
    });
}
function checkIfUserExist(req) {
    return __awaiter(this, void 0, void 0, function () {
        var exist, sql, result;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    exist = false;
                    sql = utils_1.buildSelectQuery("LoginData", ['user'], "where user=" + utils_1.addDoubleQuotesForValue(req.body.stuNum));
                    console.log(sql);
                    return [4, queryAsync(sql)];
                case 1:
                    result = _a.sent();
                    if (result.length > 0) {
                        exist = true;
                    }
                    return [2, exist];
            }
        });
    });
}
function checkIfPasswordAndEmailChange(req) {
    return __awaiter(this, void 0, void 0, function () {
        var change, userToBeCheck, sql, result;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    change = false;
                    userToBeCheck = {
                        'user': req.body.stuNum,
                        'password': req.body.passkey
                    };
                    sql = utils_1.buildSelectQuery("LoginData", ['user', 'password', 'Email'], "where user=" + utils_1.addDoubleQuotesForValue(req.body.stuNum)
                        + " and password=" + utils_1.addDoubleQuotesForValue(req.body.passkey)
                        + " and Email=" + utils_1.addDoubleQuotesForValue(req.body.email));
                    console.log(sql);
                    return [4, queryAsync(sql)];
                case 1:
                    result = _a.sent();
                    if (result.length > 0) {
                        change = true;
                    }
                    return [2, change];
            }
        });
    });
}
function loginToJNUBackend(req) {
    return __awaiter(this, void 0, void 0, function () {
        var ReqForAuth, cookieJar;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    ReqForAuth = {
                        uri: config_1.LOGINURL,
                        headers: {
                            "User-Agent": config_1.ua
                        }
                    };
                    cookieJar = request.jar();
                    ReqForAuth['jar'] = cookieJar;
                    return [4, request(ReqForAuth).then(function (html) {
                            var relt = new RegExp(/id="lt" name="lt" value="(.*?)"/);
                            var reexe = new RegExp(/name="execution" value="(.*?)"/);
                            var lt = html.match(relt)[1];
                            var exe = html.match(reexe)[1];
                            var rsa = des_1.strEnc(req.body.stuNum + req.body.passkey + lt, '1', '2', '3');
                            var loginData = {
                                'rsa': rsa,
                                'ul': req.body.stuNum.length,
                                'pl': req.body.passkey.length,
                                'lt': lt,
                                'execution': exe,
                                '_eventId': 'submit'
                            };
                            return loginData;
                        })
                            .then(function (loginData) {
                            ReqForAuth['method'] = 'POST';
                            ReqForAuth['form'] = loginData;
                            ReqForAuth['simple'] = false;
                            ReqForAuth['resolveWithFullResponse'] = true;
                            return request(ReqForAuth);
                        })
                            .then(function (html) {
                            return html.body.length == 0;
                        })];
                case 1: return [2, _a.sent()];
            }
        });
    });
}
function updatePasswordAndEmail(req) {
    var query = utils_1.buildUpdateQuery("LoginData", ["password", "Email"], [req.body.passkey, req.body.email], "where user=" + utils_1.addDoubleQuotesForValue(req.body.user));
    db_1.connection.query(query, function (err, result, fields) {
        if (err)
            throw err;
    });
}
function addUserToDatabase(req) {
    var query = utils_1.buildInsertQuery("LoginData", ["user", "password", "Email"], [req.body.stuNum, req.body.passkey, req.body.email]);
    db_1.connection.query(query, function (err, result, fields) {
        if (err)
            throw err;
        console.log("addUsreToDatabase", result);
    });
}
register.post('/', function (req, res, next) { return __awaiter(void 0, void 0, void 0, function () {
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4, loginToJNUBackend(req)];
            case 1:
                if (!_a.sent()) return [3, 6];
                req.session.userinfo = req.body.stuNum;
                return [4, checkIfUserExist(req)];
            case 2:
                if (!_a.sent()) return [3, 4];
                return [4, checkIfPasswordAndEmailChange(req)];
            case 3:
                if (_a.sent()) {
                    updatePasswordAndEmail(req);
                }
                res.redirect("/info");
                return [3, 5];
            case 4:
                addUserToDatabase(req);
                res.redirect("/info/infofill");
                _a.label = 5;
            case 5: return [3, 7];
            case 6:
                res.status(401).send("登录失败，<a href=\"" + "/static/register.html" + "\">重新输入</a>");
                _a.label = 7;
            case 7: return [2];
        }
    });
}); });
//# sourceMappingURL=register.js.map