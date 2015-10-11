#!/usr/bin/python

# Downtime tracking script
# Blake Stacey (bstacey@mit.edu)
# May 2003
# Okay, so once again I've been taking somebody else's aged, clunky code
# in a language I hardly understand and trying to make it legible, both
# to myself and to the computer who is now supposed to run it.  This program
# is taking over from downtime.pl, a Perl script which handled the logging
# of downtime events for a family of neutrino detectors around the world.
# (Kamiokande is down thanks to a chain reaction of exploding phototubes,
# etc.) During the move from the SNEWS website's old home (budoe.bu.edu)
# to cyclotron.mit.edu, the Perl script broke, as Perl scripts are wont to
# do.  I learned Perl by reading other people's crocky programs, but I learned
# Python from scratch, so I decided the new version should have a .py suffix.

# When somebody loads the downtime tracking page in their web browser
# (assuming they've gone through appropriate HTTPS authentication) Apache
# calls the Python interpreter which executes this script.  After importing
# modules and setting some variable values, execution goes to the end of
# this file, where we test which course of action to take.  This one file
# contains instructions for displaying the form, handling the data returned
# from the form and displaying a table of results once the user's command
# is processed.

# Auxiliary files include:
# clqrecord.py -- a class for holding an entry read from disk
# template.html -- a file defining the properties of all the web pages
#                  this program generates
# form-template.html -- a pattern for the form our program shows
# table-template.html -- a pattern for the results table we create
#                        when a command is executed successfully
# ballred.gif, ballyellow.gif, ballgreen.gif, PythonPowered.gif --
# small graphics files to spruce up the web pages
# Note that the Python program gains readability over the Perl ancestor
# at the cost of adding extra files.

# Modules we import for needed functionality
import cgi
import string
import math
import re
import os
import os.path
import sys
import time

# This module is one I coded myself
from clqrecord import cLQRecord

# Note my trademark usage of excessive Hungarian notation.
sHomeDir = "/srv/wwwhosts/snews.bnl.gov/shift-data"
sDBDir = os.path.join(sHomeDir, "db")
sTableDir = os.path.join(sHomeDir, "downtime")

sSnnetURL = "https://snews.bnl.gov"

# Use "snews-cgi/" instead of cgi-bin/ as URL to avoid conflicts on
# snews.bnl.gov
sCgiURL = "https://snews.bnl.gov/snews-cgi/downtime.py"

sTemplateFile = "template.html"
sFormFile = "form-template.html"
sTableFile = "table-template.html"

SENDMAIL = "/usr/sbin/sendmail"

# A dictionary of error messages
TimeWarpErrors = {1: 'Start time is greater than end time!', \
                  2: 'End time is earlier than current time!'}


def StripHTML(sText):
    # strip HTML tags from the input text

    SubResult = [sText]      # put the string into a list
    # explanation of regex:
    # [^>] matches all characters not equal to >
    # * tells to match any number >= 0 of those characters
    pattern = re.compile("<[^>]*>")
    
    SubResult = pattern.subn("", SubResult[0])
    if SubResult[1] == 0:
        return sText
    else:
        return SubResult[0]

def MakeFileName(iEntryNum):
    # return the filename matching the given index number

    return "lastquery_" + str(iEntryNum) + ".dat"

def WriteLastQueryFile(form, sFileName):
    # write the contents of the supplied form to a "lastquery_N.dat"
    # formatted file
    sPathName = sDBDir + sFileName

    hOutput = open(sPathName, "w")

    for keyname in form.keys():
        hOutput.write(keyname + "=" + form[keyname].value + "\n")
        
    hOutput.close()

def ReadLastQueryFile(sFileName):
    # read the contents of the specified file
    
    sPathName = sDBDir + sFileName
    hInput = open(sPathName, "r")
    sInput = hInput.read()

    hInput.close()

def ReadEntry(iEntryNum):
    # read the entry with index number iEntryNum
    
    sFileName = MakeFileName(iEntryNum)
    return ReadLastQueryFile(sFileName)

def NewEntry(form, iEntryNum):
    # create a new entry with the specified number
    
    sFileName = MakeFileName(iEntryNum)
    sBadFile = "Error: unable to write file " + sFileName
    
    try:
        WriteLastQueryFile(form, sFileName)
    except:
        raise sBadFile
    
