import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import Header from './components/Header'

export default function Home({ data }) {

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

<<<<<<< HEAD
=======

>>>>>>> 36b8e1fbbcd87784a58c1a47e894d59bb65552cf
export const getServerSideProps = async () => {

  const data = {
    123: {
      course: 'CS 170',
      name: 'Efficient Algorithms and Intractable Problems',
      discord: 'https://discord.gg/CS170',
    },
    125: {
      course: 'CS 61C',
      name: 'Great Ideas in Computer Architecture (Machine Structures)',
      discord: 'https://discord.gg/CS61C',
    }
  }

  return {
    props: {
      data
    },
  };
};
