FROM python:latest

ADD . /app
WORKDIR /app
COPY ./event_loop.py /event_loop.py
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
CMD ["python","-u","event_loop.py"]
