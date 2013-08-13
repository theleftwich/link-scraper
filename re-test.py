import re

url = 'https://docs.google.com/a/umich.edu/spreadsheet/ccc?key=0AinMDATKswMWdGJraFQtRTBMSWt3bFgzRjV4clZuNUE#gid=1'

key_ex = re.compile('key=([^#]*)')		
spreadsheet_key = re.findall(key_ex,url)

print spreadsheet_key
#spreadsheet_key = fieldValues[1].match(key_ex)
# (/key=([^#]*)/)[1];