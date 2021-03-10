# First Stage

FROM ubuntu:20.04

RUN apt-get update
RUN apt-get -y install python3-pip

WORKDIR /app

COPY ./requirements.txt .
COPY ./requirements_test.txt .

RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements_test.txt

COPY ./src .
COPY ./models ./models
COPY ./data ./data

CMD [ "pytest", "-v" ]

# Second Stage

FROM ubuntu:20.04

RUN apt-get update
RUN apt-get -y install python3-pip

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src .
COPY ./models ./models
COPY ./data ./data
COPY ./tmp ./tmp
EXPOSE 9001

CMD [ "python3", "./app.py" ]
