FROM python:3.11-slim

RUN apt-get update && apt-get install -y git

RUN pip install git+https://github.com/Zerka30/servarr-backup

ENTRYPOINT ["servarr"]
CMD ["--help"]
