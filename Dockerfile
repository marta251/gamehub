FROM riccardomorelli/python-alpine-stockfish

WORKDIR /gamehub

COPY dist/gamehub-0.0.1-py3-none-any.whl .
COPY words.txt /gamehub/data/words.txt

RUN ["python", "-m", "pip", "install", "gamehub-0.0.1-py3-none-any.whl"]

ENTRYPOINT ["gamehub"]