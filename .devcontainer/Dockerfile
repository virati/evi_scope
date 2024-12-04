FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye


RUN apt-get update && apt-get install -y ffmpeg

# Update pip
RUN pip install --upgrade pip

#Install poetry official way
USER vscode
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH = "${PATH}:/home/vscode/.local/bin"
