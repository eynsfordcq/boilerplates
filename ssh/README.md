# ssh

## ssh-socket

On ubuntu 24, to change the listening ssh port, we have to modify ssh.socket (`/etc/systemd/system/ssh.service.requires/ssh.socket`) instead of sshd_config

See [serverfault](https://serverfault.com/questions/1159599/how-to-change-the-ssh-server-port-on-ubuntu)