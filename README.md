# Andromeda
Building a search engine from scratch. We plan on implementing the 3 major components in a search engine - `Crawler`, `Parser` and `Indexing`. We will begin by developing command line tools for these components and then wrapping these with an API service to be used by a frontend. This project is being done under IEEE-NITK.

## Setup
### VPN Connection
To establish a VPN connection to NITK-NET:
- Login at the Sophos portal - [link](vpnportal.nitk.ac.in).
- Download SSL-VPN config file for the necessary OS.
- Execute `sudo openvpn <path-to-config-file>` to initiate the connection sequence. Keep this terminal open.

### SSH
- Execute `ssh <user>@<container-ip>` and then enter necessary details on being prompted.

## Guidelines
- Please follow the [pep8](https://peps.python.org/pep-0008/) python style guide
- Refer to this [link](https://cbea.ms/git-commit/) to write proper commit messages

## Parser
### Uploading html content  
- Run the content_writer.py file inside the src folder.  
- Change the url variable if you wish to parse a different webpage.  
- This content will later be uploaded from the database.  
### Parsing the html content  
- Navigate inside the /src/cli_scripts folder.  
- Give the following commands  
    > pip install --editable .  
    > parse <absolute path of the /assets/html_content.txt file>
- The links and words will be separated and stored in /assets/links.txt and /assets/words.txt respectively
- Later on this will be stored in the database

## Intended Tech Stack
- Python
- NextJS
- pyCLI
- Flask-RESTful

## References
- [Text Retrieval](https://www.coursera.org/learn/text-retrieval/home/info)
- [Can I Make A Search Engine From Scratch](https://www.youtube.com/watch?v=Mwa4aphsJGI)
- [NextJS Playlist](https://youtube.com/playlist?list=PL4cUxeGkcC9g9gP2onazU5-2M-AzA8eBw)
- [pyCLI](https://pythonhosted.org/pyCLI/#:~:text=The%20cli%20package%20is%20a,profiling%20to%20your%20CLI%20apps.)
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
- [Crawler Tutorials](https://youtube.com/playlist?list=PL6gx4Cwl9DGA8Vys-f48mAH9OKSUyav0q)
