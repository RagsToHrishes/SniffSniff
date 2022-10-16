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
            <h1>Don't be lost!</h1>
            <h1>Sniff out your friends!</h1>
          </div>
          <img src='/mascot.png'/>
        </div>
      </div>

    </div>
  )
}
