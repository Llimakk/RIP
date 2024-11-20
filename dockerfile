FROM python

WORKDIR /usr/src/app

COPY requiements.txt ./

RUN pip install -r requiements.txt