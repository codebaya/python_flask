from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from extractors.wwr import extract_jobs

options = Options()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# driver.get("https://www.indeed.com/jobs?q=python&l=New%20York%2C%20NY&vjk=9e585184979e06fe")

def get_page_count(keyword):
    base_url = "https://indeed.com/jobs?q="
    # search_term = "python"
    tails = "&l=&from=searchOnHP&vjk=1015284880e2ff62"
    driver.get(f"{base_url}{keyword}&start=0{tails}")
    response = driver.page_source

    soup = BeautifulSoup(response, "html.parser")
    pagination = soup.find("nav", class_="css-jbuxu0")
    if pagination == None:
        pagination = soup.find("ul", class_="pagination-list")
        count = page_list(pagination, "li")
        return count

        if pagination == None:
            return 1

    count = page_list(pagination, "div")
    return count

def page_list(pagination, props):
    pages = pagination.find_all(f"{props}", recursive=False)
    print(f"pages : {props} : {pages} ")

    count = int(pages[-2].string)
    # print(f"pages {props} : ", pages[-2].string)
    # return count
    # count = len(pages)
    if count >= 5:
        return 5
    else:
        return count


# print(get_page_count("python"))

# https://kr.indeed.com/jobs?q=python&start=10&pp=gQAPAAABgzTh2VcAAAAB5PlkhwAnAQAXbEUdrPeMA45_qpZvWSrVVv2e1FR1a_fOmbWel970fLwAlGxGAAA&vjk=207c600998e380be
def extract_indeed_jobs(keyword):
    results = []
    pages = get_page_count(keyword)
    # pages = 15
    for page in range(pages):

        base_url = "https://indeed.com/jobs?q="
        domain_url = "https://www.indeed.com"
        # search_term = "python"

        tails = "&l=&from=searchOnHP&vjk=1015284880e2ff62"
        final_url = f"{base_url}{keyword}&start={page*10}{tails}"
        print(final_url)
        driver.get(final_url)
        response = driver.page_source

        soup = BeautifulSoup(response, "html.parser")
        job_list = soup.find("ul", class_ = "jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                # h2 = job.find("h2", class_="jobTitle")
                anchor = job.select_one("h2 a")
                salary = job.select_one("div", class_="attribute_snippet")
                # print("salary : ", salary)
                title = anchor.find("span").string
                link = domain_url + anchor["href"]
                # print("link : ", link)
                company = job.find("span", class_="companyName").text
                location = job.find("div", class_="companyLocation").string
                if location == None:
                    location = "Everywhere"
                job_data = {
                    "position": title.replace(",", " "),
                    "company": company.replace(",", " "),
                    "location": location.replace(",", " "),
                    "link": link,
                }

                results.append(job_data)

    return results

# result = extract_indeed_jobs("python")
# print(result)
