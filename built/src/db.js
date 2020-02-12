"use strict";
exports.__esModule = true;
var mysql = require("mysql");
var connection = mysql.createConnection({
    host: 'aliyun.linjiaqin.xyz',
    user: 'root',
    password: 'toor',
    database: 'JNUSTU'
});
exports.connection = connection;
connection.connect(function (err, result) {
    if (err)
        console.log("Fail to connect database");
    else
        console.log(result);
});
//# sourceMappingURL=db.js.map