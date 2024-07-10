FROM python

WORKDIR /home/gamehub

COPY dist/gamehub-0.0.1-py3-none-any.whl .
COPY words.txt /home/gamehub/files/words.txt
COPY snake_highscore.txt /home/gamehub/files/snake_highscore.txt

RUN ["python", "-m", "pip", "install", "gamehub-0.0.1-py3-none-any.whl"]
RUN ["apt-get",  "install",  "stockfish"]

ENTRYPOINT ["gamehub"]