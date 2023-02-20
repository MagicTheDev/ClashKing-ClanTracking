FROM python:3.8
RUN mkdir -p /bot
WORKDIR bot
COPY ./requirements.txt /bot/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /bot
EXPOSE 8000
CMD python3 main.py