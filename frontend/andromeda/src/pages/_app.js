import Head from 'next/head';

import 'react-loading-skeleton/dist/skeleton.css'

import Layout from '@/components/Layout';
import '@/styles/globals.css';


export default function App({ Component, pageProps }) {
	return (
		<>
			<Head>
				<title>Andromeda</title>
			</Head>
			<Layout>
				<Component {...pageProps} />
			</Layout>
		</>
	);
}
