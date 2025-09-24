# elastic
for elastic 9
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.4-amd64.deb
bin/keytool -importkeystore -destkeystore /etc/elasticsearch/certs/http-surakshaedr1.p12 -srckeystore /usr/share/elasticsearch/elastic-stack-ca.p12 -srcstoretype PKCS12
 [
eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTkyLjE2OC4xLjU6OTIwMCJdLCJmZ3IiOiI0ZWQxMjUxZDY2NDgyMTEwNmI0MjVmYzdkOTExMWFmMTEwYzFiNmRmYzZjZTUyMjA2MzdhMTQyMWM2NjljNDI5Iiwia2V5IjoiZWRJZ0E1a0JaUnZCQUVxbGl6Slc6TFJZdEJhVlU1Xy04Yk9HWlRwV2x0QSJ9
]

[
M 16 0 C 18.909 3.875 23.657 5.804 31.076 3.727 C 29.588 23.314 20.748 23.017 16 28 M 16.089 0.018 C 13.418 3.43 8.373 5.804 1.078 3.727 C 2.586 23.314 10.748 23.165 16 28
]

https://docs.google.com/document/d/1DcI9GZp4p6PYwPJ9QgfSKynxnbC3BrJxuGng7Ml5qko/edit?usp=sharing

https://drive.google.com/drive/folders/1N6raqO5Q6riz33RyrXq9ePf8RPFDBLh6?usp=drive_link

logstash: https://docs.google.com/document/d/17CXY0xoRjNSdlwJRlprjoRBcA77GvqmtSp-IJIHutDc/edit?usp=sharing
Narang: https://drive.google.com/file/d/1FIFv0BOS1cV7KZ8EuyLVJWV-IFrFZz60/view?usp=drive_link
35214392
cmR5em9aZ0JES2VPbjBabUpzSmc6WElQdXdISW9uclRKSkVsbC1LTU5CUQ==

global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'thiru_fake_aps'
    static_configs:
      - targets:
          - '127.0.0.1:9100'
