# syntax=docker/dockerfile:1

FROM ubuntu:22.04 AS compiler
USER root
WORKDIR /tmp
ARG ECCODES=eccodes-2.35.0-Source
ARG ECCODES_DIR=/usr/include/eccodes

RUN apt update -y \
    && apt install gcc g++ gfortran perl wget cmake libaec-dev libpng-dev -y \
    && apt clean all

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN wget -c --progress=dot:giga \
    https://confluence.ecmwf.int/download/attachments/45757960/${ECCODES}.tar.gz  -O - | tar -xz -C . --strip-component=1 

WORKDIR /tmp/build
SHELL ["/bin/bash", "-c" ]
RUN cmake -DCMAKE_INSTALL_PREFIX="${ECCODES_DIR}" -DENABLE_PNG=ON .. \
    && make -j"$(nproc)" \
    && make install

USER 1001

FROM python:3.10 AS py310
USER root
WORKDIR /tmp

ENV ECCODES_DIR=/usr/include/eccodes
COPY --from=compiler --chown=1001:0 /usr/include/eccodes /usr/include/eccodes
RUN apt update -y \
    && apt install libaec-dev libpng-dev -y \
    && apt clean all

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .
RUN pip install wheel \
    && pip install . --no-cache-dir && python -c "import pygrib"
USER 1001


FROM python:3.11 AS py311
USER root
WORKDIR /tmp

ENV ECCODES_DIR=/usr/include/eccodes
COPY --from=compiler --chown=1001:0 /usr/include/eccodes /usr/include/eccodes
RUN apt update -y \
    && apt install libaec-dev libpng-dev -y \
    && apt clean all

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .
RUN pip install wheel \
    && pip install . --no-cache-dir && python -c "import pygrib"

USER 1001

FROM python:3.12 AS py312
USER root
WORKDIR /tmp

ENV ECCODES_DIR=/usr/include/eccodes
COPY --from=compiler --chown=1001:0 /usr/include/eccodes /usr/include/eccodes
RUN apt update -y \
    && apt install libaec-dev libpng-dev -y \
    && apt clean all

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .
RUN pip install wheel \
    && pip install . --no-cache-dir && python -c "import pygrib"

USER 1001
