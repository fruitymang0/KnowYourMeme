import requests
from bs4 import BeautifulSoup
import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
      
class KnowYourMeme(callbacks.Plugin):
    """
    Looks up memes on the website KnowYourMeme
    """
    sT = ""
    count = 0
    
    def meme(self, irc, msg, args, searchTerm):
        """
        [<searchTerm>]
        
        Searches up a meme. If <searchTerm> is provided, it searches for the specific meme. Otherwise, it chooses a random one.
        """
        found = 1
        if(not searchTerm):
            page = "http://knowyourmeme.com/random"
            count = 0
        else:
            if(sT!=searchTerm):
                sT = searchTerm
                count = 0
            for i in searchTerm:  #formatting search term
                if i == " ":
                    i = "+"
            searchedURL = "http://knowyourmeme.com/search?q=" + searchTerm # making the search url
            resultsPage = requests.get(searchedURL, headers=_HEADERS) 
            soup = BeautifulSoup(resultsPage.content, 'html.parser')  
            listOfLinks = soup.findAll("a", href=True)  #Finding all links in the results page
            counter = 0
            count2 = count
            for i in listOfLinks:
                if ("/random" in i['href'] and counter > 10) or ("page=2" in i['href']) or ("photos/trending" in i['href'] and "/memes/" in i['href']):
                    found = 0
                    break
                if "/memes/" in i['href'] and counter > 110:
                    if(count2==0):
                        break
                    else:
                        count2-=1
                counter+=1
            page = "http://knowyourmeme.com" + listOfElements[counter]['href']  #Picking first meme

        if(found):
            url = requests.get(page, headers=_HEADERS) #opening the final page
            soup = BeautifulSoup(url.content, 'html.parser')
            title = soup.find('meta', attrs={"property": "og:title"})['content'] #getting title info
            finalURL = soup.find('meta', attrs={"property": "og:url"})['content'] #getting the page url
            irc.reply(f"{title}, {finalURL}")
        else:
            irc.reply("No memes were found.")
    meme = wrap(meme, [optional('anything')])

    def memePic(self, irc, msg, args):
        """
        Gets a meme image from KnowYourMeme.
        """
        url = "http://knowyourmeme.com/photos/random"
        page = requests.get(url, headers=_HEADERS)  # requesting code
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('meta', attrs={"property": "og:title"})['content'] #getting title info
        finalURL = soup.find('meta', attrs={"property": "og:url"})['content'] #getting the page url
        irc.reply(f"{title}, {finalURL}")
    memePic = wrap(memePic)
    
    def nextMeme(self, irc, msg, args):
        """
        Goes to the next meme on the list.
        """
        if sT is None:
            irc.reply("No meme has been searched for yet.")
        else:
            count += 1
            meme(self, irc, msg, args, sT)
    nextMeme = wrap(nextMeme)
    
      
Class = KnowYourMeme
