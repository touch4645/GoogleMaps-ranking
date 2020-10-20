FROM python:3.8.0
USER root

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update && apt-get install -y google-chrome-stable && apt-get install -yqq unzip

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/86.0.4240.22`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install heroku cli
RUN curl https://cli-assets.heroku.com/install.sh | sh

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN apt-get update && apt-get install -y \
	&& pip install --upgrade pip

# change dir
WORKDIR /home/KJA_APP

# install module
COPY requirements.txt /home
RUN pip install -r /home/requirements.txt

# flask setting
ENV FLASK_APP '/home/KJA_APP/app.py'
ENV FLASK_DEBUG 1
