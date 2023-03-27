import { useState } from 'react';
import { useRouter } from 'next/router';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';


export default function SearchBar() {
	const [searchText, setSearchText] = useState('');

	const router = useRouter();

	const handleChange = (event) => {
		console.log(searchText);
		setSearchText(event.target.value);
	};

	const handleSubmit = (e) => {
		e.preventDefault();

		if (router.pathname == '/search') {
			router.reload({ pathname: '/search', query: { text: searchText} });
		}
		else {
			router.push({ pathname: '/search', query: { text: searchText} });
		}
	};

	return (
		<>
			<form onSubmit={handleSubmit}>
				<div className="flex flex-row rounded-full border border-solid border-white items-center px-10 w-72 md:w-96 gap-2">
					<input
						type="search"
						className="relative flex-auto bg-transparent bg-clip-padding py-2 text-base font-normal text-white outline-none focus:outline-none"
						placeholder="Search"
						onChange={handleChange}
					/>
					<button
						type="submit"
					>
						<FontAwesomeIcon icon={faMagnifyingGlass} className="text-white" />
					</button>
				</div>
			</form>
		</>
	);
}
