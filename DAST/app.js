const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
const port = 3000;

// Setup an in-memory database for testing SQLi
const db = new sqlite3.Database(':memory:');
db.serialize(() => {
  db.run("CREATE TABLE users (id INT, username TEXT, password TEXT)");
  db.run("INSERT INTO users VALUES (1, 'admin', 'P@ssw0rd123')");
});

// VULNERABILITY: Security Misconfiguration
// Exposing internal server information via custom headers
app.use((req, res, next) => {
  res.setHeader("X-Debug-Mode", "Enabled");
  res.setHeader("Server-Backend-Version", "1.0.4-beta");
  next();
});

// VULNERABILITY: Reflected Cross-Site Scripting (XSS)
// User input is rendered directly into the HTML without sanitization
app.get('/', (req, res) => {
  const name = req.query.name || 'Guest';
  res.send(`<h1>Welcome, ${name}</h1><p>Search for a user by ID at /user?id=1</p>`);
});

// VULNERABILITY: SQL Injection (SQLi)
// Directly concatenating user input into the SQL query string
app.get('/user', (req, res) => {
  const userId = req.query.id;
  const query = `SELECT username FROM users WHERE id = ${userId}`;
  
  db.get(query, (err, row) => {
    if (err) {
      // VULNERABILITY: Information Exposure through Error Messages
      // Sending raw database errors to the client
      res.status(500).send("Database Error: " + err.message);
    } else {
      res.json(row || { error: "User not found" });
    }
  });
});

// VULNERABILITY: Sensitive Data Exposure
// Hardcoded credentials and secrets exposed via an unprotected endpoint
app.get('/debug-config', (req, res) => {
  res.json({
    db_connection: "postgres://admin:super_secret_password@localhost:5432/db",
    api_key: "aiza_test_key_sample_12345",
    environment: "development"
  });
});

app.listen(port, () => {
  console.log(`Vulnerable app listening at http://localhost:${port}`);
});