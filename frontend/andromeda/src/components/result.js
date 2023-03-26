export default function Result({data}) {
    return (
        <div className="py-5">
            <div className="flex flex-row rounded items-center">
                <img className="inline object-cover w-7 h-7 mr-2 rounded-full" src="http://www.google.com/s2/favicons?domain=www.google.com" alt="Profile image"/>
                <div>
                    <div className="text-[0.70rem]">
                        Tailwind UI
                    </div>
                    <div className="text-[0.75rem]">
                        <a href="https://www.google.com/" target="_blank" rel="noopener noreferrer">https://tailwindui.com/components/application-ui..</a>
                    </div>
                    </div>

            </div>
            <div className="text-xl text-sky-700">
            Avatars - Official Tailwind CSS UI Components
            </div>
            {/* set max width for the below componenent */}
                        <div className="max-w-2xl text-md   ">
            Avatar group stacked bottom to top. Preview ... Get the code →. Rounded avatars. PNG Preview. Get the code →. Circular avatars with top notification.
                </div>
        </div>
    );}
    