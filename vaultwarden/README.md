# vaultwarden

## Backups

Refer [github.com/Bruceforce/vaultwarden-backup](https://github.com/Bruceforce/vaultwarden-backup), Or just use restic


### Setup cron

```sh
# run once per day
0 0 * * * root /path/to/vw-backup.sh > /path/to/vw-backup.out 2>&1
```