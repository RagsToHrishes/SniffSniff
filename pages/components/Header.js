import styles from '../css/Header.module.css'

export default function Header() {
    return (
        <div>
            <div className={styles.header}>
                <img  src='/icon.png' />
                <div className={styles.sound}>
                    <p item='text'>sniff</p>
                    <p item='text'>sniff</p>
                </div>
            </div>
        </div>
    )
}