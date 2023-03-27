import Head from "next/head";
import Image from "next/image";
import { Inter } from "next/font/google";
import styles from "@/styles/Home.module.css";
import { useState } from "react";
import Link from "next/link";
const inter = Inter({ subsets: ["latin"] });


export default function Home() {
  const [searchText, setSearchText] = useState("");
  
  const onClick = (e) => {
    e.preventDefault();
    console.log("Clicked");
    console.log(searchText);

  }
  
  const handleChange = (event) => {
    setSearchText(event.target.value);
  };
  return (
    <>
      <main className={styles.main}>
        <div className={styles.center}></div>
          <div className="flex-col my-[100px]">
            <div className="text-8xl font-bold font-chakra">Andromeda</div>
            <div className="mt-[50px]">
              <div class="flex justify-center">
                <div class="mb-3 xl:w-96">
                  <div class="relative mb-4 flex w-full flex-wrap items-stretch rounded  border border-solid border-neutral-300 ">
                    <input
                      type="search"
                      class="relative m-0 -mr-px block w-[1%] min-w-0 flex-auto rounded-l  bg-transparent bg-clip-padding px-3 py-1.5 text-base font-normal text-neutral-700 outline-none transition duration-300 ease-in-out focus:border-primary focus:text-neutral-700 focus:shadow-te-primary focus:outline-none "
                      placeholder="Search"
                      aria-label="Search"
                      aria-describedby="button-addon1"
           
                      onChange={handleChange}
                    />
                    <div className="rounded-l  pt-2 pr-2">

                    <Link href={{ pathname: '/search', query: { text: searchText} }}>
                    
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
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
