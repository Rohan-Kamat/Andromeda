# Andromeda
Building a search engine from scratch. We plan on implementing the 3 major components in a search engine - `Crawler`, `Parser` and `Indexing`. We will begin by developing command line tools for these components and then wrapping these with an API service to be used by a frontend. This project is being done under IEEE-NITK.

## Dev Server
### VPN Connection
To establish a VPN connection to NITK-NET:
1. Login at the Sophos portal - [link](vpnportal.nitk.ac.in).
2. Download SSL-VPN config file for the necessary OS.
3. Execute `sudo openvpn <path-to-config-file>` to initiate the connection sequence. Keep this terminal open.

### SSH
1. Execute `ssh <user>@<container-ip>` and then enter necessary details on being prompted.

## Getting Started
### Setup
1. Install `Docker Engine` by following this [link](https://docs.docker.com/engine/install/ubuntu/).
2. Touch a file - `src/.env`. 
    ```.env
    MONGO_USER=admin
    MONGO_PASSWORD=adminpw
    ```
3. Create a virtual environment and then install all the dependencies in `src/requirements.txt` after activating the environment.

### Running
1. Activate the virtual environment.
2. Execute `docker-compose up -d` to bring up the `MongoDB` server.

> **Note** <br />
> In the Docker network, the MongoDB server will be running at port - `27017` and a service known as Mongo-Express will be running at port - `8081` which provides a GUI to access the database.

## Guidelines
- Please follow the [pep8](https://peps.python.org/pep-0008/) python style guide
- Refer to this [link](https://cbea.ms/git-commit/) to write proper commit messages

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
