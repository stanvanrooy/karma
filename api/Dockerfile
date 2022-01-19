FROM python:3.9
RUN apt-get update 
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]

