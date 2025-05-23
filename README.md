# elastic
for elastic 9
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.4-amd64.deb
bin/keytool -importkeystore -destkeystore /etc/elasticsearch/certs/http-surakshaedr1.p12 -srckeystore /usr/share/elasticsearch/elastic-stack-ca.p12 -srcstoretype PKCS12
