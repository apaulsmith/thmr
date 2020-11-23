# set base image (host OS)
FROM python:3.7

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY ./docker_requirements.txt .

RUN pip install --upgrade cython
RUN pip install --upgrade pip
RUN apt update
RUN apt install -y python-numpy
RUN apt install -y python-pandas
RUN apt install -y vim
# install dependencies
RUN pip install werkzeug==0.16.0
RUN pip install -r docker_requirements.txt
RUN pip install pandas

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "python", "./run.py"," --flask","--reset-db"," --generate" ]
