FROM fedora:latest
LABEL authors="palomo"

WORKDIR "/root/app/"

RUN dnf update -y && \
    dnf install python3 python3-pip virtualenv git -y


ENTRYPOINT ["/bin/sh", "-c"]