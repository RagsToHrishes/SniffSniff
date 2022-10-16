import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import Header from './components/Header'
import Link from 'next/link'

export default function Home() {

  return (
    <div>
      <Header />
      <div>
        <div className={styles.section}>
          <div className={styles.sectiontext}>
            <h1 className={styles.orange}>Don't be lost!</h1>
            <h1 className={styles.black}>Sniff out your classmates</h1>
            <p className={styles.caption}>Find where your classmates are online, discover new information, and stay up to date with your class’s content.</p>
          </div>
          <img className={styles.mascot} src='/mascot.png'/>
        </div>
      </div>

      <div className={styles.section2}>
        <h1 className={styles.sec2head}>Sniff out...</h1>
        <div className={styles.containers}>
          <div className={styles.container1}>
            <img className={styles.sec2_dogs} src='/winking_dog.png'/>
            <h3 className={styles.h3}>Discord</h3>
            <p className={styles.dog_captions}>find the most active discord channel</p>
          </div>
          <div className={styles.container2}>
            <img className={styles.sec2_dogs} src='/excited_dog.png'/>
            <h3 className={styles.h3}>Slack</h3>
            <p className={styles.dog_captions}>find the most active slack channel</p>
          </div>
          <div className={styles.container3}>
            <img className={styles.sec2_dogs} src='/curious_dog.png'/>
            <h3 className={styles.h3}>Missed Info</h3>
            <p className={styles.dog_captions}>find out what you missed while you were gone</p>
          </div>
        </div>
      </div>

      <div className={styles.section3}>
        <h1 className={styles.sec3head}>Meet Sniffodoo!</h1>
        <div className={styles.bigContainer}>
          <img className={styles.sniffodoo} src='/sniffodoo.png'/>
          <div className={styles.smallContainers}>
            <div className={styles.small1}>
              <h1 className={styles.bigSniffoDoo}>Sniffodoo!</h1>
              <p className={styles.sniffoBody}>Your own detective who will sniff out and give you a summary of what you missed 
                while you were away from your class channels.</p>

              <p className={styles.sniffoBody}>Save time. Say Goodbye to your 1000+ unread messages.</p>
            </div>
            <div className={styles.small2}>
              <p className={styles.sniffoBody}> Add your own Sniffodoo to your channels!</p>
              <Link href="./search.js">
                <a className={styles.downloadButton}>Download Sniffodoo</a>
              </Link>
            </div>
          
          </div>
        </div>
      </div>

    </div>
  )
}
