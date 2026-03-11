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
sudo systemctl daemon-reload
sudo systemctl restart power-monitor
```


```zsh
# .env
TELEGRAM_TOKEN=123456:ABCDEF
TELEGRAM_CHAT_ID=123456789
PING_TIMEOUT=180
SERVER_URL=https://power.domain.name/ping
PING_INTERVAL=30
CLIENT_ID=home-pc
```

```zsh
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d power.domain.name
```


```zsh

```













