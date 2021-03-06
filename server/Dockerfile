FROM python:3.7

#
# Google Cloud Sdk 설치
#

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

#
# 음성인식 Python 패키지 설치
#

# Install python packages
RUN pip install \
  pydub \
  argparse \
  google-cloud-speech

RUN apt update
RUN apt install -y ffmpeg

#
# 웹 서버 설치
#

# MySql 설치
RUN apt install -y mariadb-server

# django 설치
RUN pip install \
  django==2.2.11 \
  djangorestframework==3.9.0 \
  django-rest-swagger==2.2.0 \
  mysqlclient

# 기본 DB 생성
RUN service mysql start && echo create database server\; | mysql -u root

EXPOSE 80 443 8000

# nginx 설치
RUN apt install -y nginx

CMD service mysql start \
  && python /server/manage.py migrate \
  && service nginx start \
  && python /server/manage.py runserver
