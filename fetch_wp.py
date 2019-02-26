#!/usr/bin/env python
# copy wordpress resources to an "output" dir in curreent directory
# input is wordpress export xml file

import argparse
import xml.etree.ElementTree as ET
import sys,os
import urllib2

# declare namespace
ns = { "wp": "http://wordpress.org/export/1.2/",
      "content":"http://purl.org/rss/1.0/modules/content/"}

parser = argparse.ArgumentParser(description='Download wordpress media.')
parser.add_argument( 'filename',
                    help='Wordpress exported xml file ')
parser.add_argument('--list', dest='list', action='store_false',
                    help='Wordpress exported xml file (default: pipe input)')
args = parser.parse_args()

if args.filename:
   tree = ET.parse(args.filename)
else:
   print('No export file specified, and no pipe input. Quitting')
   sys.exit(1)
if args.list:
   #print('listing selected')
   root = tree.getroot()
   #print(str(root.nsmap))
   #for child in root.findall(".//item",root.nsmap):
   for child in root.findall(".//item",ns):
      url = child.find("wp:attachment_url",ns)
      if not url is None and len(url) == 0:
         print(url.text)