def ModifyEntry(form, iEntryNum):
    # "modify" the specified entry by overwriting its file with
    # the given form data
    
    sFileName = MakeFileName(iEntryNum)
    sBadFile = "Error: unable to write file " + sFileName
    
    try:
        WriteLastQueryFile(form, sFileName)
    except:
        raise sBadFile

def DeleteEntry(iEntryNum):
    # delete the specified entry by zapping its file
    
    sPathName = sDBDir + MakeFileName(iEntryNum)
    sBadFile = "Error: unable to delete file " + sPathName
    try:
        #unlink(sPathName)
        os.remove(sPathName)
    except:
        raise sBadFile

def SafeDeleteEntry(iEntryNum, sExpName):
    # delete the specified entry,
    # but ONLY IF its experiment name matches sExpName
    
    record = cLQRecord(sDBDir + MakeFileName(iEntryNum))
    if sExpName == record.ExpName:
        DeleteEntry(iEntryNum)

def GetEntryNum():
    # search the database directory for the highest-numbered file
    # and return that number plus one
    i = 1
    while os.path.isfile(sDBDir + MakeFileName(i)):
        i = i + 1
    
    return i

def Display(sContent):
    # open the template HTML file and read its contents
    hTemplate = open(sTemplateFile, "r")
    sTemplateInput = hTemplate.read()
    hTemplate.close()
    
    # Error message if we need to throw an exception
    sBadTemplate = "Error processing HTML template."
    
    # Substitute the given content in the proper place
    # within the template
    SubResult = re.subn("<!-- INSERT CONTENT HERE -->", \
                        sContent, sTemplateInput)
    if SubResult[1] == 0:
        raise sBadTemplate
    
    # print a content-type header to let browsers know what flavor
    # of data we are transmitting
    print "Content-type: text/html\n\n"
    
    print SubResult[0]

def TimeWarpError(iType, form, iStartTime, iEndTime):
    # signal the user that an odd relativistic phenomenon has occurred
    
    # output buffer, empty at first
    sOutput = ""
    sOutput = sOutput + "<P>You entered:\n\n"
    sOutput = sOutput + "<P>Starting time:<br>\n"
    sOutput = sOutput + form["startyear"].value + " " \
              + form["startmonth"].value + " " \
              + form["startday"].value + " " + form["starthour"].value \
              + ":" + form["startmin"].value + "\n"
    sOutput = sOutput + "<P>(" + str(iStartTime) + " epoch seconds)\n"
    sOutput = sOutput + "<P>Ending time:<br>\n"
    sOutput = sOutput + form["endyear"].value + " " \
              + form["endmonth"].value + " " \
              + form["endday"].value + " " + form["endhour"].value \
              + ":" + form["endmin"].value + "\n"
    sOutput = sOutput + "<P>(" + str(iEndTime) + " epoch seconds)\n"
    sOutput = sOutput + "<P>WARNING: " + TimeWarpErrors[iType] + "\n" \
              + " (Type " + str(iType) + ")\n" \
              + "<P><a href=\"" +  sCgiURL + "\"" + \
              ">Click here for a new form.</a>\n"
    
    # display the buffer and exit
    Display(sOutput)
    raise SystemExit

def GetEpochTime(sDay, sMonth, sYear, sHour, sMinute, sZone):
    # return the time in seconds since epoch
    sTime = sDay + " " + sMonth + " " + sYear + " " + sHour \
            + ":" + sMinute

    os.environ['TZ'] = sZone
    time.tzset()
    
    return int(time.mktime(time.strptime(sTime, "%d %B %Y %H:%M")))

