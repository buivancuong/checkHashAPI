FROM python:3.6.9-slim-buster
COPY . .
RUN apt-get update
RUN apt install gcc -y
RUN apt install build-essential -y
RUN pip install -r requirements.txt
RUN g++ -std=c++11 bf_client.cpp -o bf_client
RUN g++ -std=c++11 bf_server.cpp -o bf_server
RUN chmod +x bf_*
RUN chmod +x init.sh

CMD ./init.sh


# ENTRYPOINT ["python", "-W ignore", "app.py"]