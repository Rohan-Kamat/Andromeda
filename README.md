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
#### Docker
1. Install `Docker Engine` by following this [link](https://docs.docker.com/engine/install/ubuntu/).

#### Chromedriver
```bash
# Install Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get -y update \
    && apt-get -y install google-chrome-stable

# Install chromedriver
RUN wget -N https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ~/ \
    && rm ~/chromedriver_linux64.zip \
    && mv -f ~/chromedriver /usr/local/bin/chromedriver
```
> **Warning** <br />
> Take care to use `compatible` versions for `google-chrome` and `chromedriver`. Refer [this](https://stackoverflow.com/a/55266105/15333904) answer on StackOverflow.

#### Env
1. Touch a file - `src/.env`. 
    ```.env
    MONGO_USER=admin
    MONGO_PASSWORD=adminpw
    ```
2. Create a virtual environment and then install all the dependencies in `src/requirements.txt` after activating the environment.

### Running
1. Activate the virtual environment.
2. Execute `docker-compose up -d` to bring up the `MongoDB` server.
3. Execute `python3 src/crawler.py start` to start the process of crawling.

> **Note** <br />
> In the Docker network, the MongoDB server will be running at port - `27017` and a service known as Mongo-Express will be running at port - `8081` which provides a GUI to access the database.

## Guidelines
- Please follow the [pep8](https://peps.python.org/pep-0008/) python style guide
- Refer to this [link](https://cbea.ms/git-commit/) to write proper commit messages

## Intended Tech Stack
- Python
- NextJS
    - [Tutorial](https://youtube.com/playlist?list=PL4cUxeGkcC9g9gP2onazU5-2M-AzA8eBw)
- [click](https://click.palletsprojects.com/en/8.1.x/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)

## References
- [Text Retrieval](https://www.coursera.org/learn/text-retrieval/home/info)
- [Can I Make A Search Engine From Scratch](https://www.youtube.com/watch?v=Mwa4aphsJGI)
- [Crawler Tutorials](https://youtube.com/playlist?list=PL6gx4Cwl9DGA8Vys-f48mAH9OKSUyav0q)
