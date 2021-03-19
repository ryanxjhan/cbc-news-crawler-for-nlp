from crawler import crawl
from crawler import getlinks

keywords = ['asian']
num_of_news = 5918
links_path = 'links.txt'
news_path = 'news.txt'

if __name__ == "__main__":
    
    finished = []
    for keyword in keywords:

        getlinks.getlinks(keyword, num_of_news, links_path)
        crawl.crawl(links_path, news_path)
        
        finished.append(keyword)
        print('---------------\n')
        print('Finished crawling keyword(s): {}'.format(str(finished)))