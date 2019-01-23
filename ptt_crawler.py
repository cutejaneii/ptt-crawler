# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import threading
from model import ptt_article_model, ptt_response_model
from check_date import check_ptt_date
import re
from six import u
from check_remove_words import check_any_remove_words


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
                page_no = anchor['href'].encode('utf-8').replace('/bbs/'+ board +'/index','').replace('.html','')
    return page_no

def get_imgur_img(imgur_url):
    photo_url=''
    try:
        imgur_soup = get_ptt_soup(imgur_url)
        imgs = imgur_soup.findAll("link", {"rel":"image_src"})
        for img in imgs:
            if ('.jpg' in img['href']):
                photo_url=img['href'].encode('utf-8')
                break
            elif ('.png' in img['href']):
                photo_url=img['href'].encode('utf-8')
                break
            else:
                pass

    except Exception as e1:
        print(str(e1))
    return photo_url



def get_ptt_article_model(ptt_url, is_get_response, is_get_img):
    article_model = ptt_article_model()
    try:

        article_soup = get_ptt_soup(ptt_url)
        push_contents = []

        metas = article_soup.select('div.article-metaline')

        article_model.image_url=''

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

        if (is_get_response==True):

            for x in range(0, len(all_push_contents), 1):
                author=''
                if (check_any_remove_words(all_push_contents[x].text.replace(': ','').replace(':',''))==False):
                    if (len(all_push_contents[x].text.replace(': ',''))>0):
                        author = all_push_authors[x].text.encode('utf-8')
                        match = [data for data in push_contents if data.author==author]
                        if (len(match)>0):
                            for i in range(0, len(push_contents), 1):
                                if (push_contents[i].author==author):
                                    push_contents[i].content += all_push_contents[x].text.replace(': ','').replace(':','').encode('utf-8')
                            pass
                        else:
                            response_model = ptt_response_model()
                            response_model.content = all_push_contents[x].text.replace(': ','').replace(':','').encode('utf-8')
                            response_model.push_tag = all_push_tags[x].text.encode('utf-8')
                            response_model.date = all_push_dates[x].text
                            response_model.author = all_push_authors[x].text.encode('utf-8')
                            push_contents.append(response_model)

            print('push-contents1: '+str(len(push_contents)))
            push_contents = [data for data in push_contents if '噓' not in data.push_tag]

            article_model.responses.extend(push_contents)

        # handle images
        if (is_get_img==True):
            imgs = article_soup.findAll('a', {"rel":"nofollow"})

            for img in imgs:
                if ('.jpg' in img['href']):
                    article_model.image_urls.append(img['href'].encode('utf-8'))
                    article_model.image_count+=1
                elif ('.png' in img['href']):
                    article_model.image_urls.append(img['href'].encode('utf-8'))
                    article_model.image_count+=1
                elif ('i.imgur.com' in img['href']):
                    article_model.image_urls.append(img['href'].encode('utf-8'))
                    article_model.image_count+=1
                elif ('imgur.com' in img['href']):
                    article_model.image_urls.append(get_imgur_img(img['href'].encode('utf-8')).encode('utf-8'))
                    article_model.image_count+=1
                else:
                    pass
    except Exception as e:
        print('error：'+str(e))

    return article_model


def crawl_job(keyword, board, previous_day_count, last_aritlce_id):
    newest_article_id=''
    my_result=[]
    try:
        if (keyword==''):
            pageno= 10 #get_latest_page_no(board)
            ptt_soup = get_ptt_soup('https://www.ptt.cc/bbs/'+ board +'/index'+ str(pageno) +'.html')

            article_lists = ptt_soup.findAll("a")

            for anchor in article_lists:
                if (anchor['href'] is not None and '/bbs/'+ board +'/M.' in anchor['href']):
                    if ('/'+last_aritlce_id.lower() in anchor['href'].lower()):
                        break
                    if (check_any_remove_words(anchor.text)==False):
                        article_model = get_ptt_article_model('https://www.ptt.cc' + anchor['href'], True, False)
                        article_model.board=board
                        article_model.fromweb='ptt'
                        article_model.article_id = anchor['href'].replace('/bbs/'+board+'/','').replace('.html','')
                        if (newest_article_id==''):
                            newest_article_id = article_model.article_id

                        if (previous_day_count>0):
                            is_add = check_ptt_date(article_model.date, previous_day_count)
                            if (is_add == True):
                                my_result.append(article_model)
                        else:
                            my_result.append(article_model)

    except Exception as ee:
        print(str(ee))
    return newest_article_id, my_result


def crawl_job_by_pageno(board, pageno):
    newest_article_id=''
    my_result=[]
    try:
        ptt_soup = get_ptt_soup('https://www.ptt.cc/bbs/'+ board +'/index'+ str(pageno) +'.html')

        article_lists = ptt_soup.findAll("a")

        for anchor in article_lists:
            if (anchor['href'] is not None and '/bbs/'+ board +'/M.' in anchor['href']):
                if (check_any_remove_words(anchor.text)==False):
                    article_model = get_ptt_article_model('https://www.ptt.cc' + anchor['href'], True, False)
                    article_model.board=board
                    article_model.fromweb='ptt'
                    article_model.article_id = anchor['href'].replace('/bbs/'+board+'/','').replace('.html','')
                    my_result.append(article_model)

    except Exception as ee:
        print(str(ee))
    return newest_article_id, my_result



def ptt_crawl(board, keyword, previous_day_count, last_aritlce_id):
    results=[]
    newest_article_id=''

    newest_article_id, results = crawl_job(keyword = keyword, board = board, previous_day_count=previous_day_count, last_aritlce_id = last_aritlce_id)

    return newest_article_id, results

def ptt_crawl_by_pageno(board, pageno):
    results=[]
    newest_article_id=''

    newest_article_id, results = crawl_job_by_pageno(board = board, pageno=pageno)

    return newest_article_id, results
