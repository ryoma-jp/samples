
# --- build command ---
#   docker build --network=host -f Dockerfile -t ubuntu_22.10/python .

FROM ubuntu:22.10

RUN apt update && \
    apt install -y locales vim python3 python3-pip && \
    locale-gen ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL=ja_JP.UTF-8
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

RUN pip3 install psutil==5.9.1 pandas==1.4.3

