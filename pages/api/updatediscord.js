const { Pool } = require("pg");

export default function handler(req, res) {
  if (req.method === "POST") {
    (async () => {
      const pool = new Pool({
        connectionString: process.env.DATABASE_URL,
        ssl: {
          rejectUnauthorized: false,
        },
      });

      const client = await pool.connect();
      
      const course = req.body.course;
      const discord = req.body.discord;
      const query = `UPDATE Course SET discord = '${discord}' WHERE course = '${course}'`;
      const result = await client.query(query);
      const results = { results: result ? result.rows : null };
      res.status(200).json(results);
      client.release();
      
    })().catch((err) => console.log(err.stack));
  }
}