import random
import lxml
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_page_content(url):
    try:
        return requests.get(url, timeout=(1, 5)).content
    except requests.exceptions.ConnectionError:
        exit('Failed to establish connection to {0}'.format(url))


def get_courses_list(url, how_many):
    soup = BeautifulSoup(get_page_content(url), 'lxml')
    links = [link.get_text() for link in soup.find_all('loc')]
    return random.sample(links, how_many)


def get_course_info(url):
    soup = BeautifulSoup(get_page_content(url), 'html.parser')

    title = soup.find(class_="title display-3-text").text
    language = soup.find(class_='rc-Language').text
    start = ' '.join(soup.find(id='start-date-string').text.split()[1:])
    duration = len(soup.find_all(class_="week-heading"))
    rating = soup.find(class_='ratings-text').span.text.split()[0]

    return [title, language, start, duration, rating]


def output_courses_info_to_xlsx(courses_info):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['Title', 'Language', 'Start', 'Duration', 'Rating'])
    for course in courses_info:
        sheet.append(course)
    workbook.save("courses.xlsx")


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    how_many = 20
    courses_info = []
    for course in get_courses_list(url, how_many):
        courses_info.append(get_course_info(course))
    output_courses_info_to_xlsx(courses_info)
