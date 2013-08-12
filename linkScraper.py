
# Current state of this script
# This script is able to log in to the CMS and will get all links matching
# certain criteria from div#content and div#rightPortlets and write them 
# to a CSV

# don't forget to specify email addres for logging into Google Docs, paths and filenames to store your CSV!

###############################################################################

#get urls to scrape
import re, urllib, urllib2

# Download Google spreadsheet
class Spreadsheet(object):
    def __init__(self, key):
        super(Spreadsheet, self).__init__()
        self.key = key

class Client(object):
    def __init__(self, email, password):
        super(Client, self).__init__()
        self.email = email
        self.password = password

    def _get_auth_token(self, email, password, source, service):
        url = "https://www.google.com/accounts/ClientLogin"
        params = {
            "Email": email, "Passwd": password,
            "service": service,
            "accountType": "HOSTED_OR_GOOGLE",
            "source": source
        }
        req = urllib2.Request(url, urllib.urlencode(params))
        return re.findall(r"Auth=(.*)", urllib2.urlopen(req).read())[0]

    def get_auth_token(self):
        source = type(self).__name__
        return self._get_auth_token(self.email, self.password, source, service="wise")

    def download(self, spreadsheet, gid=1, format="csv"):
        url_format = "https://spreadsheets.google.com/feeds/download/spreadsheets/Export?key=%s&exportFormat=%s&gid=%i"
        headers = {
            "Authorization": "GoogleLogin auth=" + self.get_auth_token(),
            "GData-Version": "3.0"
        }
        req = urllib2.Request(url_format % (spreadsheet.key, format, gid), headers=headers)
        return urllib2.urlopen(req)

if __name__ == "__main__":
    import getpass
    import csv

    print "\n"
    print ">>>> First, the script will log in to Google Docs.\n"
    email = raw_input('Please enter your Google Docs email address (e.g., leftwich@umich.edu)\nEmail: ')
    print "\n"
    print "Now enter your Google Docs password at the prompt."
    password = getpass.getpass()
	
    spreadsheet_id = "0AinMDATKswMWdGJraFQtRTBMSWt3bFgzRjV4clZuNUE" # (spreadsheet id here)

    # Create client and spreadsheet objects
    gs = Client(email, password)
    ss = Spreadsheet(spreadsheet_id)

    # Request a file-like object containing the spreadsheet's contents
    csv_file = gs.download(ss)



# login to CMS
import mechanize
import cookielib
from bs4 import BeautifulSoup

#initialize variables...
error_code = "ok"
error_args = "ok"

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# The site we will navigate into, handling it's session
br.open('https://weblogin.umich.edu/')

# Select the first (index zero) form
br.select_form(nr=0)

# User credentials
br.form['login'] = 'leftwich' #umich login
print "\n"
print ">>>> Now, the script will log in to the CMS.\n"
br.form['login'] = raw_input('Please enter your CMS login name (e.g., leftwich):\nLogin: ')
print "\n"
print "Please enter your CMS password at the prompt."
br.form['password'] = getpass.getpass()


# Submit login
br.submit()


# Output
# specify path to file and file variables
from os.path import join as pjoin
path_to_folder = pjoin('C:\\', 'Users', 'leftwich', 'Documents', 'scraper')
filename = 'scraper03_test.csv'

# open a file to write results in
outputFile = open(path_to_folder + '\\' + filename, 'a')


# now scrape for links
# imports		
import csv 
import urllib2
import re

# Get urls from csv object we just downloaded and start loop
urls = csv.reader(csv_file)


# Open each page from Google Docs csv, read contents
for url in urls:
    response = br.open(url[0])
    fullHTML = response.read()
	
	# put the HTML into BeautifulSoup
    soup = BeautifulSoup(fullHTML)

	
	# zoom in to div#content, get content and store
    content_div = soup.find('div',attrs={'id':'contentHolder'})
	
	
	# zoom in to div#rightPortlets, get content and store
    portlet_div = soup.find('div',attrs={'id':'rightPortlets'})
	

	# get all the links from div#content, write each to a line of a .csv file
    if content_div is not None:
        for link in content_div.findAll('a'):
            h = link.get('href')
            if h is not None and h.startswith('#')==False and 'mailto' not in h:
			    #follow link and check for 404s or server errors
                if h.startswith("/"):
                    fullURL = ('http://www.engin.umich.edu' + h)
                else:
                    fullURL = h
    
                try:		
                    pageResponse = br.open(fullURL)
				
                except (mechanize.HTTPError,mechanize.URLError) as e:
                    if isinstance(e,mechanize.HTTPError):
                        error_code = str(e.code)
                    else:
                        error_args = str(e.reason.args)
                        						
                
                outputFile.write ('"' + (url[0]) + '","' + link.get('href')  + '","' + error_code + '","' + error_args + '"' + '\n')
	

	
	# get all the links from div#rightPortlets, write each to a line of a .csv file
    if portlet_div is not None:
        for link in content_div.findAll('a'):
            h = link.get('href')
            if h is not None and h.startswith('#')==False and 'mailto' not in h:
			    #follow link and check for 404s or server errors
                if h.startswith("/"):
                    fullURL = ('http://www.engin.umich.edu' + h)
                else:
                    fullURL = h
    
                try:		
                    pageResponse = br.open(fullURL)
				
                except (mechanize.HTTPError,mechanize.URLError) as e:
                    if isinstance(e,mechanize.HTTPError):
                        error_code = str(e.code)
                    else:
                        error_args = str(e.reason.args)
                        						
                #write source url, link url, error code, error arg
                outputFile.write ('"' + (url[0]) + '","' + link.get('href')  + '","' + error_code + '","' + error_args + '"' + '\n')
				
    
	

outputFile.close()    

