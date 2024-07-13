FROM python:3.9

WORKDIR /gamehub

COPY dist/gamehub-0.0.1-py3-none-any.whl .
COPY words.txt /gamehub/data/words.txt
COPY snake_highscore.txt /gamehub/data/snake_highscore.txt

RUN ["python", "-m", "pip", "install", "gamehub-0.0.1-py3-none-any.whl"]
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "stockfish"]

ENTRYPOINT ["gamehub"]