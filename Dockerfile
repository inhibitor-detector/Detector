# Use a base image with Python 2.7 ?
# FROM python:3
FROM arm32v6/python:3.11-alpine3.18

# Install basic dependencies
RUN apk update
RUN apk upgrade
RUN apk add bash
RUN apk add git
RUN apk add --update python3 python3-dev gfortran py-pip build-base py3-numpy
RUN apk add libusb
RUN apk --no-cache add musl-dev linux-headers g++
WORKDIR /app
RUN pip install --upgrade pip
# RUN pip install pyusb #installed by rfcat
# RUN pip install numpy #better installed in line 10
# RUN pip install ipython==5 #installed by rfcat
# RUN pip install PySide2 #not compatible with RPI (we won't need it anyways)

# Install rfcat
WORKDIR /app
RUN git clone https://github.com/uri-99/rfcat-tesis.git
WORKDIR /app/rfcat-tesis
RUN python3 setup.py install

# Install expect tool
WORKDIR /app
RUN apk add expect


# Copy application files
COPY ./app/auto_rfcat.sh /app/auto_rfcat.sh
RUN chmod +x /app/auto_rfcat.sh
COPY ./app/analyzer.sh /app/analyzer.sh
RUN chmod +x /app/analyzer.sh
COPY ./app/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# clean / optimize docker size
# todo: migrate following apt-get to Alpine format
# RUN apt-get autoremove -y
# RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/* /var/tmp/*

# Run rfcat on start
CMD ["/app/start.sh"]