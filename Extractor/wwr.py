import requests
from bs4 import BeautifulSoup

def create_soup(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Whale/3.18.154.7 Safari/537.36'}
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'lxml')

    return soup

def extract_wwr_jobs(keyword):
    url = 'https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term='
    soup = create_soup(url + keyword)

    result = []

    jobs = soup.find_all('section', attrs={'class':'jobs'})

    for job in jobs:
        job_posts = job.find_all('li')[:-1]
        for post in job_posts:
            anchors = post.find_all('a')
            anchor = anchors[1]

            link = 'https://weworkremotely.com' + anchor['href']
            company, kind, location = anchor.find_all('span', attrs={'class':'company'})
            title = anchor.find('span', attrs={'class':'title'})

            job_data = {
                'company': company.get_text(strip=True),
                'location': location.get_text(strip=True),
                'position': title.get_text(strip=True),
                'link': link
            }

            result.append(job_data)

    return result
