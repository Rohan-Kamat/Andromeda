import Result from '@/components/result';
import Link from 'next/link'
import styles from "@/styles/Home.module.css";

import { useEffect } from 'react';



function MetaData() {

  return (
    <>
    <main className="min-h-screen align-center">

    <div className={styles.center}>
      <div className='flex flex-col'>

       <div class="relative mb-4 flex w-full flex-wrap items-stretch rounded  border border-solid border-neutral-300 ">
                    <input
                      type="search"
                      class="relative m-0 -mr-px block w-[1%] min-w-0 flex-auto rounded-l  bg-transparent bg-clip-padding px-3 py-1.5 text-base font-normal text-neutral-700 outline-none transition duration-300 ease-in-out focus:border-primary focus:text-neutral-700 focus:shadow-te-primary focus:outline-none "
                      placeholder="Search"
                      aria-label="Search"
                      aria-describedby="button-addon1"
                      
                      />
                    <div className="rounded-l  pt-2 pr-2">

                    <Link href={`search/`}>
                    
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
     <Result />
     <Result />
     <Result />
     <Result />
     <Result />
     <Result />
     <Result />
     <Result />
     <Result />

                          </div>
                          </div>
                          </main>
    </>
  );
}

export default MetaData;