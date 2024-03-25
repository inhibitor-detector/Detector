# Use a base image with Python 2.7
FROM python:3

# Install rfcat dependencies
WORKDIR /app
RUN pip install requests

# Set the working director
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