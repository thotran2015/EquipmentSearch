from Result import Result
import unittest
#import the 14 websites
import ebay
import marshallscientific
import equipnet
import google
import medwow
import used_line
import eurekaspot
import labcommerce
import newlifescientific
import labx
import biosurplus
import sci_bay
import dotmed
import sibgene

FUNCTIONS=[biosurplus.extract_results, \
dotmed.extract_results, \
ebay.extract_results, \
equipnet.extract_results, \
eurekaspot.extract_results, \
google.extract_results, \
labcommerce.extract_results, \
labx.extract_results, \
marshallscientific.extract_results, \
medwow.extract_results, \
newlifescientific.extract_results, \
sci_bay.extract_results, \
sibgene.extract_results, \
used_line.extract_results ]


WEBSITE_NAMES={ebay.extract_results : "ebay" , equipnet.extract_results : "equipnet" , google.extract_results : "google" , used_line.extract_results : "used line", \
eurekaspot.extract_results : "eurekaspot", labcommerce.extract_results :"labcommerce", newlifescientific.extract_results :"newlifescientific", biosurplus.extract_results: "biosurplus" , sci_bay.extract_results : "sci_bay", \
dotmed.extract_results : "dotmed" , sibgene.extract_results: "sibgene" , labx.extract_results : "labx", medwow.extract_results: "medwow", marshallscientific.extract_results: \
"marshallscientific"}

'''
If any function throws an error, the test will fail
Otherwise, it will pass
Check manually that these tests print logical outputs
'''
class TestWebScraping(unittest.TestCase):

    def test_blank(self):
    	for func in FUNCTIONS:
    		print "blank test, %s:" %WEBSITE_NAMES[func]
        	print func('', None)

    def test_multiword_biosystems(self):
    	for func in FUNCTIONS:
    		print "applied biosystems 9700, %s:" %WEBSITE_NAMES[func]
        	try:
        		print func('applied biosystems 9700')
        	#ignore error caused by printing unicode
        	except TypeError, e: 
        		if "unicode" not in e.message.lower():
        			raise TypeError(e.message)
        	except UnicodeEncodeError:
        		pass


    def test_multiword_diasorin(self):
    	for func in FUNCTIONS:
    		print "Diasorin Liaison, %s:" %WEBSITE_NAMES[func]
        	try:
        		print func('Diasorin Liaison')
        	except TypeError, e: 
        		if "unicode" not in e.message.lower():
        			raise TypeError(e.message)
        	except UnicodeEncodeError:
        		pass

    def test_multiword_biomek(self):
    	for func in FUNCTIONS:
    		print "Beckman Coulter Biomek Workstation, %s:" %WEBSITE_NAMES[func]
        	try:
        		print func('Beckman Coulter Biomek Workstation')
        	except TypeError, e: 
        		if "unicode" not in e.message.lower():
        			raise TypeError(e.message)
        	except UnicodeEncodeError:
        		pass

    def test_multiword_pump(self):
    	for func in FUNCTIONS:
    		print "Bell and Gossett centrifugal pump, %s:" %WEBSITE_NAMES[func]
        	try:
        		print func('Bell and Gossett centrifugal pump')
        	except TypeError, e: 
        		if "unicode" not in e.message.lower():
        			raise TypeError(e.message)
        	except UnicodeEncodeError:
        		pass

    def test_returns_results(self):
    	for func in FUNCTIONS:
    		print "Test to make sure %s returns results: " %WEBSITE_NAMES[func]
    		results=[]
    		terms=["GenomeLab GeXP", "1200 Series HPLC System", 'Beckman Coulter Biomek Workstation', "Homogenizer Probe", "Sartorius", "Hair Removal Laser"]
    		for search_term in terms:
    			print search_term
        		results.extend(func(search_term))
        		if len(results)>0:
        			break
        	if len(results)==0:
        		self.fail(WEBSITE_NAMES[func] + " does not return any results.")

if __name__ == '__main__':
    unittest.main()