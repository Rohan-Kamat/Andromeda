import { useState } from 'react';

import Spinner from '@/components/Spinner';
import { LoaderContext } from '@/contexts/loaderContext';
import styles from '@/styles/Home.module.css';


export default function Layout({ children }) {
	const [loading, setLoading] = useState(false)

	return (
		<>
			<LoaderContext.Provider value={{ loading, setLoading }}>
				{loading && <Spinner />}
				<main>
					<div className={styles.center}></div>
					{children}
				</main>
			</LoaderContext.Provider>
		</>
	);
}
