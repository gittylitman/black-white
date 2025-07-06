FROM python:3.12.2

ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
RUN sh /home/netfree-unix-ca.sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
WORKDIR /app
COPY ./ /app
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -sSL https://sdk.cloud.google.com | bash && \
    apt-get clean

ENV PATH="/root/google-cloud-sdk/bin:${PATH}"
RUN pip install  .
CMD [ "flet" , "run" , "-d" , "--web" , "--port" , "8092" , "src/main.py" ]