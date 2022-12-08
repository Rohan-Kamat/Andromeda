# Parser
## Uploading html content  
- Run the content_writer.py file inside the src folder.  
- Change the url variable if you wish to parse a different webpage.  
- This content will later be uploaded from the database.  
## Parsing the html content  
- Navigate inside the /src/cli_scripts folder.  
- Give the following commands  
    > pip install --editable .  
    > parse <absolute path of the /assets/html_content.txt file>
- The links and words will be separated and stored in /assets/links.txt and /assets/words.txt respectively
- Later on this will be stored in the database
