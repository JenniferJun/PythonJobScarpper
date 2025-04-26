# BLUEPRINT | DONT EDIT

import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


# Get Response with specific url call
def get_request_response(url):
    response = requests.get(
        url,
        headers={
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
    return response


def get_playwright(url):
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            p = sync_playwright().start()
            browser = p.chromium.launch(headless=True,
                                        args=[
                                            '--no-sandbox',
                                            '--disable-setuid-sandbox',
                                            '--disable-dev-shm-usage'
                                        ])
            page = browser.new_page()
            page.goto(url)
            content = page.content()
            browser.close()
            p.stop()
            soup = BeautifulSoup(content, "html.parser")
            return soup
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                print(
                    f"Failed to initialize Playwright after {max_retries} attempts: {e}"
                )
                # Fallback to requests if Playwright fails
                response = get_request_response(url)
                return BeautifulSoup(response.content, "html.parser")
            print(f"Attempt {retry_count} failed, retrying...")
            time.sleep(1)  # Wait a bit before retrying


def parsing_berlinstartup(soup_content):
    jobs_list = soup_content.find("ul", class_="jobs-list-items").find_all(
        "li", class_="bjs-jlid")

    jobs = []
    for job in jobs_list:
        title = job.find("h4", class_="bjs-jlid__h").text.strip()
        title_url = job.find("h4", class_="bjs-jlid__h").find("a")['href']
        company = job.find("a", class_="bjs-jlid__b").text.strip()
        company_url = job.find("a", class_="bjs-jlid__b")['href']
        description = job.find("div",
                               class_="bjs-jlid__description").text.strip()
        skill_area = job.find_all("a", class_="bjs-bl-whisper")

        skills = []
        for skill in skill_area:
            skill_info = {
                'area': skill.text.strip(),
                'area_url': skill['href'],
            }
            skills.append(skill_info)

        #직무제목, 직무상세 URL, 회사이름, 회사정보 URL, 직무설명, 직무영역정보(직무, 직무링크)
        job_dict = {
            'title': title,
            'title_url': title_url,
            'company': company,
            'company_url': company_url,
            'description': description,
            'location': "",
            'skills': skills,
        }

        jobs.append(job_dict)
    return jobs


def parsing_web3(soup_content):
    jobs_list = soup_content.find("tbody",
                                  class_="tbody").find_all("tr",
                                                           class_="table_row")

    jobs = []
    skills = []
    for job in jobs_list:
        try:
            title = job.find(
                "div", class_="job-title-mobile").find("h2").text.strip()
            title_url = job.find("div",
                                 class_="job-title-mobile").find("a")['href']
            company = job.find(
                "td", class_="job-location-mobile").find("h3").text.strip()
            company_url = job.find(
                "td", class_="job-location-mobile").find("a")['href']

            description = ""
            if job.find("td", class_="job-location-mobile"):
                description_a = job.findAll("td", class_="job-location-mobile")
                description = ", ".join(
                    [d.text.strip() for d in description_a])

            skill_area = job.find_all('span',
                                      class_='my-badge my-badge-secondary')
            skills = extract_span_info(skill_area)
        except:
            pass

        #직무제목, 직무상세 URL, 회사이름, 회사정보 URL, 직무설명, 직무영역정보(직무, 직무링크)
        job_dict = {
            'title': title,
            'title_url': title_url,
            'company': company,
            'company_url': company_url,
            'description': description,
            'location': "",
            'skills': skills,
        }

        jobs.append(job_dict)

    return jobs


def extract_span_info(soup):
    span_info = []
    for span in soup:
        anchor = span.find('a')
        if anchor:
            try:
                text = anchor.text.strip()
                href = anchor.get('href', '')
                span_info.append({'text': text, 'href': href})
            except:
                pass
    return span_info


def parsing_weworkremotely(soup_content):
    try:
        jobs_lists = soup_content.findAll("section", class_="jobs")
        jobs = []
        for jobs_list in jobs_lists:
            jobs_list = jobs_list.find("article").find("ul").find_all("li")

            for job in jobs_list:
                try:
                    if (job.find("li", class_="view-all")):
                        continue

                    if (job.find("div", class_="new-listing__header").find(
                            "h4", class_="new-listing__header__title")):
                        title = job.find(
                            "div", class_="new-listing__header").find(
                                "h4", class_="new-listing__header__title"
                            ).text.strip()
                    else:
                        continue

                    title_url = job.find("a")['href']
                    company = job.find(
                        "p", class_="new-listing__company-name").text.strip()
                    company_url = job.find(
                        "div", class_="tooltip--flag-logo").find(
                            "a")['href'] if job.find(
                                "div", class_="tooltip--flag-logo") else ""

                    description = ""
                    if job.find("div",
                                class_="new-listing__categories").find("p"):
                        description_a = job.find(
                            "div",
                            class_="new-listing__categories").findAll("p")
                        description = ", ".join(
                            [d.text.strip() for d in description_a])

                    job_dict = {
                        'title': title,
                        'title_url': title_url,
                        'company': company,
                        'company_url': company_url,
                        'description': description,
                        'location': "",
                        'skills': "",
                    }
                    jobs.append(job_dict)
                except:
                    continue
    except:
        pass
    return jobs


def search_berlinstartup(skill):
    base_url = "https://berlinstartupjobs.com"
    o_jobs = []
    # "https://berlinstartupjobs.com/skill-areas/{skill}/"
    s_response = get_request_response(f"{base_url}/skill-areas/{skill}/")
    s_soup = BeautifulSoup(s_response.content, "html.parser")
    o_jobs = parsing_berlinstartup(s_soup)
    span_info = extract_span_info(s_soup)

    return o_jobs


def search_web3(skill):
    base_url = "https://web3.career"
    o_jobs = []
    # "https://web3.career/python-jobs"
    s_response = get_request_response(f"{base_url}/{skill}-jobs")
    s_soup = BeautifulSoup(s_response.content, "html.parser")
    o_jobs = parsing_web3(s_soup)
    return o_jobs


def search_weworkremotely(skill):
    base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
    o_jobs = []
    # "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=python"
    s_soup = get_playwright(f"{base_url}{skill}")
    o_jobs = parsing_weworkremotely(s_soup)
    return o_jobs
