from api import search

books = search(title='the view from saturday', author='konigsburg')

print "Here are all of the versions available:"
for book in books:
	print book.title

print "\nHere is the second result in more detail:\n",books[1]

print "\nHere are all of the copies of that book:\n"
for copy in books[1].copies:
	print copy

print "\nThese are the ones that are available:\n"
for copy in books[1].available_copies:
	print copy

#this refreshes the copies available
books[1].update_copies()

print "We just refreshed the results. Here are the new ones:\n"
for copy in books[1].copies:
	print copy

print "Did they change? Probably not, unless someone just returned a book!"
