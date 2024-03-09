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

# Install rfcat
WORKDIR /app
RUN git clone https://github.com/atlas0fd00m/rfcat.git
WORKDIR /app/rfcat
RUN python setup.py install

# install ooktools
# WORKDIR /app
# RUN pip install ooktools


# Set the working directory
WORKDIR /app

# Copy your application files if needed
RUN apt-get install -y expect
COPY auto_rfcat.sh /app/auto_rfcat.sh
RUN chmod +x /app/auto_rfcat.sh

# clean / optimise docker size
RUN apt-get autoremove -y
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/* /var/tmp/*

# Run rfcat on start
CMD ["/app/auto_rfcat.sh"]