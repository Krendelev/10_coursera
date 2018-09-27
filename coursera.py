
import random
import argparse
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_parsed_source(url):
    try:
        responce = requests.get(url, timeout=(1, 7))
        return BeautifulSoup(responce.content, 'html.parser')
    except(requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout):
        return None


def get_random_links(how_many, page):
    links = [link.get_text() for link in page.find_all('loc')]
    return random.sample(links, how_many)


def get_course_info(page):
    info = {
        'Title': 'Failed to get info', 'Language': '–',
        'Start': '–', 'Duration': '–', 'Rating': '–'
        }
    try:
        info['Title'] = page.find(class_='title display-3-text').text
        info['Language'] = page.find(class_='rc-Language').text
        info['Start'] = ' '.join(page.find(class_='startdate').text.split()[1:])
        info['Duration'] = len(page.find_all(class_='week-heading'))
        info['Rating'] = page.find(class_='ratings-text').span.text.split()[0]
    except AttributeError:
        pass
    return info


def output_courses_info_to_xlsx(courses_info):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(list(courses_info[0].keys()))
    for course in courses_info:
        sheet.append(list(course.values()))
    return workbook


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    how_many = 20
    courses_info = []
    source = get_parsed_source(url)
    if not source:
        exit('Failed to establish connection to {}'.format(url))
    for link in get_random_links(how_many, source):
        courses_info.append(get_course_info(get_parsed_source(link)))
    workbook = output_courses_info_to_xlsx(courses_info)
    workbook.save(get_args().output or 'courses.xlsx')
