from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# headless
chrome_options.headless = True
# user-agent
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

def get_page_count(keyword):
    url = 'https://kr.indeed.com/jobs?q='

    browser.get(url + keyword)

    soup = BeautifulSoup(browser.page_source, 'lxml')
    
    navigation = soup.find('nav', attrs={'role':'navigation'})
    
    if navigation == None:
        return 1
    
    pages = navigation.find_all('div')
    count = len(pages)

    if count == 0:
        return 1
    
    elif count >= 5:
        more_pages = 5
        
        while True:
          browser.get(f'{url}{keyword}&start={(more_pages - 1) * 10}')
          
          soup = BeautifulSoup(browser.page_source, 'lxml')
          
          navigation = soup.find('nav', attrs={'role':'navigation'})
          
          pages = navigation.find_all("div")
          
          if len(pages) == 4:
            break
        
          elif more_pages >= 10:
            break
        
          else:
            more_pages = more_pages + 1
            
        return more_pages
    
    else:
        return count - 1

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    result = []
    
    for page in range(pages):
        url = 'https://kr.indeed.com/jobs?q='

        browser.get(f'{url}{keyword}&start={page * 10}')

        soup = BeautifulSoup(browser.page_source, 'lxml')

        job_list = soup.find('ul', attrs={'class': 'jobsearch-ResultsList'})
        jobs = job_list.find_all('li', recursive=False)

        for job in jobs:
            zone = job.find('div', attrs={'class':'mosaic-zone'})
            if zone == None:
                anchor = job.select_one('h2 a')

                title = anchor['aria-label'].replace('의 전체 세부 정보', '')
                link = 'https://kr.indeed.com' + anchor['href']

                company = job.find('span', attrs={'class':'companyName'}).get_text(strip=True)
                location = job.find('div', attrs={'class':'companyLocation'}).get_text(strip=True)

                job_data = {
                    'company': company,
                    'location': location,
                    'position': title,
                    'link': link
                }

                result.append(job_data)
                
    browser.close()
    
    return result

