TwiGit is a simple python script that you can use with Cron to get the latest Hacking News (exploit/poc/0day) from Twitter and Github and send it to your Telegram channel automatically.

This script use Twitter search API and GitHub search repos API to find latest hacking news using keywords combinaison.

**REQUIREMENTS** 
- Twitter API Keys/Tokens
- Telegram Bot Token
- Your chat_id (https://api.telegram.org/bot<YOUR-BOT-TOKEN>/getUpdates?offset=0)
```pip install -r requirements.txt```

**INFORMATIONS**
- id.txt contain the last highest tweet id found and use it in the next search request in order to find only newest tweets and avoid duplicate.
- Twitter search query use -filter: retweets & -filter: reply to avoid duplicate tweets also
- Github search is configured to send only interesting repos related to hacking that has been created that day (filter str(date.today()) (you can configure as you whish)
