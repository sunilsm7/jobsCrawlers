import selenium.webdriver as webdriver
import csv


def test_write_csv_file(search_term, results):
    myFile = open('csv-write-data.csv', 'w')
    with myFile:
        writer = csv.writer(myFile, delimiter=',')
        header = [search_term, 'job title', 'url']
        writer.writerow(i for i in header)
        writer.writerows(results)


def get_results(search_term):
    url = 'https://www.indeed.co.uk/advanced_search?q={}&l=&radius=50'.format(search_term)
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
    # query.send_keys(search_term)
    results_limit.send_keys(50)
    sort_by.send_keys('date')
    fromage.send_keys('7')
    search_form.submit()

    links = browser.find_elements_by_css_selector("div.jobsearch-SerpJobCard>div.title>a")                                 
 
    results = []

    for link in links:
        href = link.get_attribute('href')
        job_title = link.get_attribute('text')
        job_post = [search_term, job_title, href]
        print(job_post)
        results.append(job_post)
    browser.close()
    test_write_csv_file(search_term, results)
    return results

get_results('python developer')