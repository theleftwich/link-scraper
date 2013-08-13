import easygui as eg

msg         = "This program will grab links from the body and sidebars, test them, and store the information in a CSV in the C:\scraper directory."
title       = "Link Scraper/Tester v. 0.5"
fieldNames  = ["Google Docs Spreadsheet URL","U-M email address","Name of output file (must end in .csv)","CMS Password"]
fieldValues = []  # we start with blanks for the values
fieldValues = eg.multpasswordbox(msg,title, fieldNames)

# make sure that none of the fields was left blank
while 1:  # do forever, until we find acceptable values and break out
    errmsg = ""
    if fieldValues == None: 
        break

    
    # look for errors in the returned values
    for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        
    if errmsg == "": 
        break # no problems found
    else:
        # show the box again, with the errmsg as the message    
        fieldValues = eg.multenterbox(errmsg, title, fieldNames, fieldValues)
    
print ("Reply was:", fieldValues)

#fieldValues is a list, can access with fieldValues[0] etc.

