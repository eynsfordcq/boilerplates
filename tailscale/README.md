# tailscale

## Setup on OCI (Ubuntu 24)

```sh
# install
curl -fsSL https://tailscale.com/install.sh | sh

# enable ip forwarding
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

# allow masquerading
sudo iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
```
