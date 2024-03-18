# Use a base image with Python 2.7
FROM python:3

# Install rfcat dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install libusb-1.0
WORKDIR /app
RUN pip install pyusb
RUN pip install numpy
RUN pip install ipython==5
RUN pip install PySide2
RUN pip install requests

# Set the working directory
WORKDIR /app

# Copy your application files if needed
COPY ./client.py /app/client.py
COPY ./start.sh /app/start.sh

# clean / optimise docker size
RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/* /var/tmp/*

# Run client on start
CMD ["./start.sh"]