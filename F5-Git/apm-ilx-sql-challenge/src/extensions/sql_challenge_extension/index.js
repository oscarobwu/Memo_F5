// Debug logging control.
// 0 = debug off, 1 = debug level 1, 2 = debug level 2
const debug = 1;
 
// Includes
const f5 = require('f5-nodejs');
const sql = require('mssql');

const config = {
    user: '<sql username>',
    password: '<sql password>',
    server: '<database server host name>', // You can use 'localhost\\instance' to connect to named instance
    database: '<sql database name>',
    options: {
        encrypt: true // Use this if you're on Windows Azure
    }
}
 
const connection = new sql.ConnectionPool(config);
 
// Create a new rpc server for listening to TCL iRule calls.
const ilx = new f5.ILXServer();

// Start listening for ILX::call and ILX::notify events.
ilx.listen();

ilx.addMethod('sql_challenge', function (request, response) {
    connection.connect()
    .then(function () {
        const request = new sql.Request(connection);
        request.execute('[dbo].[GetChallenge]') // <- change the name of this to the stored procedure you want to call
            .then((result) => {
                if (result !== undefined) {
                    const challenge = result.recordset[0]; // only expecting a single row returned, but this code could be changed if you are looking for multiple questions
                    if (debug >= 1) { console.log(`addMethod(): ${challenge.Question} ${challenge.Answer}`); } // <- change these to match the column names of the recordset returned from SQL server
                    response.reply([0, challenge.Question, challenge.Answer]); // Return 0 (success status code) and multiple values
                }
                else {
                    console.log('ERROR: no results.');
                    response.reply([1]); // Return 1 (error status code)
                }
                connection.close();
            })
            .catch((err) => {
                connection.close();
                console.log(`STORED PROC ERROR: ${err}`);
                response.reply([2]); // Return 2 (error status code)
            });
    }).catch((err) => {
        connection.close();
        console.log(`CONNECTION ERROR: ${err}`);
        response.reply([3]); // Return 3 (error status code)
    });
});


