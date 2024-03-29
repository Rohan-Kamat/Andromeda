import { useState, useEffect, useContext } from 'react';
import { useRouter } from 'next/router';
import getConfig from 'next/config';
import Link from 'next/link';

import ReactPaginate from 'react-paginate';

import Result from '@/components/Result';
import SearchBar from '@/components/SearchBar';
import { LoaderContext } from '@/contexts/loaderContext';


function SearchPage() {
	const router = useRouter();
	const { text } = router.query;

	const [results, setResults] = useState([]);
	
	const [page, setPage] = useState(1);
	
	const handlePageChange = (e) => {
		setPage(e.selected + 1);
	};

	const { setLoading } = useContext(LoaderContext);
	
	useEffect(() => {
		const getData = async () => {
			setLoading(true);
			
			try {
				const { publicRuntimeConfig } = getConfig();
				const apiHost = publicRuntimeConfig.apiHost;
				const perPage = publicRuntimeConfig.perPage;

				const response = await fetch(
					`${apiHost}/search?query=${text}&page=${page}&per_page=${perPage}`,
					{
						method: 'GET',
						headers: {
							'Content-Type': 'application/json',
						},
					}
				).then((response) => response.json());

				const links = response.map((item) => {
					return item[0];
				});

				setResults(links);
			} catch (error) {
				console.log(error);
				setResults([]);
			}

			setLoading(false);
		};
		if (text) {
			getData();
		}
	}, [page, text, setLoading]);

	return (
		<>
			<div className="py-20 px-10 xl:px-72">
				<Link href="/"><h1>Andromeda</h1></Link>
				<SearchBar />
				<hr className="mt-4" />
				<div className="">
					{results.map((link, index) => {
						return <Result link={link} key={index} />;
					})}
				</div>
				<ReactPaginate
					breakLabel="..."
					nextLabel=">"
					onPageChange={handlePageChange}
					pageRangeDisplayed={5}
					pageCount={3}
					previousLabel="<"
					renderOnZeroPageCount={null}
					className="flex flex-row justify-center items-center gap-x-5"
				/>
			</div>
		</>
	);
}

export default SearchPage;
