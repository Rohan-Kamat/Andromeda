import Result from "@/components/result";
import Link from "next/link";
import styles from "@/styles/Home.module.css";
import { use, useState } from "react";
import { useRouter } from "next/router";
import { useEffect } from "react";
import ReactLoading from "react-loading";

import ReactPaginate from 'react-paginate';

function SearchPage() {
  const router = useRouter();
  const { text,page,per_page } = router.query;
  const [isLoading, setIsLoading] = useState(true);
  const [results, setResults] = useState([]);
  const [searchText, setSearchText] = useState(text);
  const [links, setLinks] = useState([]);
  
  const handleChange = (event) => {
    console.log(event.target.value);
    setSearchText(event.target.value);
  };


  const handlePageChange = (event) => {
    console.log(event.selected);
    router.query.page = event.selected + 1;
    router.push(router)
  }


  const callAPI = async () => {
    console.log("Calling API");
    const response = await fetch(
      `http://10.22.0.51:5000/search?query=${text}&page=${page}&per_page=${per_page}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    ).then((response) => response.json());
    
    const links = response.map((item) => {
      return item[0];
    });

    
    setLinks(links);
    console.log("fetched results")
    setIsLoading(false);
  };



 

  useEffect(() => {
    if (text == undefined) return;
    setIsLoading(true);
    setSearchText(text);
    callAPI();
  }, [text,page,per_page]);

  return (
    <div className="">
      <main className="min-h-screen align-center">
        <div className={`${styles.center} fixed top-0 -z-1`}></div>
        <div className="flex flex-col">
          <div className="">
            <div class="mx-auto mb-4 mt-10 flex w-full flex-wrap items-stretch rounded max-w-[500px]  border border-solid border-neutral-300 ">
              
              <input
                type="search"

                class="relative m-0 -mr-px block w-[1%] min-w-0 text-white flex-auto rounded-l  bg-transparent bg-clip-padding px-3 py-1.5 text-base font-normal text-neutral-700 outline-none transition duration-300 ease-in-out focus:border-primary  focus:shadow-te-primary focus:outline-none "
                placeholder="Search"
                aria-label="Search"
                aria-describedby="button-addon1"
                value={searchText}
                onChange={handleChange}
              />

              <div className="rounded-l  pt-2 pr-2">
                <Link
                  href={{ pathname: '/search', query: { text: searchText, page:1,per_page:10} }}
                  onClick = {() => {
                    router.query.text = searchText;
                    router.query.page = 1;  
                    router.push(router)
                  }}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    class="h-5 w-5"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </Link>
              </div>
            </div>

            {isLoading ? (
              <div className=" flex flex-col items-center mt-[300px] ">
                <ReactLoading color={"#FFFFFF"} height={64} width={64} />
              </div>
            ) : (
              <div className="  mx-auto max-w-[600px]">
                {links.map((link,index) => {
                  return <Result link={link} key={index}/>;
                })}
              </div>
            )}


<div className="mb-3">
<ReactPaginate
        breakLabel="..."
        nextLabel=">"
        onPageChange={handlePageChange}
        pageRangeDisplayed={5}
        pageCount={3}
        previousLabel="<"
        renderOnZeroPageCount={null}
        className="flex flex-row justify-center items-center gap-x-5"
      /></div>
          </div>
        
        </div>
      </main>
    </div>
  );
}

export default SearchPage;
