
import random
import argparse
import collections
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_source_page(url):
    try:
        return requests.get(url, timeout=(1, 7)).content
    except(requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout):
        return None


def get_random_courses_links(courses_count, page):
    content = BeautifulSoup(page, 'html.parser')
    links = [link.get_text() for link in content.find_all('loc')]
    return random.sample(links, courses_count)


def get_course_info(page):
    course_info = collections.OrderedDict()
    try:
        content = BeautifulSoup(page, 'html.parser')
        course_info['Title'] = content.find(class_='title display-3-text').text
        course_info['Language'] = content.find(class_='rc-Language').text
        course_info['Start'] = ' '.join(content.find(class_='startdate').text.split()[1:])
        course_info['Duration'] = len(content.find_all(class_='week-heading'))
        course_info['Rating'] = content.find(class_='ratings-text').span.text.split()[0]
    except AttributeError:
        pass
    return course_info


def output_courses_info_to_xlsx(courses_info):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['Title', 'Language', 'Start', 'Duration', 'Rating'])
    for course in courses_info:
        sheet.append(
            list(course.values()) or
            ['failed to get info', '--', '--', '--', '--']
            )
    return workbook


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', default='courses.xlsx', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    source = get_source_page(url)
    if not source:
        exit('Failed to establish connection to {}'.format(url))
    courses_count = 20
    courses_info = []
    for link in get_random_courses_links(courses_count, source):
        courses_info.append(get_course_info(get_source_page(link)))
    workbook = output_courses_info_to_xlsx(courses_info)
    workbook.save(get_args().output)
