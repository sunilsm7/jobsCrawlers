import selenium.webdriver as webdriver
import csv
import pandas as pd


BASE_URL = 'https://www.indeed.co.uk/advanced_search?q={}&l={}&radius=50'
CSV_URL = ''


class IndeedCrawlerException(Exception):
    pass


class IndeedCrawler:
    """
    Crawler to get jobs results from indeed.
    """

    def __init__(self):
        self.base_url = BASE_URL
        self.csv_url = CSV_URL
        self.keywords = None
        self.results = []

    def write_csv_file(self, results):
        myFile = open('crawler_indeed.csv', 'w')
        with myFile:
            writer = csv.writer(myFile, delimiter=',')
            header = ['keyword', 'job title', 'url']
            writer.writerow(i for i in header)
            writer.writerows(results)

    def read_keywords_csv(self):
        """
        read keywords csv file
        """
        data = pd.read_csv("keywords.csv")

        self.keywords = data
        return self.keywords

    def crawl(self):
        data_frame = self.read_keywords_csv()

        # iterating over rows using iterrows() function  
        for index, item in data_frame.iterrows(): 
            keyword = item['keyword']
            location = item['location']
            self.parse_keyword(keyword, location)

        # write results to file
        self.write_csv_file(self.results)

    def parse_keyword(self, search_query, location_query):
        url = self.base_url.format(search_query, location_query)
        browser = webdriver.Chrome()
        browser.get(url)
        search_form = browser.find_element_by_name('sf')
        query = browser.find_element_by_name('as_and')
        location = browser.find_element_by_id('where')
        results_limit = browser.find_element_by_id('limit')
        sort_by = browser.find_element_by_id('sort')
        norecruiters = browser.find_element_by_id('norecruiters').click()
        fromage = browser.find_element_by_id('fromage')
        # modify search

        results_limit.send_keys(50)
        sort_by.send_keys('date')
        fromage.send_keys('7')
        search_form.submit()

        links = browser.find_elements_by_css_selector("div.jobsearch-SerpJobCard>div.title>a")                                 
        local_result = []
        for link in links:
            href = link.get_attribute('href')
            job_title = link.get_attribute('text')
            job_post = [search_query, job_title, href]
            self.results.append(job_post)
        browser.close()
        return local_result


def main():
    indeed_crawler = IndeedCrawler()
    indeed_crawler.crawl()


if __name__ == '__main__':
    main()