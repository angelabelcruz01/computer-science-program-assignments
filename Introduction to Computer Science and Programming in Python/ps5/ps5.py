# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Angel Cruz
# Collaborators: none
# Time:

import feedparser
import string
import time
import threading
import re
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initializes a NewStory object
        
        A NewsStory object has 5 attributes:
            self.guid = (string, globally unique identifier GUID, determined by guid input)
            self.title = (string, the new's story headline, determined by the title input)
            self.description = (string, a paragraph summarizing the news story, determined by description input)
            self.link = (string, a link to the website with the entire story, determined by link input)
            self.pubdate = (datetime, the date the news was published, determined by pubdate input)
        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        '''
        Used to safely return self.guid out of the class
        
        Returns: self.guid
        '''
        return self.guid
    
    def get_title(self):
        '''
        Used to safely return self.title out of the class
        
        Returns: self.title
        '''
        return self.title
       
    def get_description(self):
        '''
        Used to safely return self.description out of the class
        
        Returns: self.description
        '''
        return self.description
    
    def get_link(self):
        '''
        Used to safely return self.link out of the class
        
        Returns: self.link
        '''
        return self.link
    
    def get_pubdate(self):
        '''
        Used to safely return self.pubdate out of the class
        
        Returns: self.pubdate
        '''
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
        Initializes a subclass of class Trigger.
        PhraseTrigger has one attribute:
            self.phrase (string, a ​phrase​ is one or more words separated by a single space between the words.)
        '''
        self.phrase = phrase.lower()
        
    def is_phrase_in(self, txtSample):
        '''
        It takes in one string argument text (txtSample). This method is not case-sensitive.
        
        Returns: It returns ​True​ if self.phrase is present in txtSample, ​False​ otherwise. 
        '''
        regexPhrase = r'\b' + self.phrase + r'\b'
        
        for p in string.punctuation:
            txtSample = txtSample.replace(p, ' ')

        txtSampleList = map(lambda x: x.strip(), txtSample.split())
        txtSampleClean = ' '.join(txtSampleList).lower()
        return bool(re.search(regexPhrase, txtSampleClean))
        

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
        Initializes a subclass TitleTrigger of class Phrasetrigger
        '''
        PhraseTrigger.__init__(self, phrase)
        
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())   


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        '''
        Initializes a subclass DescriptionTrigger of class Phrasetrigger
        '''
        PhraseTrigger.__init__(self, phrase)
        
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())   



# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, triggerdate):
        '''
        Initializes a subclass TimeTrigger of class Trigger.
        It has the following input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
        Time is cnverted from string to a datetime before saving it as an attribute.
        '''
        self.triggerdate = self.format_datetime(triggerdate)
        
    def format_datetime(self, input_string):
        '''
        It takes a string date value with the following format "%d %b %Y %H:%M:%S" and converts it to datetime. 
        It handles excpetions in case the format is not provided correctly
        '''
        try:
            input_datetime = datetime.strptime(input_string, "%d %b %Y %H:%M:%S")
        except ValueError:
            raise ValueError("Input string does not match the expected format (%d %b %Y %H:%M:%S)")
    
        return input_datetime



# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, triggerdate):
        '''
        Initializes a subclass BeforeTrigger of class TimeTrigger
        '''
        TimeTrigger.__init__(self, triggerdate)
        
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo = pytz.UTC) < self.triggerdate.replace(tzinfo = pytz.UTC)


class AfterTrigger(TimeTrigger):
    def __init__(self, triggerdate):
        '''
        Initializes a subclass AfterTrigger of class TimeTrigger
        '''
        TimeTrigger.__init__(self, triggerdate)
        
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo = pytz.UTC)  > self.triggerdate.replace(tzinfo = pytz.UTC) 


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    '''
    Initializes a NotTrigger of class Trigger
    
    It takes a Trigger object as input and save it as class attribute.
    This trigger should produce its output by inverting the output of another trigger.
    '''
    def __init__(self, inputTrigger):
        self.inputTrigger = inputTrigger
        
    def evaluate(self, story):
        return not self.inputTrigger.evaluate(story)



# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    '''
    Initializes a AndTrigger of class Trigger
    
    It takes two trigger objects as input and save it as class attribute.
    This trigger should take two triggers as arguments to its constructor, and should fire on a
    news story only if ​both of the inputted triggers would fire on that item.
    '''
    def __init__(self, inputTrigger1, inputTrigger2):
        self.inputTrigger1 = inputTrigger1
        self.inputTrigger2 = inputTrigger2
        
    def evaluate(self, story):
        return self.inputTrigger1.evaluate(story) and self.inputTrigger2.evaluate(story)
    

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    '''
    Initializes a OrTrigger of class Trigger
    
    It takes two trigger objects as input and save it as class attribute.
    This trigger should take two triggers as arguments to its constructor, and should fire if either
    one (or both) of its inputted triggers would fire on that item.
    '''
    def __init__(self, inputTrigger1, inputTrigger2):
        self.inputTrigger1 = inputTrigger1
        self.inputTrigger2 = inputTrigger2
        
    def evaluate(self, story):
        return self.inputTrigger1.evaluate(story) or self.inputTrigger2.evaluate(story)
    
    


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    tempStories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story): 
                tempStories.append(story)
    return tempStories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("North Korea")
        t2 = DescriptionTrigger("Biden")
        t3 = DescriptionTrigger("Government")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

