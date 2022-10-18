FROM python:3.10

RUN python -m pip install flask flask-restful

COPY * /root/wordle/

WORKDIR /root/wordle
CMD python site.py