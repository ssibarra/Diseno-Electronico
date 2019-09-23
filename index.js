const express = require("express");
const bodyParser = require("body-parser");
const gpsConv = require("gpstime");
const app = express();
const mysql = require("mysql");
const path = require("path");

var connection = mysql.createConnection({
  host: "rdsdiseno.c37pqurbdepy.us-east-1.rds.amazonaws.com",
  user: "admin",
  password: "diseno1234",
  database: "RDS_diseno",
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
app.get("/", function(req, res) {
  res.sendFile(path.join(__dirname + "/public/index.htm"));
});
app.get("/query", (req, res) => {
  if (connection) {
    connection.query(
      "SELECT * FROM RDS_diseno.Arriving_Data ORDER BY idpacket DESC limit 1;",
      (err, rows) => {
        console.log(rows);
        if (err) {
          throw err;
        } else {
          let nWeeks, time, lng, lat;
          lat = rows[0].lat;
          lat = `${lat[0]}${lat[1]}${lat[2]}.${lat[3]}${lat[4]}${lat[5]}${
            lat[6]
          }${lat[7]}`;
          lng = rows[0].lng;
          lng = `${lng[0]}${lng[1]}${lng[2]}${lng[3]}.${lng[4]}${lng[5]}${
            lng[6]
          }${lng[7]}${lng[8]}`;
          // newMsg = newMsg.split("");

          // nWeeks = `${newMsg[6]}${newMsg[7]}${newMsg[8]}${newMsg[9]}`;
          // time = `${newMsg[11]}${newMsg[12]}${newMsg[13]}${newMsg[14]}${
          //   newMsg[15]
          // }`;

          // lat = `${newMsg[16]}${newMsg[17]}${newMsg[18]}.${newMsg[19]}${
          //   newMsg[20]
          // }${newMsg[21]}${newMsg[22]}${newMsg[23]}`;
          // lon = `${newMsg[24]}${newMsg[25]}${newMsg[26]}${newMsg[27]}.${
          //   newMsg[28]
          // }${newMsg[29]}${newMsg[30]}${newMsg[31]}${newMsg[32]}`;
          // syrusID = `${newMsg[45]}${newMsg[46]}${newMsg[47]}${newMsg[48]}${
          //   newMsg[49]
          // }${newMsg[50]}${newMsg[51]}${newMsg[52]}`;

          // let dateConvert = gpsConv.wnTowToUtcTimestamp(
          //   parseInt(nWeeks, 10),
          //   parseInt(time, 10)
          // );

          // let newDate = `${dateConvert.getUTCDate() +
          //   1}-${dateConvert.getUTCMonth() +
          //   1}-${dateConvert.getUTCFullYear()} `;
          // let newTime = `${dateConvert.getUTCHours() -
          //   5}:${dateConvert.getMinutes()}`;

          data = {
            // id: null,
            // date: newDate,
            // time: newTime,
            lon: lng,
            lat: lat
            // syrusID: syrusID
          };

          res.json(data);
        }
      }
    );
  }
});

app.listen(7000, () => {
  console.log("Server on");
});
