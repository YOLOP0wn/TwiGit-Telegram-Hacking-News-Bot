TwiGit is a simple python script that you can use with Cron to get the latest Hacking News (exploit/poc/0day) from Twitter and Github and send it to your Telegram channel automatically.

This script use Twitter search API and GitHub search repos API to find latest hacking news using keywords combinaison.

Create a new telegram group and invite all your team mates/friends in it, add your telegram Bot as Admin to it, and share Hackin News with everyone.
&nbsp; 


**REQUIREMENTS** 
- Twitter API Keys/Tokens with Read, write, and direct messages privileges (ht<span>tps://developer.twitter.com)
- Telegram Bot Token (ht<span>tps://telegram.me/botfather)
- Your chat_id (ht<span>tps://api.telegram.org/bot[YOUR-BOT-TOKEN]/getUpdates?offset=0)
&nbsp; 


**INFORMATIONS**
- "id.txt" file contain the last highest tweet id found and use it in the next search request in order to find only newest tweets and avoid duplicate.
- Twitter search query use -filter: retweets & -filter: reply to avoid duplicate tweets also
- Github search is configured to send only interesting repos related to hacking that has been created that day (filter str(date.today()) (you can configure as you whish)
- Reponse data of Twitter API et Github API are stored concatenated in "tweets" and "git" variable in order to send all news in 2 saparated messages (twitter telegram message and github telegram message) instead of 1 message per tweet (avoid spam)
&nbsp; 


**INSTALL**
- pip install -r requirements.txt
- Fill Keys & Tokens & chat_id values
- You may need to change path of "id.txt" file in the script (absolute path) to work properly with Cron
- You may need to run script several times until having the last tweets id (if you receive no more data, then you have latest tweet id and there's no new hacking information yet)
