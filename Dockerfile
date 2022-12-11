FROM openstax/selenium-chrome

USER root

COPY src/ /home/src/

WORKDIR /home/src

# Install apt dependencies
RUN apt-get install < Aptfile

# # Install dependencies
# RUN python3 -m venv venv \
#     && source venv/bin/activate

RUN pip install -r ./requirements.txt

RUN chmod +x ./*.py

# # Install Chrome
# RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
#     && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
#     && apt-get -y update \
#     && apt-get -y install google-chrome-stable

# # Install chromedriver
# RUN wget -N https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip -P ~/ \
#     && unzip ~/chromedriver_linux64.zip -d ~/ \
#     && rm ~/chromedriver_linux64.zip \
#     && mv -f ~/chromedriver /usr/local/bin/chromedriver \
#     && chown root:root /usr/local/bin/chromedriver \
#     && chmod 0755 /usr/local/bin/chromedriver

ENTRYPOINT ["python3", "/home/src/crawler.py"]
