# Utilities used by multiple files.

from html.entities import html5 as html5entities
from math import floor, log10
import mimetypes
import os
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

namespaces = {'xhtml': 'http://www.w3.org/1999/xhtml'}

# Need a new parser each time we want to parse a page
def xml_parser():
  xmlparser = ET.XMLParser()
  for entity in html5entities:
    xmlparser.entity[entity] = html5entities[entity]
  return xmlparser

# Returns all html from a page
def download_html(url):
  with urlopen(url) as response:
    raw = response.read()
    html = raw.decode('utf-8', 'ignore')
    return html

def download_images(manga_name, page_counts, image_urls):
  manga_name = validate_ntfs_path(manga_name) # Remove colons and such
  chapter_padding = 1 + floor(log10(len(page_counts) - 1)) # Uniform padding throughout all chapters
  page_padding = 1 + floor(log10(max(page_counts) - 1)) # Uniform padding throughout all chapters
  for chapter in range(1, len(page_counts)):
    padded_chapter = str(chapter).zfill(chapter_padding)
    dir_path = os.path.join(os.getcwd(), "downloads", validate_ntfs_path(manga_name), "Chapter {0}".format(padded_chapter))
    os.makedirs(dir_path, exist_ok=True) # Ensure directories exist
    for page in range(1, page_counts[chapter] + 1): # +1 to include final page
      padded_page = str(page).zfill(page_padding)
      file_name = "c{0}p{1}".format(padded_chapter, padded_page)
      download_image(dir_path, file_name, image_urls[chapter][page])
      

def download_image(dir_path, file_name, image_url):
  request = Request(image_url, headers={'User-Agent': "Mozilla"}) # Give user agent to keep from getting blocked
  try:
    with urlopen(request) as response:
      extension = get_image_extension(response.headers['content-type'])
      file_name = "{0}{1}".format(file_name, extension)
      file_path = os.path.join(dir_path, file_name)
      if not os.path.isfile(file_path):
        with open(file_path, 'wb') as out_file:
          out_file.write(response.read())
        print("Downloaded {0}".format(file_name))
  except HTTPError as http_error:
    error_path = os.path.join(dir_path, os.path.pardir, "errors")
    with open(error_path, 'a') as error_file:
      error_file.write("Could not download {0} at {1}\n".format(file_name, image_url))

def get_image_extension(content_type):
  extension = mimetypes.guess_extension(content_type)
  if extension == ".jpe": # image/jpeg will give .jpe as the extension because why not
    extension = ".jpg"
  return extension

def validate_ntfs_path(pathstring):
  return re.sub("[<>:/\\|?*\"]|[\0-\31]", "", pathstring)