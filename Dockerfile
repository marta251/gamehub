FROM python

WORKDIR /home/gamehub

COPY dist/gamehub-0.0.1-py3-none-any.whl .

RUN ["python", "-m", "pip", "install", "gamehub-0.0.1-py3-none-any.whl"]

ENTRYPOINT ["gamehub"]