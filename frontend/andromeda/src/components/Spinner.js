import { BeatLoader } from 'react-spinners';


export default function Spinner() {
	return (
		<div className="fixed top-0 left-0 w-screen h-screen bg-darkGray/40 flex items-center justify-center backdrop-blur-lg !z-50">
			<BeatLoader color='#fff' />
		</div>
	);
}
