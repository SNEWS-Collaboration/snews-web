#!/usr/bin/python

# cLQRecord class
# Blake Stacey (bstacey@mit.edu)
# May 2003

# This is an accessory file to downtime.py.

import re
import string
import os
import time

class cLQRecord:
    BallFiles = {'Red': 'ballred.gif', 'Yellow': 'ballyellow.gif', \
                 'Green': 'ballgreen.gif'}

    def ReadFromFile(self, sPathName):
       # fill the class's data attributes with text from the file

        # open the file for input
        try:
            hInput = open(sPathName, "r")
        except:
            print "Error: unable to read file " + sPathName + " for input."
        # read the contents of the file
        sInput = hInput.read()

        # use regular expressions to parse the important whatsits
        # out of the file's text
        # explanation of regex:
        # The field name is followed by an equal sign and the regex-speak
        # metacharacter combination '(.*)'. Parentheses group the meta-
        # characters so we can refer to the text they match, the . indicates
        # we wish to match all characters except newlines, and the * tells
        # Python we wish to match an arbitrary length of these characters.
        # This regex matches all strings beginning with the fieldname plus
        # an equals sign, and stuffs the rest of the line into the first
        # group of the MatchObject returned by the re.search() method.
        self.Entry = re.search(r"entry=(.*)", sInput).group(1)
        self.Name = re.search(r"name=(.*)", sInput).group(1)
        self.EMail = re.search(r"email=(.*)", sInput).group(1)
        self.ExpName = re.search(r"expt=(.*)", sInput).group(1)
        self.StartYear = re.search(r"startyear=(.*)", sInput).group(1)
        self.StartMonth = re.search(r"startmonth=(.*)", sInput).group(1)
        self.StartDay = re.search(r"startday=(.*)", sInput).group(1)
        self.StartHour = re.search(r"starthour=(.*)", sInput).group(1)
        self.StartMin = re.search(r"startmin=(.*)", sInput).group(1)
        self.EndYear = re.search(r"endyear=(.*)", sInput).group(1)
        self.EndMonth = re.search(r"endmonth=(.*)", sInput).group(1)
        self.EndDay = re.search(r"endday=(.*)", sInput).group(1)
        self.EndHour = re.search(r"endhour=(.*)", sInput).group(1)
        self.EndMin = re.search(r"endmin=(.*)", sInput).group(1)
        self.Grade = re.search(r"grade=(.*)", sInput).group(1)
        self.Comment = re.search(r"comment=(.*)", sInput).group(1)
        # if there were any more fields, I would look for a better way
        # to get this done, but for the moment it should work
        # (and on that philosophy all software around here is built).
    
    def HTML(self):
        # generate an HTML-formatted table row containing the data
        # stored in this class instance
        sRow = ""
        sRow = sRow + "<tr>"
        sRow = sRow + "<td align=\"center\">" + self.Entry + "</td>"
        sRow = sRow + "<td>" + self.ExpName + "</td>"
        sRow = sRow + "<td>" + self.StartYear + "</td>"
        sRow = sRow + "<td>" + self.StartMonth + "</td>"
        sRow = sRow + "<td>" + self.StartDay + "</td>"
        sRow = sRow + "<td>" + self.StartHour + ":" + self.StartMin + "</td>"
        sRow = sRow + "<td>" + self.EndYear + "</td>"
        sRow = sRow + "<td>" + self.EndMonth + "</td>"
        sRow = sRow + "<td>" + self.EndDay + "</td>"
        sRow = sRow + "<td>" + self.EndHour + ":" + self.EndMin + "</td>"
        sRow = sRow + "<td><img src=\"/images/" + self.BallFiles[self.Grade] + \
               "\"></td>"
        sRow = sRow + "<td>" + self.Comment + "</td>"
        sRow = sRow + "</tr>"
        
        return sRow

    def EpochEndTime(self):
        # return the ending time in epoch seconds
        # this *has* to be the most apocalyptically-titled function
        # I've ever coded.

        sTime = self.EndDay + " " + self.EndMonth + " " + self.EndYear \
                + " " + self.EndHour + "h" + self.EndMin
        return int(time.mktime(time.strptime(sTime, "%d %B %Y %Hh%M")))
    
    def EpochStartTime(self):
        # return the starting time in epoch seconds
        # comparison depends upon this

        sTime = self.StartDay + " " + self.StartMonth + " " + self.StartYear \
                + " " + self.StartHour + "h" + self.StartMin
        return int(time.mktime(time.strptime(sTime, "%d %B %Y %Hh%M")))
    
    def __init__(self, sPathName):
        # initialization routine (constructor)
        self.ReadFromFile(sPathName)
    
    def __cmp__(self, other):
        # defines comparison between LQRecord objects
        # objects will be sorted by their starting dates since epoch
        return cmp(self.EpochStartTime(), other.EpochStartTime())
    
