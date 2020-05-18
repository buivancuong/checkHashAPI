FROM python:3.6.9-slim-buster
COPY . .
RUN apt-get update
RUN apt install gcc -y
RUN pip install -r requirements.txt
RUN chmod +x bf_*
RUN chmod +x init.sh

CMD ./init.sh


# ENTRYPOINT ["python", "-W ignore", "app.py"]