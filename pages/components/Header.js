import styles from '../css/Header.module.css'
import Link from 'next/link'

export default function Header() {
    return (
        <div>
            <div className={styles.header}>
                <Link href="/">
                    <a>
                        <img  src='/icon.png'/>
                    </a>
                </Link>
                <div className={styles.options}>
                    <Link href="/">
                        <a>
                            <p>Home</p>
                        </a>
                    </Link>
                    <Link href="/search">
                        <a>
                            <p>Courses</p>
                        </a>
                    </Link>
                </div>
            </div>
        </div>
    )
}