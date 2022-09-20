from requests import get
from bs4 import BeautifulSoup


def extract_jobs(keyword) :

    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    domain_url = "https://weworkremotely.com"

    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find_all("section", class_="jobs")
        # print(len(jobs))
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = domain_url + anchor['href']
                company, kind, region = anchor.find_all('span', class_="company")
                # print(f"region {region}.string")
                if region == None:
                    region = "anywhere"
                # print("region : ", region)
                title = anchor.find('span', class_="title")
                # print(company.string, kind.string, region.string, title.string)
                job_data = {
                    'position': title.string.replace(",", " "),
                    'company': company.string.replace(",", " "),
                    'location': region.string,
                    'link': link,
                }

                results.append(job_data)

    return results


# extract_jobs(python)