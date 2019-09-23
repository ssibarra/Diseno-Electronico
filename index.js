const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const mysql = require("mysql");
const path = require("path");

var connection = mysql.createConnection({
  host: "desingrds.ci0brdruazre.us-east-1.rds.amazonaws.com",
  user: "Administrator",
  password: "Administrator",
  database: "desingdata",
  port: 3306
});
connection.connect(function(err) {
  if (err) {
    console.error("error connecting: " + err.stack);
    return;
  }
  console.log("connected as id " + connection.threadId);
});

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static("public"));
app.get("/realtime", (req, res) => {
  if (connection) {
    connection.query(
      "SELECT * FROM gpsdata ORDER BY id DESC limit 1;",
      (err, rows) => {
        if (err) {
          throw err;
        } else {
          res.json(rows);
        }
      }
    );
  }
});

app.post("/historical", (req, res) => {
  console.log(req.body);
  // if (connection) {
  //   connection.query(
  //     "SELECT * FROM gpsdata ORDER BY id DESC limit 1;",
  //     (err, rows) => {
  //       if (err) {
  //         throw err;
  //       } else {

  //       }
  //     }
  //   );
  // }
   res.json(req.body);
});

app.listen(80, () => {
  console.log("Server on");
});
