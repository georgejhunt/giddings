#!/usr/bin/env python3
# copy wordpress resources to an "output" dir in curreent directory
# input is wordpress export xml file

import argparse
import xml.etree.ElementTree as ET
import sys,os
import urllib3


# declare namespace
ns = { "wp": "http://wordpress.org/export/1.2/",
      "content":"http://purl.org/rss/1.0/modules/content/"}

# parse the input command line
parser = argparse.ArgumentParser(description='Download wordpress media.')
parser.add_argument( 'filename',
                    help='Specify Wordpress exported xml file.')
parser.add_argument('-l','--list', dest='list', action='store_true',
                    help='Output a list of external urls.')
parser.add_argument('-c','--check', dest='check', action='store_true',
                    help='Perform a survey of items requiring downloading.')
args = parser.parse_args()

# parse the wordpress XML export file
if args.filename:
   tree = ET.parse(args.filename)
else:
   print('No export file specified, and no pipe input. Quitting')
   sys.exit(1)

def dlfile(url):
    # Open the url
    urllib3.disable_warnings()
    try:
       with urllib3.PoolManager() as http:
          r = http.request('GET', url)
          with open(os.path.basename(url), 'wb') as fout:
              fout.write(r.data)
    #handle errors
    except urllib3.exceptions.HTTPError as e:
        print("HTTP Error:", e.code, url)

# put the media in it's own folder, don't polute
directory_name = 'wp_media'
orig_cwd = os.getcwd()
dirn = os.path.join(orig_cwd,directory_name)
if not os.path.basename(orig_cwd) == directory_name:
   if not os.path.exists(dirn):
         os.mkdir(dirn)
   os.chdir(dirn)

root = tree.getroot()
if args.list:
   for child in root.findall(".//item",ns):
      url = child.find("wp:attachment_url",ns)
      if not url is None and len(url) == 0:
         print(url.text)
   os.chdir(orig_cwd)
   sys.exit(0)  

if args.check:
   print("check selected")
   f = []
   for (dirpath, dirnames, filenames) in os.walk(dirn):
       f.extend(filenames)
   download_cnt = present_cnt = 0
   for child in root.findall(".//item",ns):
      url = child.find("wp:attachment_url",ns)
      if not url is None and len(url) == 0:
         if os.path.basename(url.text) not in f:
            download_cnt +=1
         else:
            present_cnt += 1
   print("\nNunber of items already downloaded: %s \n%s will download: %s"%(
            present_cnt,sys.argv[0],download_cnt,))
   os.chdir(orig_cwd)
   sys.exit(0)  

# Do the download of new items
f = []
for (dirpath, dirnames, filenames) in os.walk(dirn):
    f.extend(filenames)
for child in root.findall(".//item",ns):
   url = child.find("wp:attachment_url",ns)
   if not url is None and len(url) == 0:
      if os.path.basename(url.text) not in f:
         print("Downloading %s"%os.path.basename(url.text))
         dlfile(url.text)

# all done, restore original directory
os.chdir(orig_cwd)
