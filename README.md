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

# create a dedicated heap options file (survives package upgrades)
echo "-Xms4g" | sudo tee /etc/elasticsearch/jvm.options.d/heap.options
echo "-Xmx4g" | sudo tee -a /etc/elasticsearch/jvm.options.d/heap.options

# elasticsearch.yml
sudo bash -lc 'grep -q "^bootstrap.memory_lock:" /etc/elasticsearch/elasticsearch.yml && sudo sed -i "s/^bootstrap.memory_lock:.*/bootstrap.memory_lock: true/" /etc/elasticsearch/elasticsearch.yml || echo "bootstrap.memory_lock: true" | sudo tee -a /etc/elasticsearch/elasticsearch.yml'

# systemd limits (allow memlock)
sudo mkdir -p /etc/systemd/system/elasticsearch.service.d

cat <<'EOF' | sudo tee /etc/systemd/system/elasticsearch.service.d/override.conf

[Service]
LimitMEMLOCK=infinity
EOF       
