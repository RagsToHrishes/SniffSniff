import styles from './css/Search.module.css'
import Header from './components/Header'
import { useState } from 'react'

export default function Search({ data, category }) {

    const [categorySelect, setCategorySelect] = useState('')
    const [searchQuery, setSearchQuery] = useState('')
    const [courseSelect, setCourseSelect] = useState('')

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (e.target.value != ''){            
            const data = {
                course: courseSelect,
                discord: e.target[0].value
            }

            const JSONdata = JSON.stringify(data);
            const endpoint = '/api/updatediscord';

            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSONdata
            }

            await fetch(endpoint, options).catch(err => console.log(err))
        }
    }

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
                                <div key={index} onClick={() => item == categorySelect ? setCategorySelect('') : setCategorySelect(item)} className={categorySelect == item ? styles.orange : styles.nothing}>
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
                                <div key={index} className={styles.singleCourse} onClick={() => item[0] == courseSelect ? setCourseSelect('') : setCourseSelect(item[0])}>
                                    <p className = {courseSelect == item[0] ? styles.courseClick : styles.nothing}>{item[0]}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div>
                        <h1>Channels</h1>
                        <p>Select and join the right class channels</p>
                        {courseSelect && data.filter(values => values[0] == courseSelect).map((item, index) => (
                            <div key={index}>
                                {!item[3] && <div className={styles.noChannels}>
                                    <h3>It seems like there are no channels for the class you are searching for...</h3>
                                    <h2>Be the one to create it!</h2>
                                    <p>Once you create a channel, add it below, so other classmates can sniff you out too!</p>
                                    <div className={styles.channelButtons}>
                                        <form onSubmit={handleSubmit}>
                                            <input type="text" placeholder="enter discord channel..."/>
                                            <input type="text" placeholder="enter slack link..."/>
                                            <button type="submit">Submit</button>
                                        </form>
                                    </div>
                                    <img src="./channelavatar.png"/>
                                </div>}
                                {item[3] && <div className={styles.hasChannels}>
                                    <div className={styles.discordBox}>
                                        <img src='./discord.png'/>
                                        <a href={item[3]} target="_blank" rel="noopener noreferrer">Join Discord Link</a>
                                    </div>
                                    <div className={styles.slackBox}>
                                        <img src='./slack.png' />
                                        <a>Join Slack Link</a>
                                    </div>
                                </div>
                                }
                            </div>
                        ))}
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
    const data = courseInfo[0].sort()
    const category = Array.from(courseInfo[1])
    category.sort()

    return {
      props: {
        data,
        category
      },
    };
  };