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

### Create discord bot at https://discord.com/developers/applications/BOTID/bot
Give admin permissions and create a discord bot token
Save the discord bot token in the DISCORD_TOKEN variable in a .env file

### Install with docker
`sudo docker build -t homie-music . && sudo docker run -d --name homie-music --env-file .env -it homie-music`