def EmailText(form):
    # make a human-readable message from the form fields

    # assemble the strings which we'll substitute into the message
    sName = form["name"].value
    sAddress = form["email"].value
    sExperiment = form["expt"].value
    try:
        sStartTime = form["startday"].value + " " \
                     + form["startmonth"].value \
                     + " " + form["startyear"].value + " " \
                     + form["starthour"].value + ":" \
                     + form["startmin"].value
        sEndTime = form["endday"].value + " " + form["endmonth"].value \
                   + " " + form["endyear"].value + " " \
                   + form["endhour"].value + ":" + form["endmin"].value    
        sComment = form["comment"].value
        sColor = form["grade"].value
    except:
        pass

    # decide which course of action to take
    if form["modstatus"].value == "Delete":
        sOutput = "This e-mail has been automagically generated by the SNEWS" \
                  + " downtime coordination website.  " + sName + " (" \
                  + sAddress + ") posted a notification that a downtime" \
                  + " entry belonging to " + sExperiment + " has been"\
                  + " deleted.\n\n"
    else:
        # time zone tomfoolery
        # convert given time to epoch seconds
        startsecs = GetEpochTime(form["startday"].value, \
                                 form["startmonth"].value, \
                                 form["startyear"].value, \
                                 form["starthour"].value, \
                                 form["startmin"].value, \
                                 "UTC")
        endsecs = GetEpochTime(form["endday"].value, \
                               form["endmonth"].value, \
                               form["endyear"].value, \
                               form["endhour"].value, \
                               form["endmin"].value, \
                               "UTC")
        # convert epoch seconds to UTC
        sStartUTC = time.strftime("%a %d %b %Y %H:%M", time.gmtime(startsecs))
        sEndUTC = time.strftime("%a %d %b %Y %H:%M", time.gmtime(endsecs))
        # convert epoch seconds to local time
        os.environ['TZ'] = form["startzone"].value
        time.tzset()
        sStartLocal = time.strftime("%a %d %b %Y %H:%M",
                                    time.localtime(startsecs))
        sEndLocal = time.strftime("%a %d %b %Y %H:%M %Z",
                                  time.localtime(endsecs))

        
        sOutput = "This e-mail has been automagically generated by the SNEWS" \
                  + " downtime coordination website.  " + sName + " (" \
                  + sAddress + ") posted a notification that " + sExperiment \
                  + " will experience downtime from " + sStartUTC + " to " \
                  + sEndUTC + " UTC (" + sStartLocal + " to " + sEndLocal \
                  + ").\n\nThis downtime entry is graded " \
                  + sColor + ".\n\n" + sComment + "\n"
    
    return sOutput

def DisplayTable():
    # create and show a table containing a sorted list of all the
    # entries
    
    # read the template from its file
    hTable = open(sTableFile, "r")
    sTableInput = hTable.read()
    hTable.close()
    
    # create a list to hold our records
    record_list = []
    
    # get the record files's names and store them in a list
    filename_list = os.listdir(sDBDir)
    
    # loop through the filenames and try reading them
    for name in filename_list:
        # we only want to read files of the proper type
        # explanation of regex: \d matches a digit 0-9, + indicates
        # that we must have at least one digit, and \. indicates a literal
        # period (we must escape the . because . is a metacharacter).
        if re.match(r"lastquery_\d+\.dat", name):
            try:
                record_list.append(cLQRecord(sDBDir + name))
            except:
                continue
                #try:
                #    msg = "Unexpected error in proccessing file " \
                #          + name + " " \
                #          + str(sys.exc_info()[0]) \
                #          + " " + str(sys.exc_info()[2])
                #    Display(msg)
                #    return 0
                #except:
                #    msg = "Unexpected error in processing file!"
                #    Display(msg)
                #    return 0
    
    # sort the record list
    # I can't quite grasp the old code's logic, so I'm sorting by
    # starting date (measured in epoch seconds)
    # look in cLQRecord's __cmp__ function for the comparison logic
    record_list.sort()
    
    # generate a table from the sorted records
    sTable = ""
    for record in record_list:
        # only use entries whose end time is later than now
        try:
            if record.EpochEndTime() > int(time.time()):
                sTable = sTable + record.HTML()
        except:
            continue
            
    # make the substitution
    try:
        sSubResult = re.subn("<!-- TABLE CONTENT -->", sTable, sTableInput)
    except:
        sSubResult = "ERROR!"
    
    # display the table on the user's browser
    Display(sSubResult)
    
def DisplayForm():
    # read the form template, process it and display the result
    # so we can gather user input
    
    # read the template from its file
    hForm = open(sFormFile, "r")
    sFormInput = hForm.read()
    hForm.close()
    
    iEntryNum = GetEntryNum()
    sSubResult = re.subn("<!-- DEFAULT ENTRY NUMBER -->", \
                         str(iEntryNum), sFormInput)
    
    # display the form for the user
    Display(sSubResult)

