import requests
from bs4 import BeautifulSoup

def create_soup(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Whale/3.18.154.7 Safari/537.36'}
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'lxml')

    return soup

def get_page_count(keyword):
    url = 'https://www.jobkorea.co.kr/Search/?stext='
    
    page = 1
    
    while page <= 10:
        soup = create_soup(f'{url}{keyword}&Page_No={page}')
        jobs = soup.select('.clear > .list-post .long')
        
        if len(jobs) == 0:
            return page - 1
      
        elif page == 10:
            return page
        
        else:
            page = page + 1

def extract_jobkorea_jobs(keyword):
    pages = get_page_count(keyword)
    result = []
    
    for page in range(pages):
        url = 'https://www.jobkorea.co.kr/Search/?stext='
        soup = create_soup(f'{url}{keyword}&Page_No={page}')

        jobs = soup.find_all('div', attrs={'class':'post'})[:20]

        for job in jobs:
            job_post = job.find('div', attrs={'class':'post-list-corp'}).find('a')

            link = 'https://www.jobkorea.co.kr' + job_post['href']
            company = job_post['title']

            title = job.find('div', attrs={'class':'post-list-info'}).find('a')['title']
            location = job.find('div', attrs={'class': 'post-list-info'}).find('span', attrs={'class': 'loc long'}).get_text(strip=True)

            job_data = {
                'company': company,
                'location': location,
                'position': title,
                'link': link
            }

            result.append(job_data)
        
    return result