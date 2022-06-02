FROM python:latest
#FROM arm32v7/python:latest

COPY . /tradingBot
WORKDIR /tradingBot

RUN apt-get update
RUN apt-get install -y build-essential checkinstall
RUN python -m pip install --upgrade pip

#RUN pip install poetry
#RUN poetry build
#RUN poetry install

#RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
#RUN pip install -r requirements.txt

#CMD ["pip install", "dist/tradingBot-0.1.0-py3-none-any.whl"]
CMD ["/bin/bash"] 
#CMD ["python", "./src/tradingBot/bots/heikinAshiObserver.py"]
#CMD ["poetry run", "python src/tradingBot/bots/heikinAshiObserver.py"] 