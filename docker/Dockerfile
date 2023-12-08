FROM python:3.10

WORKDIR /usr/src/app

COPY ../ .

RUN cp -p /bin/openssl ./bin/
RUN pip install --no-cache-dir -r ./docker/requirements.txt

EXPOSE 5000

CMD ["python", "./main.py"]