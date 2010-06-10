from HTMLParser import HTMLParser
from urllib2 import urlopen

import xml.sax.handler
import pprint

class MyHTMLParser(HTMLParser):

	def __init__(self, url):
		HTMLParser.__init__(self)
		req = urlopen(url)
		self.feed(req.read())
            
	def handle_starttag(self, tag, attrs):
		if tag == 'td':
			for attr,val in attrs:
				if attr == 'class' and val.startswith('qcm'):		
					print attr + ' ' + val

	def handle_endtag(self, tag):		
		print "Encountered the end of a %s tag" % tag

myhtml = MyHTMLParser('file:///Users/Jeje/Documents/Django_Projects/UniformZulu/qcm_correction_reglementation.html')

class QCMHandler(xml.sax.handler.ContentHandler):

	def startElement(self, name, attributes):
		if name == 'td':
			self.tdclass = attributes['class']
	
#parser = xml.sax.make_parser()
#handler = QCMHandler()
#parser.setContentHandler(handler)
#parser.parse('/Users/Jeje/Documents/Django_Projects/UniformZulu/qcm_correction_reglementation.html')
#pprint.pprint(handler.mapping)