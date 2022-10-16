import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import Header from './components/Header'

export default function Home() {

  return (
    <div>
      <Header />
      <div>
        <div className={styles.section}>
          <div className={styles.sectiontext}>
            <h1 className={styles.orange}>Don't be lost!</h1>
            <h1 className={styles.black}>Sniff out your friends!</h1>
            <p className={styles.caption}>Find where your classmates are online, discover new information, and stay up to date with your class’s content</p>
          </div>
          <img className={styles.mascot} src='/mascot.png'/>
        </div>
      </div>

    </div>
  )
}
