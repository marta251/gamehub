FROM python:3.9-alpine AS base

WORKDIR /

RUN apk update
RUN apk add --no-cache g++ make git musl-dev

# Clone the Stockfish source code
RUN git clone https://github.com/official-stockfish/Stockfish.git stockfish-src

# Compile Stockfish
RUN cd stockfish-src/src && \
    make -j build STATIC=1 LDFLAGS="-static" && \
    mv stockfish /usr/local/bin


# Build the final image
FROM python:3.9-alpine

WORKDIR /gamehub

# Copy the compiled Stockfish binary from the base image
COPY --from=base /usr/local/bin/stockfish /usr/local/bin/stockfish

COPY dist/gamehub-0.0.1-py3-none-any.whl .
COPY words.txt /gamehub/data/words.txt

RUN ["python", "-m", "pip", "install", "gamehub-0.0.1-py3-none-any.whl"]


ENTRYPOINT ["gamehub"]