import requests
from bs4 import BeautifulSoup
import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

_HEADERS = {
    'User-Agent': 'Mozilla/5.0'}  #browser headers
sT = ""
count = 1
imgCount = 1
picGotten = 0
lastCounter = 0
class KnowYourMeme(callbacks.Plugin):
    """
    Looks up memes on the website KnowYourMeme
    """
    def fetchMeme(self, searchTerm=None, getPic=None):
        """
        Searches up a meme. If <searchTerm> is provided, it searches for the specific meme. Otherwise, it chooses a random one.
        """
        found = 1
        global sT
        global count
        global imgCount
        global lastCounter
        if(not searchTerm):
            page = "http://knowyourmeme.com/random"
            count = 1
            imgCount = 1
            lastCounter = 0
        else:
            if(sT!=searchTerm):
                sT = searchTerm
                count = 1
                imgCount = 1
                lastCounter = 0
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
                        if(not getPic):
                            count+=1
                        break
                    else:
                        count2-=1
                counter+=1
            page = "http://knowyourmeme.com" + listOfLinks[counter]['href']  #Picking first meme

        if(found):
            if(getPic):
                picURL = page + "/photos"
                picPage = requests.get(picURL, headers=_HEADERS) 
                soup = BeautifulSoup(picPage.content, 'html.parser')  
                listOfPicLinks = soup.findAll("a", class_='photo')  #Finding all links in the results page
                counter = 0
                picCount = imgCount
                for i in listOfPicLinks:
                    if("/photo" in i['href']):
                        if(picCount==0):
                            break
                        else:
                            picCount -=1
                    counter+=1
                counter-=1
                if(lastCounter==counter):
                    return("No more pictures were found.")
                else:
                    lastCounter=counter
                page = "http://knowyourmeme.com" + listOfPicLinks[counter]['href']
                url = requests.get(page, headers=_HEADERS) #opening the final page
                soup = BeautifulSoup(url.content, 'html.parser')
                title = soup.find('meta', attrs={"property": "og:title"})['content'] #getting title info
                imageURL = soup.find('meta', attrs={"property": "og:image"})['content'] #getting the image
                return(f"{title}, {imageURL}")
            else:
                url = requests.get(page, headers=_HEADERS) #opening the final page
                soup = BeautifulSoup(url.content, 'html.parser')
                title = soup.find('meta', attrs={"property": "og:title"})['content'] #getting title info
                finalURL = soup.find('meta', attrs={"property": "og:url"})['content'] #getting the page url
                return(f"{title}, {finalURL}")   
        else:
            return("No memes were found.")
            
    def meme(self, irc, msg, args, searchTerm):
        """
        [<searchTerm>]
        
        Searches up a meme. If <searchTerm> is provided, it searches for the specific meme. Otherwise, it chooses a random one.
        """
        global picGotten
        picGotten = 0
        irc.reply(self.fetchMeme(searchTerm, 0))
    meme = wrap(meme, [optional('text')])
    
    def getpic(self, irc, msg, args, searchTerm):
        """
        [<searchTerm>]
        
        Searches up a meme picture.
        """
        global picGotten
        picGotten = 1
        irc.reply(self.fetchMeme(searchTerm, 1))
    getpic = wrap(getpic, ['text'])

    def memepic(self, irc, msg, args):
        """
        Gets a meme image from KnowYourMeme.
        """
        url = "http://knowyourmeme.com/photos/random"
        page = requests.get(url, headers=_HEADERS)  # requesting code
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('meta', attrs={"property": "og:title"})['content'] #getting title info
        finalURL = soup.find('meta', attrs={"property": "og:url"})['content'] #getting the page url
        irc.reply(f"{title}, {finalURL}")
    memepic = wrap(memepic)
    
    def nextmeme(self, irc, msg, args):
        """
        Goes to the next meme on the list.
        """
        global sT
        global count
        if sT is None:
            irc.reply("No meme has been searched for yet.")
        else:
            count += 1
            irc.reply(self.fetchMeme(sT, 0))
    nextmeme = wrap(nextmeme)
    
    def nextpic(self, irc, msg, args):
        """
        Goes to the next picture of the meme that has been searched for.
        """
        global sT
        global imgCount
        global picGotten
        if(not picGotten):
            irc.reply("No meme picture has been searched for yet. Use the @getpic command.")
        else:
            imgCount += 1
            irc.reply(self.fetchMeme(sT, 1))
    nextpic = wrap(nextpic)
    
    
Class = KnowYourMeme
