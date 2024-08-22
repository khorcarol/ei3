const express = require('express');
const app = express();
const cors = require('cors');
const db = require("./db");
const corsOptions = {
    origin: ["http://localhost:5173"],
};

app.use(cors(corsOptions));

app.get("/data/:sensor_id", (req, res) => {
  const sensor_id = req.params.sensor_id;
  const selectQuery = `
  SELECT * FROM Raw_data WHERE sensor_id = ?
`;
  db.all(selectQuery, [sensor_id], (err, rows) => {
    if (err) {
      console.error("Error fetching data:", err.message);
    } else {
      res.json({"data": rows});
    }
  });

});


const port = 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});