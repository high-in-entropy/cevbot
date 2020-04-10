# -*- coding: utf-8 -*-
"""
Created on Wed Apr 8 20:23:11 2020

@author: Viraj, CEV NIT Surat
"""

from telegram.ext import Updater, CommandHandler
import os

def key_blog(category):
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    try:
        url = 'https://www.cevgroup.org/category/' + str(category) + '/'
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = soup(webpage, "html.parser")
        lis = []
        for link in page_soup.find_all('a', attrs={'rel': 'bookmark'}):
            lis.append(link.get('href'))
        flist = ""
        for i in range(0, len(lis), 2):
            lis[i] = str(int(i/2)+1) + ". " + lis[i] + "\n\n"
            flist += lis[i]
        return flist
    except:
        return "No article found for that category. Try changing the category."

def latest_blogs():
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    try:
        url = 'https://www.cevgroup.org/blog/'
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = soup(webpage, "html.parser")
        lis = []
        for link in page_soup.find_all('a', attrs={'rel': 'bookmark'}):
            lis.append(link.get('href'))
            flist = ""
        for i in range(0, 10, 2):
            lis[i] = str(int(i/2)+1) + ". " + lis[i] + "\n\n"
            flist += lis[i]
        return flist
    except:
        return ("Theres some error at our side. Please try again later:(")
   
    
def notifications_github():
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup as soup
    try:
        url = 'https://raw.githubusercontent.com/cutting-edge-visionaries/Resources/master/notifications/notification.txt'
        req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        page_soup = soup(webpage, "html.parser")
        return (page_soup)
    except:
        return ("Some error fetching the data. We regret, please try again later.")
    
def latest(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Just a sec! Fetching the list of latest blogs published on CEV Website")
    url = latest_blogs()
    context.bot.send_message(chat_id=update.effective_chat.id, text=url)
    
def start(update, context):
    text = '''Welcome to CEV Bot. You have at your disposal these commands :
        
1. /help - Will display set of commands you can use.

2. /latest - Will fetch a list of 5 recently published blogs on CEV Website.

3. /resources - A well maintained repository of some wonderful resources pertaining to a wide variety of fields.

4. /blog <topic> - Will fetch a list of blogs for your topic of interest. Remove <,> while using the command.
Example, /blog blockchain will fetch blogs related to blockchain.

5. /events - Will inform you regarding future events and activities of CEV'''
    context.bot.send_message(chat_id=update.effective_chat.id, text = text)
    

def resources(update, context):
    links = '''1. A curated list of resources of a huge variety of fields maintained by Team CEV :
https://cutting-edge-visionaries.github.io/Resources/

2. A list of resources maintained by CEV Aryavarta mostly related to the field of Finance, Economics and Algorithmic Portfolio Optimization:
https://github.com/cutting-edge-visionaries/AryavartaResources'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=links)
    
def events(update, context):
    text = notifications_github().text
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def blog(update, context):
    if context.args == []:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Type in the KeyWord along with the blog command')
        return
    if len(context.args) != 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Only one argument allowed')
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Just a sec! Finding related blogs from a huge vault of CEV blogs:)")
    category = context.args[0]
    url = key_blog(category)
    context.bot.send_message(chat_id=update.effective_chat.id, text=url)
    
    
def helpp(update, context):
    text = '''Welcome to CEV Bot. You have at your disposal these commands :
        
1. /help - Will display set of commands you can use.

2. /latest - Will fetch a list of 5 recently published blogs on CEV Website.

3. /resources - A well maintained repository of some wonderful resources pertaining to a wide variety of fields.

4. /blog <topic> - Will fetch a list of blogs for your topic of interest. Remove <,> while using the command.
Example, /blog blockchain will fetch blogs related to blockchain.

5. /events - Will inform you regarding future events and activities of CEV'''
    context.bot.send_message(chat_id=update.effective_chat.id, text = text)

def main():
    TOKEN = "Your API TOKEN Here."
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    start_handler=CommandHandler("start",start)
    blog_handler=CommandHandler("blog", blog)
    help_handler=CommandHandler("help", helpp)
    events_handler=CommandHandler("events", events)
    resources_handler=CommandHandler("resources",resources)
    latest_handler=CommandHandler("latest",latest)
    dp.add_handler(start_handler)
    dp.add_handler(blog_handler)
    dp.add_handler(help_handler)
    dp.add_handler(events_handler)
    dp.add_handler(resources_handler)
    dp.add_handler(latest_handler)
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://<heroku-app-name>.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()
