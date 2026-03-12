```zsh
# nano .env
TELEGRAM_TOKEN=123456:ABCDEF
PING_TIMEOUT=180
SERVER_URL=https://power.domain.name/ping
PING_INTERVAL=30
CLIENT_ID=home-pc
```


```zsh
# Install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


```zsh
sudo nano /etc/systemd/system/power-monitor-serv.service

sudo systemctl daemon-reload
sudo systemctl restart power-monitor-serv
sudo systemctl status power-monitor-serv

```


```zsh
sudo systemctl daemon-reload
sudo systemctl enable power-monitor-client
sudo systemctl start power-monitor-client
systemctl status power-monitor-client
```


```zsh
# ~/.config/systemd/user/power-monitor.service

systemctl --user enable power-monitor
systemctl --user start power-monitor

```


```zsh
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d power.domain.name
```














