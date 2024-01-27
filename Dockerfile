FROM python:3.13.0a3-alpine3.19

WORKDIR /app

COPY ./app .

# hcidump and hcitool binaries are in the bluez-deprecated it seems
RUN apk add openrc bluez-deprecated bluez sudo build-base gcc python3-dev musl-dev linux-headers \ 
    && pip3 install -r requirements.txt
