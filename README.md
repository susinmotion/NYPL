NYPL API 
=========
An unofficial API for the New York Public Library Catalog




Dependencies
-----------

 - requests (pip install requests)
 - BeautifulSoup4 (pip install beautifulsoup4)

Installation
--------------

```sh
pip install NYPL_API


```


Use
----
```sh
>>> from NYPL import search
>>> search(title="The View from Saturday", author="E.L. Konigsburg")
[<Book instance: The View From Saturday (Downloadable Audiobook)>, <Book instance: The View From Saturday (Paperback)>, <Book instance: The View From Saturday (Book)>, <Book instance: The View From Saturday (Audiobook CD)>, <Book instance: The View From Saturday (Book)>]
```

Sample
---
see example.py

Output
---
Results are output as a list of Book objects, which have the following attributes:
 - author
 - title (in the format "title (genre)" )
 - link_to_copies (url to a page of the libraries that have the book) 
 - copies (a list of all copies of the book) \* 
 - available_copies (a list of *available* copies of the book)  \* 
 
copies and available_copies are represented as lists of Copy objects, which have the following attributes:
 - location (eg. "96th Street")
 - collection (eg. "96th Street Children's Fiction")
 - callNo (call number, eg. "J FIC K"
 - status (eg. "DUE 10-28-14")
 






\* copies and available copies are not generated automatically with default search. They can be generated automatically with robust search:
```
search(keyword, title, author, lazy=False)
```

More Info
--------

Unfortunately, the official New York Public Library is only available to library employees, and during library hack-a-thons. Now, it's data anytime--Happy developing!

Feedback is most welcome.
https://github.com/susinmotion/NYPL_API