# python runtime parent image
FROM python:3.7.4

# set the working directory to app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get install default-libmysqlclient-dev &&\
    pip install -r requirements.txt

# Expose 8000 for api
EXPOSE 8000

# Define environment variable
ENV NAME devlopment

# Run server when the container launches
CMD python manage.py runserver 0.0.0.0:8000