import styles from './css/Search.module.css'
import Header from './components/Header'

export default function Search({ data }) {
    return (
        <div>
            <Header />
            <div className={styles.search}>
                <p className={styles.searchh}>Search!</p>
            </div>
        </div>
    )
}

export const getServerSideProps = async () => {
    const { Pool } = require("pg");
  
    async function getCourses() {
        const connectionString = process.env.DATABASE_URL;
        const pool = new Pool({
            connectionString,
            application_name: "$ docs_simplecrud_node-postgres",
        });
    
        const client = await pool.connect();

        const courses = await client.query("SELECT * FROM Course");

        client.release();

        const dict = {}
        for (var i = 0; i < courses.rows.length; i++) {
            dict[courses.rows[i].id] = {
                "course": courses.rows[i].course,
                "title": courses.rows[i].title,
                "subjectArea": courses.rows[i].subjectArea,
                "discord": courses.rows[i].discord
            }
        }

        return dict
    }

    const data = await getCourses();
  
    return {
      props: {
        data
      },
    };
  };