# n8n

## Generate self-signed cert
```sh
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout n8n-selfsigned.key \
  -out n8n-selfsigned.crt \
  -subj "/CN=<ipv4>"
```

## Create .env file
```plaintext
# Optional timezone to set which gets used by Cron and other scheduling nodes
# New York is the default value if not set
GENERIC_TIMEZONE=Asia/Kuala_Lumpur

# Your server's local IP address
N8N_HOST_IP=<ipv4>
```