def ProcessForm(form):    
    # extract the information from the form in easily digestible format

    Output = ""  # our output buffer, empty at first
    
    # test for various error scenarios
    try:
        name = form["name"].value
    except:
        # name is required, so output an error if 
        # not given and exit script
        Display("You need to supply a name. Please go back.")
        raise SystemExit
    try:
        email = form["email"].value
    except:
        Display("You don't have an e-mail address?  I don't believe you.")
        raise SystemExit
    if (name == "") or (email == ""):
        Display("Please complete all required fields.")
        raise SystemExit
    
    try:
        iEntryNum = int(form["entry"].value)
    except:
        Display("That is an invalid entry number. Please try again.")
        raise SystemExit
    
    if form["modstatus"].value == "Delete":
        SafeDeleteEntry(iEntryNum, form["expt"].value)
        Output = Output + "<P>Entry number " + str(iEntryNum) \
                 + " was successfully deleted.\n"
    else:
        
        try:
            iStartTime = GetEpochTime(form["startday"].value, \
                                      form["startmonth"].value, \
                                      form["startyear"].value, \
                                      form["starthour"].value, \
                                      form["startmin"].value, \
                                      form["startzone"].value)
        except:
            Display("You must specify a starting time. Please go back.")
            raise SystemExit
        try:
            iEndTime = GetEpochTime(form["endday"].value, \
                                    form["endmonth"].value, \
                                    form["endyear"].value, \
                                    form["endhour"].value, \
                                    form["endmin"].value, \
                                    form["startzone"].value)
        except:
            Display("You must specify an ending time. Please go back.")
            raise SystemExit
    
        if iStartTime > iEndTime:
            TimeWarpError(1, form, iStartTime, iEndTime)
        if iEndTime < int(time.time()):
            TimeWarpError(2, form, iStartTime, iEndTime)

        # convert times to UTC
        form["startday"].value = time.strftime("%d", time.gmtime(iStartTime))
        form["startmonth"].value = time.strftime("%B", time.gmtime(iStartTime))
        form["startyear"].value = time.strftime("%Y", time.gmtime(iStartTime))
        form["starthour"].value = time.strftime("%H", time.gmtime(iStartTime))
        form["endday"].value = time.strftime("%d", time.gmtime(iEndTime))
        form["endmonth"].value = time.strftime("%B", time.gmtime(iEndTime))
        form["endyear"].value = time.strftime("%Y", time.gmtime(iEndTime))
        form["endhour"].value = time.strftime("%H", time.gmtime(iEndTime))
        
        # do something with the collected form data
        if form["modstatus"].value == "New":
            NewEntry(form, iEntryNum)
            Output = Output + "<P>Entry number " + str(iEntryNum) \
                         + " was successfully created.\n"
        elif form["modstatus"].value == "Modify":
            ModifyEntry(form, iEntryNum)
            Output = Output + "<P>Entry number " + str(iEntryNum) \
                     + " was successfully modified.\n"

    # TEMP
        Display(Output)
        raise SystemExit


                
    # end if-not-"Delete" block
    Output = Output + "<P>Click <a href=\"" + sCgiURL + \
             "?key=table\">here</a> for the updated " + \
             "downtime entry table.\n"


    
    # write the current action to the list of all modifications and
    # send an e-mail to snews-downtime with the new entry's specs
    hListAll = open(sDBDir + "list.all", "a")
    p = os.popen("%s -t -i" % SENDMAIL, "w")
    p.write("To: snews-downtime@lists.bnl.gov\n")
    #p.write("To: bstacey@mit.edu\n")
    p.write("Subject: snews-downtime entry %d\n" % iEntryNum)
    p.write("\n")
    
    # turn the form fields into nice text
    p.write(EmailText(form))
    form["startzone"].value = "UTC"
    p.write("\n\n---MACHINE-READABLE---\n\n")
    for name in form.keys():
        hListAll.write(name + "=" + form[name].value + "\n")
        p.write(name + "=" + form[name].value + "\n")
                     
    hListAll.write("\n")
    hListAll.close()
    sts = p.close()
    
    # send the completion message to the user
    Display(Output)

## End of functions

## Execution flow begins here

# evaluate CGI request
try:
    form = cgi.FieldStorage()
except:
    msg = "Unexpected error: " + sys.exc_info()[0]
    Display(msg)
    

# "key" is a hidden form element with an 
# action command such as "process"
try:
    key = form["key"].value
except:
    key = None

# decide whether to display the form requesting data
# or process the data already collected
if key == "process":
    ProcessForm(form)
elif key == "table":
    try:
        DisplayTable()
    except:
        msg = "Unexpected error caught at top level! " \
              + str(sys.exc_info()[0]) \
              + " " + str(sys.exc_info()[2])
        Display(msg)
else:
    DisplayForm()

# Share and enjoy.

