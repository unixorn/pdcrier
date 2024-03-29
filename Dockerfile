FROM unixorn/debian-py3:latest
LABEL maintainer="Joe Block <jpb@unixorn.net>"
LABEL description="Make a debug toolkit on debian buster-slim"

RUN apt-get update && \
    apt-get install -y apt-utils ca-certificates --no-install-recommends && \
		update-ca-certificates && \
		rm -fr /tmp/* /var/lib/apt/lists/* && \
    /usr/bin/python3 -m pip install --upgrade pip --no-cache-dir && \
    pip3 cache purge

RUN mkdir /data && \
  mkdir /config

COPY dist/*.whl /data
RUN pip3 install --no-cache-dir /data/*.whl

CMD ["bash"]
