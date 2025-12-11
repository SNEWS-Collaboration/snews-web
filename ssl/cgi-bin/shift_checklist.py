#!/usr/bin/python

# Shift checklist, based on Blake's downtime script


# Modules we import for needed functionality
import cgi
import string
import math
import re
import os
import os.path
import time


# Note my trademark usage of excessive Hungarian notation.
sHomeDir = "/srv/wwwhosts/snews.bnl.gov/shift-data"
sDBDir = os.path.join(sHomeDir, "db")
sShiftLogFile = os.path.join(sHomeDir, "logfile.html")
sShiftEmailFile = os.path.join(sHomeDir, "remindme")

sSnnetURL = "https://snews.bnl.gov"
sTemplateFile = "shift_template.html"
sFormFile = "shift_checklist-template.html"

# SENDMAIL = "/usr/sbin/sendmail"

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
    print( "Content-type: text/html\n\n")
    
    print( SubResult[0])

def DisplayForm():
    # read the form template, process it and display the result
    # so we can gather user input
    
    # read the template from its file
    hForm = open(sFormFile, "r")
    sFormInput = hForm.read()
    hForm.close()
    
    # display the form for the user
    Display(sFormInput)

def ProcessForm(form):    
    # extract the information from the form in easily digestible format

    Output = ""  # our output buffer, empty at first
    
    # test for various error scenarios 
    name = form["name"].value


    if (name == ""):
        # name is required, so output an error if 
        # not given and exit script
        Display("You need to supply a name. Please go back.")
        raise SystemExit

    email2 = form["email2"].value
    if (email2 == ""):
        try:
            email = form["email"].value
        except:
            Display("You need to supply an email address. Please go back")
            raise SystemExit
    else:
        email=email2
    

#    year = form["year"].value
#    month = form["month"].value
#    day = form["day"].value
#    hour = form["hour"].value
#    min = form["min"].value

    
    
    serverok = form["serverok"].value

    logcheck = form["logcheck"].value

    pingcheck = form["pingcheck"].value

    bserverok = form["bserverok"].value

    blogcheck = form["blogcheck"].value

    bpingcheck = form["bpingcheck"].value

#    estarcheck = form["estarcheck"].value

    commcheck = form["commcheck"].value

    notes = form["notes"].value


    # Display the stuff
    Output = Output + "<b>Shifter name: </b>"+name+"&nbsp &nbsp  " 
    Output = Output + "<b>Email will be sent to: </b>"+email+"&nbsp &nbsp  " 
#    Output = Output + "<P>Time of check:  "+month+" "+day+" "+year+" "+hour+":"+min+"\n"
    Output = Output + "<b>Time: </b>"+ time.asctime(time.localtime(time.time()))+"<br>"
    Output = Output + " <b>Server OK: </b>"+serverok+" &nbsp"
    Output = Output + " <b>Log checked: </b>"+logcheck+" &nbsp"
    Output = Output + " <b>Ping check OK: </b>"+pingcheck+" &nbsp"
    Output = Output + " <b>Backup server OK: </b>"+bserverok+" &nbsp"
    Output = Output + " <b>Backup server log checked: </b>"+blogcheck+" &nbsp"
    Output = Output + " <b>Backup server ping check OK: </b>"+bpingcheck+" &nbsp"
#    Output = Output + " <b>Estar check OK: </b>"+estarcheck+" &nbsp"
    Output = Output + " <b>Comm checked: </b>"+commcheck+"<br>"
    Output = Output + " <b>Notes: </b>"+notes+"<br>"
    Output = Output + "----------------------------------------------------------------<br>"

    # Now append the stuff to the log file
    hShiftLog = open(sShiftLogFile,"a")
    hShiftLog.write(Output)
    hShiftLog.close()

    # Now put email in file for reminders
    hShiftEmail = open(sShiftEmailFile,"w")
    hShiftEmail.write(email)
    hShiftEmail.close()

    
    # send the completion message to the user
    Display(Output)


## End of functions

## Execution flow begins here

# evaluate CGI request
form = cgi.FieldStorage()

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
else:
    DisplayForm()

# Share and enjoy.

