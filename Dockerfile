FROM python:2.7

ARG destdir=/opt/webpage-monitor
ARG pip=${destdir}/bin/pip

COPY . /tmp/build

RUN set -x \
  \
  && apt-get update \
  && apt-get install -y libsnappy-dev \
  \
  && virtualenv --never-download ${destdir} \
  && cd /tmp/build \
  && ${pip} install -r requirements.txt \
  && ${pip} install . \
  \
  && cp /tmp/build/pkg/docker/entrypoint.sh ${destdir}/bin \
  && chmod +x ${destdir}/bin/entrypoint.sh

ENTRYPOINT ["/opt/webpage-monitor/bin/entrypoint.sh"]
