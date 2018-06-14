import requests
import math
import time
import pandas as pd

def url():
    prefix = "https://www.udemy.com"
    suffix = "/api-2.0/courses/?"
    return prefix + suffix

def auth_string():
    auth_string = 'Basic SUPER_LONG_STRING'
    return auth_string

def headers():
    headers = {}
    headers['Authorization'] = auth_string()
    headers['Accept'] = 'application/json, text/plain, */*'
    return headers

def get_response_json(page, page_size, language = 'zh'):
    parameters = {"page": page, "page_size": page_size, "language": language}
    response = requests.get(url(), params=parameters, headers=headers())
    return response.json()

def price_number(price_text):
    if price_text == 'Free':
        return 0
    number = price_text.replace('CA$', '')
    return number

def append_course_info(info_list, course):
    item = course['id'], course['url'], price_number(course['price']), course['title']
    result = info_list[:]
    result.append(item)
    return result

if __name__ == '__main__':
    count = get_response_json(1, 1)['count']

    PAGE_SIZE = 5
    total_pages = math.ceil(count / PAGE_SIZE)

    course_info_list = []
    for page in range(1, total_pages + 1):
        print(str.format('---> Page # {0} of page size {1}', page, PAGE_SIZE))

        data = get_response_json(page, PAGE_SIZE)

        if 'results' not in data:
            print('.... throttled ... wait for a few moments ....')
            time.sleep(60)
            continue

        courses = data['results']
        for c in courses:
            info = (c['url'], price_number(c['price']), c['title'])
            joined = u'\t'.join([str(i) for i in info])
            print(str(c['id']) + ': ' + joined)
            
            course_info_list = append_course_info(course_info_list, c)
            print('--------------------')
            
        break

    # print(course_info_list)
    dataFrame = pd.DataFrame(course_info_list, columns=['id', 'url', 'price', 'title'])
    dataFrame.to_csv('./course_info.tsv', sep='\t', index=False)