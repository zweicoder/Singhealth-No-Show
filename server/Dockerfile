FROM ubuntu:14.04

MAINTAINER Chong Zhi Wei <zhiwei_chong@mymail.sutd.edu.sg>

RUN apt-get update && apt-get install -y git gcc build-essential software-properties-common
RUN add-apt-repository ppa:fkrull/deadsnakes
RUN apt-get install -y python2.7 python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
WORKDIR /opt
RUN git clone --recursive https://github.com/dmlc/xgboost
RUN cd xgboost; make -j4 -i
RUN apt-get -y install python-pip && pip install setuptools flask flask_cors
RUN cd /opt/xgboost/python-package/ && python setup.py install
WORKDIR /root
RUN git clone https://github.com/zweicoder/Singhealth-No-Show.git capstone
WORKDIR capstone/server
EXPOSE 5000
RUN apt-get -y install curl
CMD export FLASK_APP=server.py && flask run --host=0.0.0.0