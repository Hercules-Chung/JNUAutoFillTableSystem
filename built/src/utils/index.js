"use strict";
exports.__esModule = true;
function addDoubleQuotesForValue(value) {
    return "\"" + value + "\"";
}
exports.addDoubleQuotesForValue = addDoubleQuotesForValue;
function buildUpdateQuery(table, columns, values, conditions) {
    var result = "update " + table + " set ";
    columns.forEach(function (col, index, arr) {
        arr[index] = col + "=" + addDoubleQuotesForValue(values[index]);
    });
    result += columns.join(',');
    result += " ";
    result += conditions;
    return result;
}
exports.buildUpdateQuery = buildUpdateQuery;
function buildSelectQuery(table, columns, conditions) {
    var result = "select ";
    if (columns.length == 0) {
        result += "*";
    }
    else {
        result += columns.join(",");
    }
    result += " from ";
    result += table;
    result += " ";
    result += conditions;
    return result;
}
exports.buildSelectQuery = buildSelectQuery;
function buildInsertQuery(table, columns, values) {
    var result = "insert into " + table + " (";
    for (var i = 0; i < columns.length - 1; i++) {
        result += columns[i];
        result += ",";
    }
    result += columns[columns.length - 1];
    result += ") ";
    result += "values (";
    for (var i = 0; i < columns.length - 1; i++) {
        result += "\"";
        result += values[i];
        result += "\"";
        result += ",";
    }
    result += "\"";
    result += values[columns.length - 1];
    result += "\"";
    result += ")";
    return result;
}
exports.buildInsertQuery = buildInsertQuery;
//# sourceMappingURL=index.js.map