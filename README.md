# Strifebot
## Discord bot for the strife discord server

## Instructions
1. install python libraries using pip
2. install pm2 using npm
3. create db topics.sqlite
    TODO Explain how
4. Start database script in startup dir with pm2
5. Start strife script in startup dir with pm2


## Example strife.conf
```
#Strife
owner_roleid=
admin_roleid=
seniorMod_roleid=
moderator_roleid=
reading_roleid=
clerk_roleid=
commoners_roleid=
peasant_roleid=
ghost_roleid=

rules_channelid=
roles_channelid=
general_channelid=
logs_channelid=

TOKEN=
```

## python package-list (Tested working versions)
```
beautifulsoup4      4.9.3
discord             1.0.1
discord.py          1.5.1
humanize            3.1.0
six                 1.15.0
urbandictionary     1.1
wavelink            0.9.6
wikipedia           1.4.0
wordnik-py3         2.1.2
xmltodict           0.12.0
youtube-dl          2020.12.9
```
