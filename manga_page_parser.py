# Parses manga's info page

import xml.etree.ElementTree as ET

import utils

class MangaPageParser:
  tree = None
  
  def __init__(self, url):
    self.tree = ET.ElementTree(ET.XML(utils.download_html(url), utils.xml_parser()))
  
  def get_page_count(self):
    page_list = self.tree.findall(".//xhtml:select[@id='pageMenu']/xhtml:option", utils.namespaces)
    return len(page_list)
  
  def get_image_url(self):
    return self.tree.find(".//xhtml:img[@id='img']", utils.namespaces).get("src")