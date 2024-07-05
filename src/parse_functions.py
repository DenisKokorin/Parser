import requests
from bs4 import BeautifulSoup
import fake_useragent

user_agent = fake_useragent.UserAgent()

def get_link_vacancy(request):
    data = requests.get(
        url=f"https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=113&text={request}&page=1", headers={'user-agent': user_agent.random})
    if data.status_code != 200:
        return print("error get data from url")
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        page_count = int(
            soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
    except:
        return print("error find page_count")
    for page in range(page_count):
        try:
            result = requests.get(url=f"https://hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=113&text={request}&page={page}", headers={'user-agent': user_agent.random})
            if result.status_code == 200:
                soup = BeautifulSoup(result.content, "lxml")
                for a in soup.find("span",attrs={"class": "serp-item__title-link-wrapper"}).find_all("a", attrs={"class": "bloko-link", "target": "_blank"}):
                    yield f'{a.attrs["href"].split("?")[0]}'
        except:
            print("error build links")


def get_vacancy(link):
    data = requests.get(url=link, headers={'user-agent':user_agent.random})
    soup = BeautifulSoup(data.content, "lxml")
    try:
        title = soup.find(attrs={"data-qa": "vacancy-title"}).text
    except:
        title = "не указано"
    try:
        salary = soup.find(attrs={"data-qa": "vacancy-salary-compensation-type-net"}).text.replace(" ","").replace(" "," ")
    except:
        salary = "не указано"
    try:
        city = soup.find("span", attrs={"data-qa": "vacancy-view-raw-address"}).text.split(", ")[0]
    except:
        city = "не указано"
    try:
        company = soup.find("span", attrs={"data-qa": "bloko-header-2"}).text.replace("\xa0", " ")
    except:
        company = "не указано"
    try:
        experience = soup.find(attrs={"data-qa": "vacancy-experience"}).text
    except:
        experience = "не указано"
    try:
        mode = soup.find("p", attrs={"data-qa": "vacancy-view-employment-mode"}).text.split(", ")
        type_of_employment = mode[0]
        schedule = mode[1]
    except:
        type_of_employment = "не указано"
        schedule = "не указано"
    try:
        viewers_count = soup.find("span", attrs={"class": "vacancy-viewers-count"}).text.replace("\xa0", " ")
    except:
        viewers_count = "не указано"



    vacancy = {
        "title": title,
        "salary": salary,
        "city": city,
        "company": company,
        "experience": experience,
        "type_of_employment": type_of_employment,
        "schedule": schedule,
        "viewers_count": viewers_count,
        "link": link
    }
    return vacancy