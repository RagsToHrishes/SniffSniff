# ExtractionML

## Discord Extraction

Install docker first

```
# pull from https://github.com/Tyrrrz/DiscordChatExporter
docker pull tyrrrz/discordchatexporter:stable

# run docker image -> TOKEN & CHANNELID https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs
# type pwd to get the current directory you are in to store output
docker run --rm -v /path/on/machine:/out tyrrrz/discordchatexporter:stable export -t TOKEN -c CHANNELID
```