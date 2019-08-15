import requests
import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
      
class Animals(callbacks.Plugin):
    """
    Pulls a random animal pic from the internet.
    """
    def doggo(self, irc, msg, args):
        """
        Pulls a random doggo pic from the internet.
        """
        r = requests.get('https://random.dog/woof.json')
        dogURL = r.json()['url']
        irc.reply(dogURL)
    doggo = wrap(doggo)

    def cat(self, irc, msg, args):
        """
        Pulls a random cat pic from the internet.
        """
        r = requests.get('https://aws.random.cat/meow')
        catURL = r.json()['file']
        irc.reply(catURL)
    cat = wrap(cat)
    
    
Class = Animals
