## Run Homie Of Timeouts
### Install Docker
Download and install docker from docker.com
```
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Create Docker group and add user
```
sudo groupadd docker
sudo usermod -aG docker $USER
```

### Clone Github Repository
ssh
`git clone git@github.com:natefoxr/discord-timeout-vote.git`
https
`https://github.com/natefoxr/discord-timeout-vote.git`

### Create discord bot at https://discord.com/developers/applications/BOTID/bot
Give admin permissions and create a discord bot token
Save the discord bot token in the DISCORD_TOKEN variable in a .env file

### Install with docker
`bash /path/to/startup.sh`

### Auto start (rebuild) docker container on reboot
Create a cron task for startup.sh
`crontab -e`
With Logging
`@reboot sleep 10 && /path/to/startup.sh >> /var/log/discord-timeout-startup.log 2>&1`
Without Logging
`@reboot sleep 10 && /path/to/startup.sh`
