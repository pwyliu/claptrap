claptrap
========

Claptrap.py uses the Twitter streaming API to watch for Borderlands 2 SHiFT codes. When a code is detected Claptrap emails it to you using the Mailgun API for easy redemption. Now you can get that rad purple SMG with minimal effort and in a timely manner. High five!

## Requirements

+Python 2.7
+(Twitter API key)[https://dev.twitter.com/]
+(Mailgun API key)[http://www.mailgun.com/]. If you don't want to use Mailgun, you can easily adapt this script to use SMTP and, say, Gmail. But that would be silly because Mailgun is cool and awesome.
+(Requests)[https://github.com/kennethreitz/requests]
+(Tweepy)[https://github.com/tweepy/tweepy]
