# watchtower

## Ignore Containers

Add the following label to ask watchtower to not auto update for the particular container 

```yaml
    labels:
      com.centurylinklabs.watchtower.enable: "false"
```

Example

```yaml
services:
  immich-server:
    container_name: immich_server
    image: ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}
    # extends:
    #   file: hwaccel.transcoding.yml
    #   service: cpu # set to one of [nvenc, quicksync, rkmpp, vaapi, vaapi-wsl] for accelerated transcoding
    volumes:
      # Do not edit the next line. If you want to change the media storage location on your system, edit the value of UPLOAD_LOCATION in the .env file
      - ${UPLOAD_LOCATION}:/usr/src/app/upload
      - /etc/localtime:/etc/localtime:ro
    env_file:
      - .env
    ports:
      - '15252:2283'
    depends_on:
      - redis
      - database
    restart: always
    healthcheck:
      disable: false
    labels:
      com.centurylinklabs.watchtower.enable: "false"
```