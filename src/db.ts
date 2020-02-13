import * as mysql from 'mysql';
import {promisify} from 'util';
const connection = mysql.createConnection({
    host: '*****',
    user: '******',
    password: '******',
    database: 'JNUSTU'
});

connection.connect((err,result)=>{
    if(err) console.log("Fail to connect database");
    else console.log(result);
});

export {
    connection
}