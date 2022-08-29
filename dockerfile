# syntax=docker/dockerfile:1

FROM python:3.10.4-bullseye



USER root

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libxss1
RUN apt-get install -y  fonts-liberation  libasound2   libatspi2.0-0
RUN apt-get install -y  libgtk-3-0  libnspr4   libnss3  libx11-xcb1  libxtst6 lsb-release  xdg-utils libgbm1
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN apt-get install -f
RUN apt-get install -y xvfb
RUN apt-get install -y unzip
RUN wget https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip
RUN unzip -d /usr/src/app chromedriver_linux64.zip
RUN chmod +x /usr/src/app/chromedriver

RUN pip install --no-cache-dir --upgrade pip


COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py /app

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080","--timeout", "90", "app:app"]