# Parses manga's info page

import xml.etree.ElementTree as ET

import utils

class MangaInfoParser:
  tree = None
  manga_name = None
  chapter_count = None
  
  def __init__(self, url):
    self.tree = ET.ElementTree(ET.XML(utils.download_html(url), utils.xml_parser()))
    
  
  def get_manga_name(self):
    if self.manga_name == None:
      self.manga_name = self.tree.findall(".//xhtml:h2[@class='aname']", utils.namespaces)[0].text
    return self.manga_name
  
  def get_chapter_count(self):
    if self.chapter_count == None:
      chapter_list = self.tree.findall(".//xhtml:div[@id='chapterlist']//xhtml:div[@class='chico_manga']", utils.namespaces)
      self.chapter_count = len(chapter_list)
    return self.chapter_count