FROM atlasanalyticsservice/analytics-ingress-base:latest

LABEL maintainer Ilija Vukotic <ivukotic@cern.ch>

WORKDIR /home/analyticssvc

RUN mkdir Jobs && mkdir Tasks && mkdir Queues
COPY Jobs Jobs/
COPY Tasks Tasks/
COPY Queues Queues/

CMD [ "sleep","9999999" ]