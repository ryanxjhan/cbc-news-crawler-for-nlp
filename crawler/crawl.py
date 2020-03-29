from bs4 import BeautifulSoup
from newsplease import NewsPlease
from newspaper import Article
import pandas as pd

def crawl(input_path, output_path):

    links = pd.read_csv(input_path)
    links.columns = ['links']
    data = pd.DataFrame(columns=('authors', 'title',
                                'publish_date', 'description', 'text',
                                'url'))

    failed = 0

    for i, link in enumerate(links.links):
        try:
            a = Article(link)
            a.download()
            a.parse()
            soup = BeautifulSoup(a.html, 'html.parser')
            text = soup.find("div", "story").get_text()
            article = NewsPlease.from_url(link)
        except Exception as e:
            print('{}\n'.format(e))
            failed += 1
            print('Getting news failed #{}\n'.format(str(failed)))
            continue

        row = [a.authors, a.title,
            article.date_publish,
            article.description,
            text,
            link]

        print('> Getting news #{}...\n'.format(str(i)))
        print(row[:4])
        data.loc[i] = row

    print('* Failed: {} Percentage: {} *'.format(str(failed), str(failed/len(links))))
    print('* Success: {}, Percentage: {} *'.format(
        str(len(data)), str(len(data)/len(links))))
    data.to_csv(output_path, header=True)

if __name__ == "__main__":

    crawl('links.txt', 'news.csv')