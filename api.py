import requests, re
from bs4 import BeautifulSoup

class Book:
	def __init__(self, title, author=None, link_to_copies=None):
		self.title = title
		self.author = author
		self.link_to_copies = link_to_copies
		self._copies = None

	def __str__(self):
		returnString = "title: %s\n author: %s\n" % (self.title.encode("utf8"),self.author)
		if self.copies is not None:
			returnString = returnString + "availability:\n\t"
			for copy in self.copies:
				returnString = returnString + "\n\t".join(str(copy).split("\n"))

		return returnString + "\n"
	
	def __repr__(self):
		return "<Book instance: %s>" % (self.title.encode("utf8"))
	
	def update_copies(self):
		if not self.link_to_copies:
			self._copies = []
		else:
			self._copies = get_copies(self.link_to_copies)
	
	@property
	def copies(self):
		if self._copies == None:
			self.update_copies()

		return self._copies

	@property
	def available_copies(self):
		return [copy for copy in self.copies if copy.status == "Available"]


class Copy:
	def __init__(self, location=None, collection=None, callNo=None, status=None):
		self.location = location
		self.collection = collection
		self.callNo = callNo
		self.status = status

	def __str__(self):
		returnString = "location: " + self.location + "\ncollection: " + self.collection + "\ncall number: " + self.callNo + "\nstatus: " + self.status
		return returnString + "\n"
	
	def __repr__(self):
		return "Copy at %s" % self.location
	


def get_source (url):
	#return content from a url as a BeautifulSoup object
	r = requests.get(url)
	source_code = r.content
	pretty_source_code = BeautifulSoup(source_code)
	return pretty_source_code


def create_search_url(keyword=None, author=None, title=None):
	#create search URL for catalog from at least one keyword, title or author
	url = "http://nypl.bibliocommons.com/search?custom_query=%28"
	if keyword:
		url = url + "anywhere%3A(" + keyword + ") AND "

	if author:
		url = url + "contributor%3A(" + author + ") AND "

	if title:
		url = url + "title%3A(" + title 

	url = url + "%29%20%29&suppress=true&custom_edit=false"
	return url

def get_title_author_av(pretty_source_code, lazy):
	#from the source code, extract books
	blocks = pretty_source_code.findAll(id = re.compile("bib\d"))
	bookslist = []
	title = None
	author = None
	copies = None
	link_to_copies = None

	for items in blocks:		
		title = items.find(testid = "bib_link").get("title")
		has_author = items.find(testid = "author_search")
		if has_author:
			author=has_author.get("title")
		has_link=items.find(testid = "availability_details")
		if has_link:
			link_to_copies = "http://nypl.bibliocommons.com/" + has_link.get("href")
		book = Book(title, author, link_to_copies)

		if not lazy:
			book.update_copies()		

		bookslist.append(book)

	return bookslist

def get_copies(url):

	libraries = get_source(url).findAll("tr")
	copies = []
	for library in libraries:
		locations = library.findAll(testid = "item_branch_name")
		collections = library.findAll(testid = "item_collection")
		callNos = library.findAll(testid = "item_call_number")
		statuses = library.findAll(testid = "item_status")
		for i in range(len(locations)):
			if locations[i]:
				location = locations[i].text.strip()
				collection = collections[i].text.strip()
				callNo = callNos[i].text.strip()
				status = statuses[i].text.strip()

				copy = Copy(location,collection,callNo,status)
				copies.append(copy)

	return copies

def search(keyword = None, author = None, title = None, lazy=True):
	""" Searches library catalog. Returns the first 10 results.

	You must supply at least one of keyword, author or title
	Results are in the format: title (format), author[, availability]
	If lazy is False, results include availability information."""

	url = create_search_url(keyword, author, title)
	books = get_title_author_av(get_source(url), lazy)
	return books
