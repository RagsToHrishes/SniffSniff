import styles from './css/Search.module.css'
import Header from './components/Header'
import { useState } from 'react'

export default function Search({ data, category }) {

    const [categorySelect, setCategorySelect] = useState('')
    const [searchQuery, setSearchQuery] = useState('')

    return (
        <div>
            <Header />
            <div className={styles.search}>
                <div className={styles.searchButton}>
                    <img src="/search.png" width="20px" height="20px"/>
                    <input type="text" placeholder="search class here..." onChange={e => setSearchQuery(e.target.value)}/>
                </div>
                <div className={styles.results}>
                    <div>
                        <h1>Category</h1>
                        <p>Scroll and click your class category</p>
                        <div className={styles.category}>
                            {category && category.map((item, index) => (
                                <div key={index} onClick={() => setCategorySelect(item)}>
                                    <p>{item}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div>
                        <h1>Courses</h1>
                        <p>Scroll, find, and click your class number</p>
                        <div className={styles.courses}>
                            {data && data.filter(values => values[2].includes(categorySelect)).filter(values => values[0].toLowerCase().includes(searchQuery.toLowerCase()) || values[1].toLowerCase().includes(searchQuery.toLowerCase())).map((item, index) => (
                                <div key={index} className={styles.singleCourse}>
                                    <p>{item[0]}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div>
                        <h1>Channels</h1>
                        <p>Select and join the right class channels</p>
                    </div>
                </div>
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

        console.log(courses)

        const coursesList = []
        const category = new Set()

        for (var i = 0; i < courses.rows.length; i++) {
            coursesList.push(
                [courses.rows[i].course,
                courses.rows[i].title,
                courses.rows[i].subjectArea,
                courses.rows[i].discord]
            )
            category.add(courses.rows[i].subjectArea)
        }

        return [coursesList, category]
    }

    const courseInfo = await getCourses();
    const data = courseInfo[0]
    const category = Array.from(courseInfo[1])
    category.sort()

    return {
      props: {
        data,
        category
      },
    };
  };