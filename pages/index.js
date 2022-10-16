import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'

export default function Home({ data }) {
  console.log(data)
  return (
    <div>

    </div>
  )
}

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
