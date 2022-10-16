import styles from '../css/Header.module.css'

export default function Header() {
    return (
        <div>
            <div className={styles.header}>
                <img  src='/icon.png'/>
                <div className={styles.options}>
                    <p>Search</p>
                    <p>Courses</p>
                </div>
            </div>
        </div>
    )
}