FROM python:3

COPY src/ /home/src/

WORKDIR /home/src

# Install apt dependencies
RUN apt-get install < Aptfile

RUN pip install -r ./requirements.txt

RUN chmod +x ./*.py

# Install Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get -y update \
    && apt-get -y install google-chrome-stable

# # Install chromedriver
RUN wget -N https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ~/ \
    && rm ~/chromedriver_linux64.zip \
    && mv -f ~/chromedriver /usr/local/bin/chromedriver

ENTRYPOINT ["python", "/home/src/crawler.py"]
