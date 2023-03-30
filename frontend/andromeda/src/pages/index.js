import SearchBar from '@/components/SearchBar';


export default function Home() {
	return (
		<>
			<div className="flex flex-col items-center justify-center h-[100vh]">
				<h1>Andromeda</h1>
				<SearchBar />
			</div>
		</>
	);
}
