import { useEffect } from "react";
import { useState } from "react";
export default function Result({link}) {
    const [data, setData] = useState({});
    const getMetaData = async () => {
        let response = await fetch(`http://10.22.0.51:5000/metadata?url=${link}`, {
        method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        response = await response.json()
        setData(response)
        
      }

    useEffect(() => {
        try{
            getMetaData()

        }catch(err){
            console.log(err)
        }
    })
    return (
        <div className="py-5">
            <div className="flex flex-row rounded items-center">
                <img className="inline object-fill mr-2 rounded-full" src={`http://www.google.com/s2/favicons?domain=${link}&size=32`} alt="favicon"/>
               <a target="_blank" href={link}> <div>
                    <div className="text-[0.70rem]">
                        {data.title!=null ? data.title.substr(0,20)+"..":null}
                    </div>
                    <div className="text-[0.75rem]">
                        <a href={link} target="_blank" rel="noopener noreferrer">{link.substr(0,50)+".."}</a>
                    </div>
                    </div></a>

            </div>
            <a target="_blank" href={link}><div className="text-xl text-sky-700">
                {data.heading}
            </div></a>
            {/* set max width for the below componenent */}
                        <div className="max-w-2xl text-md   ">
                {data.description!=null? data.description.length > 100 ? data.description.substr(0,99) + ".." :data.description: null}
                </div>
        </div>
    );}
    