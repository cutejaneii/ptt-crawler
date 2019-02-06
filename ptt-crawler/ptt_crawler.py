# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import threading
from model import ptt_article_model, ptt_response_model
from check_date import in_days
import re
from six import u
from check_remove_words import check_any_remove_words
import threading
import queue
import datetime

def get_serial(element):
    return element.serial

'''
Get ptt soup
'''
def get_ptt_soup(crawl_url):
    cookies = {'over18':'1'}
    response = requests.get(crawl_url, cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

'''
Get Latest page no
'''
def get_latest_page_no(board):
    page_no=''
    url='https://www.ptt.cc/bbs/'+ board + '/index.html'
    soup = get_ptt_soup(url)
    data = soup.findAll("a", {"class": "btn wide"})
    remove_href=['/bbs/'+ board +'/index1.html', '/bbs/'+ board +'/index.html']
    for anchor in data:
        if (anchor['href'] !=''):
            if (anchor['href'] not in remove_href):
                page_no = anchor['href'].replace('/bbs/'+ board +'/index','').replace('.html','')
    return int(page_no)+1


def get_imgur_img(imgur_url):
    photo_url=''
    try:
        imgur_soup = get_ptt_soup(imgur_url)
        imgs = imgur_soup.findAll("link", {"rel":"image_src"})
        for img in imgs:
            if ('.jpg' in img['href']):
                photo_url=img['href']
                break
            elif ('.png' in img['href']):
                photo_url=img['href']
                break
            else:
                pass

    except Exception as e1:
        print(str(e1))
    return photo_url


def to_model_job(serials, ptt_urls, is_get_response, is_get_img, q):
    model = []
    try:
        for x in range(0, len(ptt_urls), 1):
            model.append(get_ptt_article_model(serials[x], ptt_urls[x],  is_get_response, 0))
    except Exception as ex:
        print(ex)
    q.put(model) #return results
    q.task_done()


def get_ptt_article_model(serial, ptt_url, is_get_response, is_get_img):
    article_model = ptt_article_model()
    try:

        article_soup = get_ptt_soup(ptt_url)
        push_contents = []

        metas = article_soup.select('div.article-metaline')

        article_model.image_url=''
        article_model.serial=serial
        article_model.article_id = ptt_url.replace('https://www.ptt.cc/bbs/','').replace('.html','').split('/')[1]
        main_content = article_soup.find('div', {'id':'main-content'})

        all_push_contents = article_soup.findAll('span', {'class':'push-content'})
        all_push_tags = article_soup.findAll('span', {'class':'push-tag'})
        all_push_dates = article_soup.findAll('span', {'class':'push-ipdatetime'})
        all_push_authors = article_soup.findAll('span', {'class':'push-userid'})


        remove_divs = main_content.select('div')
        for r in remove_divs:
            r.extract()
        remove_spans = main_content.select('span')
        for rs in remove_spans:
            rs.extract()


        filtered = [ v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--'] ]
        expr = re.compile(u(r'[^\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\s\w:/-_.?~%()]'))
        for i in range(len(filtered)):
            filtered[i] = re.sub(expr, '', filtered[i])

        filtered = [_f for _f in filtered if _f]  # remove empty strings
        content = ' '.join(filtered)
        content = re.sub(r'(\s)+', ' ', content)


        article_model.content = content

        try:
            article_model.author=metas[0].find('span', {'class':'article-meta-value'}).text
            article_model.title=metas[1].find('span', {'class':'article-meta-value'}).text
            article_model.date=metas[2].find('span', {'class':'article-meta-value'}).text
        except:
            pass

        article_model.url=ptt_url

        if (is_get_response==1):

            for x in range(0, len(all_push_contents), 1):
                author=''
                if (check_any_remove_words(all_push_contents[x].text.replace(': ','').replace(':',''))==False):
                    if (len(all_push_contents[x].text.replace(': ','').replace(':',''))>0):
                        author = all_push_authors[x].text
                        match = [data for data in push_contents if data.author==author]
                        if (len(match)>0):
                            for i in range(0, len(push_contents), 1):
                                if (push_contents[i].author==author):
                                    push_contents[i].content += all_push_contents[x].text.replace(': ','').replace(':','')
                            pass
                        else:
                            response_model = ptt_response_model()
                            response_model.content = all_push_contents[x].text.replace(': ','').replace(':','')
                            response_model.push_tag = all_push_tags[x].text
                            response_model.date = all_push_dates[x].text
                            response_model.author = all_push_authors[x]
                            push_contents.append(response_model)

            push_contents = [data for data in push_contents if '噓' not in data.push_tag]

            article_model.responses.extend(push_contents)

        # handle images
        if (is_get_img==1):
            imgs = article_soup.findAll('a', {"rel":"nofollow"})

            for img in imgs:
                if ('.jpg' in img['href']):
                    article_model.image_urls.append(img['href'])
                    article_model.image_count+=1
                elif ('.png' in img['href']):
                    article_model.image_urls.append(img['href'])
                    article_model.image_count+=1
                elif ('i.imgur.com' in img['href']):
                    article_model.image_urls.append(img['href'])
                    article_model.image_count+=1
                elif ('imgur.com' in img['href']):
                    article_model.image_urls.append(get_imgur_img(img['href']))
                    article_model.image_count+=1
                else:
                    pass
    except Exception as e:
        print('error：'+str(e))

    return article_model

def ptt_crawl_by_keyword(keyword, board, count):
    result=[]
    article_hrefs=[]
    serials=[]
    queue_count=10
    try:
        last_pageno=5
        i=0
        p=1
        for x in range(1, (last_pageno+1), 1):
            print('crawl pageno=' + str(x) + '-> https://www.ptt.cc/bbs/'+ board +'/search?page='+ str(x) +'&q='+keyword)
            ptt_soup = get_ptt_soup('https://www.ptt.cc/bbs/'+ board +'/search?page='+ str(x) +'&q='+keyword)

            article_lists = ptt_soup.select('div[class="title"] a')

            for anchor in article_lists:
                print(anchor['href'])
                if (anchor['href'] is not None and '/bbs/'+ board +'/M.' in anchor['href']):
                    if (check_any_remove_words(anchor.text)==False):
                        i+=1
                        article_hrefs.append('https://www.ptt.cc' + anchor['href'])
                        serials.append(i)

        pass

    except Exception as ee:
        print(str(ee))
    return result


def ptt_crawl(board, last_aritlce_id, is_get_responses, count):
    result=[]
    isCrawl=True
    try:
        pageno= get_latest_page_no(board)
        while (isCrawl==True):
            ptt_soup = get_ptt_soup('https://www.ptt.cc/bbs/'+ board +'/index'+ str(pageno) +'.html')
            article_lists = ptt_soup.select('div[class="title"] a')
            pageno-=1

            i=0
            for anchor in article_lists:
                if (len(result)==count):
                    isCrawl=False
                    break
                if (anchor['href'] is not None and '/bbs/'+ board +'/M.' in anchor['href']):
                    if ('/'+last_aritlce_id.lower() in anchor['href'].lower()):
                        isCrawl=False
                        break
                    if (check_any_remove_words(anchor.text)==False):
                        i+=1
                        article_model = get_ptt_article_model(i, 'https://www.ptt.cc' + anchor['href'], is_get_responses, 0)
                        article_model.board=board
                        article_model.fromweb='ptt'
                        article_model.article_id = anchor['href'].replace('/bbs/'+board+'/','').replace('.html','')
                        result.append(article_model)
    except Exception as ee:
        print(str(ee))
    return result


def crawl_by_single_page(board, pageno, is_get_responses):
    my_result=[]
    try:
        print('https://www.ptt.cc/bbs/'+ board +'/index'+ str(pageno) +'.html')
        ptt_soup = get_ptt_soup('https://www.ptt.cc/bbs/'+ board +'/index'+ str(pageno) +'.html')

        article_lists = ptt_soup.select('div[class="title"] a')
        i = 0
        for anchor in article_lists:
            if (anchor['href'] is not None and '/bbs/'+ board +'/M.' in anchor['href']):
                if (check_any_remove_words(anchor.text)==False):
                    i+=1
                    article_model = get_ptt_article_model(i, 'https://www.ptt.cc' + anchor['href'], is_get_responses, 0)
                    article_model.board=board
                    article_model.serial=i
                    article_model.fromweb='ptt'
                    article_model.article_id = anchor['href'].replace('/bbs/'+board+'/','').replace('.html','')
                    my_result.append(article_model)

    except Exception as ee:
        print(str(ee))
    return my_result


def crawl_by_pages(board, from_pageno, to_pageno, is_get_responses):
    ptt_models=[]
    article_hrefs=[]
    serials=[]
    queue_count=100
    try:
        i=0
        for x in range(to_pageno, (from_pageno-1), -1):
            print('crawl pageno=' + str(x) + '-> https://www.ptt.cc/bbs/'+ board +'/index'+ str(x) +'.html')
            ptt_soup = get_ptt_soup('https://www.ptt.cc/bbs/'+ board +'/index'+ str(x) +'.html')

            article_lists = ptt_soup.select('div[class="title"] a')

            for anchor in article_lists:
                if (anchor['href'] is not None and '/bbs/'+ board +'/M.' in anchor['href']):
                    if (check_any_remove_words(anchor.text)==False):
                        i+=1
                        article_hrefs.append('https://www.ptt.cc' + anchor['href'])
                        serials.append(i)

        # start to multi-thread crawl job....
        if (len(article_hrefs) >= queue_count):
            q = queue.Queue(queue_count)
            threads=[]
            each_count = len(article_hrefs)// (queue_count-1)

            for x in range(0, (queue_count-1)):
                thread = threading.Thread(target=to_model_job, args=(serials[x*each_count:(x+1)*each_count], article_hrefs[x*each_count:(x+1)*each_count], is_get_responses, 0, q),)
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)

            left = len(article_hrefs) - ((queue_count-1)*each_count)
            if (left > 0):
                thread = threading.Thread(target=to_model_job, args=(serials[(queue_count-1)*each_count:], article_hrefs[(queue_count-1)*each_count:], is_get_responses, 0, q),)
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)

            for _ in range(len(threads)):
                q.join()

            for _ in range(len(threads)):
                queue_data = q.get()
                ptt_models.extend(queue_data) # 取出 queue 裡面的資料

        else:
            for x in range(to_pageno, (from_pageno-1), -1):
                ptt_models.extend(crawl_by_single_page(board, x, is_get_responses))

        #ptt_models.sort(key=get_serial)
    except Exception as ee:
        print(str(ee))
    return ptt_models
