FROM rabbitmq:3.7.12

RUN apt-get -y update && apt-get install -y less

#ENV RABBITMQ_LOGS="/var/log/rabbitmq/log/"
#ENV RABBITMQ_LOGS="/var/log/rabbitmq/log/"
#ENV RABBITMQ_SASL_LOGS="/var/log/rabbitmq/log/"