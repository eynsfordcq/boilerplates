## Linux

```sh
vi /etc/systemd/system/node_exporter.service

sudo systemctl start node_exporter
sudo systemctl enable node_exporter
sudo systemctl status node_exporter
```

## MacOS

```sh
vi /Library/LaunchDaemons/node_exporter.plist

sudo launchctl bootstrap system /Library/LaunchDaemons/com.mycompany.node_exporter.plist
sudo launchctl print system/node_exporter
```
