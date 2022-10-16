import styles from '../css/Header.module.css'
import Link from 'next/link'
import { useRouter } from 'next/router';

export default function Header() {

    const myRouter = useRouter()
    const currRoute = myRouter.pathname;

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
                            <p className= {currRoute === '/' ? styles.activePage : styles.nothing}>Home</p>
                        </a>
                    </Link>
                    <Link href="/search">
                        <a>
                            <p className= {currRoute === '/search' ? styles.activePage : styles.nothing}>Courses</p>
                        </a>
                    </Link>
                </div>
            </div>
        </div>
    )
}
