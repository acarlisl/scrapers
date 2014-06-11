#!/usr/bin/python

""" Site scraper for casualvillain.com to make the comics clickable pages.
"""

from BeautifulSoup import BeautifulSoup as bs
import requests

def main():
    # Scrape all the comic data. There are 9 chapters with < 150 pages each
    comic = {}
    for chapter in range(10):
      for page in [str(x).zfill(2) for x in range(150)]:
        try:
            res = requests.get('http://www.casualvillain.com/Unsounded/comic/ch0%d/ch0%d_%s.html' % (chapter, chapter, page))
            if res.ok:
               quiet = comic.setdefault(chapter, {})
               comic[chapter][int(page)] = res.content
        except:
            continue

    # I know that since the indexes are ints, they are likely to be in order,
    # but sorting to be on the safe side.
    chapters = comic.keys()
    chapters.sort()

    for chapter in chapters:
        data = comic[chapter]
        pages = data.keys()
        pages.sort()
        if len(pages) != max(pages):
            print 'Missing pages from chapter %d' % chapter
        for page in pages:
            try:
                page_data = data[page]
                soup=bs(page_data)
                this_page = 'ch%s_%s.html' % (
                        str(chapter).zfill(2), str(page).zfill(2))
                try:
                    next_link = soup.findAll("a", { "class" : "forward" })[0]['href']
                except:
                    # At the end of chapters there is no link.
                    next_link = 'ch%s_%s.html' % (
                        str(chapter+1).zfill(2), str(1).zfill(2))
                comic_element = soup.find("div", {"id": "comic"}).find('img')
                link_soup = bs('<a href="%s">' % next_link)
                link_soup.find('a').insert(0, comic_element.extract())
                soup.find("div", {"id": "comic"}).insert(0, link_soup)
                prettyHTML=soup.prettify()
                with open(this_page, 'w') as f:
                    print >> f, prettyHTML
            except Exception as exc:
                print 'Bad chapter %d page %d %s' %(chapter, page, repr(exc))

if __name__ == '__main__':
    main()
