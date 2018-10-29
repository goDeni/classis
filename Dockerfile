FROM python:3

WORKDIR /usr/src/app

RUN pip3 install flask

COPY requirements.txt ./
COPY setup.py ./
COPY classis ./classis

RUN pip install --no-cache-dir -r requirements.txt
RUN python3 ./setup.py install
RUN mkdir ./db

CMD ["python3", "./classis/cmd/main.py"]