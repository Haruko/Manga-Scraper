from manga_info_parser import MangaInfoParser
from manga_page_parser import MangaPageParser
import utils

from math import floor, log10

def main():
  base_url = get_manga_base_url()
  
  manga_info_parser = MangaInfoParser(base_url)
  
  print("\n\n----------\n")
  
  manga_name = manga_info_parser.get_manga_name() # Name of manga
  chapter_count = manga_info_parser.get_chapter_count() # Number of chapters in manga
  print(manga_name)
  print(str(chapter_count) + " Chapters")
  
  print("\n----------\n")
  
  page_counts = get_page_counts(base_url, chapter_count)
  image_urls = get_image_urls(base_url, page_counts)
  
  utils.download_images(manga_name, page_counts, image_urls)

def get_manga_base_url():
  print("Input manga's base URL: ")
  return input().strip("/")

# Returns a list of page counts for every chapter
def get_page_counts(base_url, chapter_count):
  page_counts = [-1] # Chapters are 1-indexed but lists are 0-indexed
  for chapter in range(1, chapter_count + 1):
    chapter_url = "{0}/{1}".format(base_url, chapter) # Create chapter url
    chapter_parser = MangaPageParser(chapter_url) # Parse the chapter page
    page_counts.append(chapter_parser.get_page_count()) # Get the page count for that chapter
  return page_counts

# Returns a list with each element being a list of page URLs for that chapter
def get_image_urls(base_url, page_counts):
  image_urls = [[-1]]
  for chapter in range(1, len(page_counts)):
    chapter_image_urls = [-1] # Pages are 1-indexed but lists are 0-indexed
    for page in range(1, page_counts[chapter] + 1): # +1 to include final page
      page_url = "{0}/{1}/{2}".format(base_url, chapter, page) # Create page url
      page_parser = MangaPageParser(page_url) # Parse the page
      chapter_image_urls.append(page_parser.get_image_url()) # Get the image url for that page
    image_urls.append(chapter_image_urls)
    print("Chapter {0} urls parsed.".format(chapter))
  return image_urls

if __name__ == "__main__":
  main()