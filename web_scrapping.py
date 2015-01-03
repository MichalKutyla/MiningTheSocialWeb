import urllib
import urllib.request
from bs4 import BeautifulSoup

# Try http://ajaxian.com
URL = "http://ajaxian.com"

try:
	page = urllib.request.urlopen(URL)
except urllib.error.URLError:
	print('Failed to fetch ' + item)

soup = BeautifulSoup(page)

anchorTags = soup.findAll('a')

for a in anchorTags:
	if a.has_attr('rel'):
		tags = a['rel']
		print(a.contents[0], a['href'], tags)