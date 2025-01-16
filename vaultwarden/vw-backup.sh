#!/bin/bash
docker run --rm --volumes-from=vaultwarden -e UID=0 -e BACKUP_DIR=/vault-backup -e TIMESTAMP=true -v /vault-backup:/vault-backup bruceforce/vaultwarden-backup manual