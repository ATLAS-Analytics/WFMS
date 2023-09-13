FROM atlasanalyticsservice/analytics-ingress-base:latest

LABEL maintainer Ilija Vukotic <ivukotic@cern.ch>

WORKDIR /home/analyticssvc

RUN mkdir Jobs && mkdir Tasks && mkdir Queues && mkdir Batch
COPY Jobs Jobs/
COPY Tasks Tasks/
COPY Queues Queues/
COPY Batch Batch/

CMD [ "sleep","9999999" ]