
FROM rapydo/backend:0.6.3
LABEL maintainer="Emilian Godlewski"

COPY requirements.txt /tmp/
RUN pip3 install --upgrade --no-cache-dir -r /tmp/requirements.txt
RUN python -m textblob.download_corpora
