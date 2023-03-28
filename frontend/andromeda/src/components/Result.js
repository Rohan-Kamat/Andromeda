import { useEffect, useState } from 'react';
import Link from 'next/link';
import getConfig from 'next/config';
import Image from 'next/image';

import Skeleton, { SkeletonTheme } from 'react-loading-skeleton';


const ResultSkeleton = () => {
	return (
		<>
			<div className="my-4">
				<SkeletonTheme baseColor="#2a2a2a" highlightColor="#3f3f3f">
					<div className="flex flex-row gap-2 items-center">
						<Skeleton circle={true} width={32} height={32} />
						<div className="flex flex-col">
							<Skeleton height={18} width={100} />
							<Skeleton height={12} width={200} />
						</div>
					</div>
					<Skeleton height={20} width={350} />
					<Skeleton height={12} width={600} count={2} />
				</SkeletonTheme>
			</div>
		</>
	);
};

const truncate = (str, n) => {
	if (str == null) {
		return null;
	}
	return str?.length > n ? str.substr(0, n - 1) + '...' : str;
};

export default function Result({ link }) {
	const [data, setData] = useState({});
	
	const [loading, setLoading] = useState(false);
	
	useEffect(() => {
		const getMetaData = async () => {
			try {
				setLoading(true);

				const { publicRuntimeConfig } = getConfig();
				const apiHost = publicRuntimeConfig.apiHost;
	
				let response = await fetch(`${apiHost}/metadata?url=${link}`, {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
					},
				});
				response = await response.json();
	
				setData(response);
			}
			catch (error) {
				console.log(error);
			}
	
			setLoading(false);
		};

		getMetaData();
	}, [link]);

	return (
		<>
			{loading ? <ResultSkeleton /> : <div className="py-5">
				<div className="flex flex-row items-center gap-2">
					<div className="bg-white rounded-full overflow-clip flex items-center justify-center w-6 h-6">
						<Image className="inline object-fill" src={`http://www.google.com/s2/favicons?domain=${link}&size=32`} alt="favicon" width={16} height={16} />
					</div>
					<Link target="_blank" href={link} passHref={true}>
						<div className="text-base font-medium">
							{truncate(data.title, 20)}
						</div>
						<div className="text-xs font-light">
							{truncate(link, 100)}
						</div>
					</Link>
				</div>
				<Link target="_blank" href={link} passHref={true}>
					<div className="text-2xl text-purple font-semibold hover:underline">
						{truncate(data.heading, 50)}
					</div>
				</Link>
				<div className="max-w-2xl text-sm font-light">
					{truncate(data.description, 100)}
				</div>
			</div>}
		</>
	);
}
