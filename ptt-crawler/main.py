# -*- coding: utf-8 -*-
from model import ptt_article_model
from ptt_crawler import ptt_crawl, crawl_by_single_page, crawl_by_pages, ptt_crawl_by_keyword
from argparse import ArgumentParser
import datetime


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-b', '--board', default='movie', help='ptt board name (default: movie)')
    parser.add_argument('-a', '--article_id', default='**', help='Article id')
    parser.add_argument('-m', '--mode', type=int, default=0, help='Query mode (default:0)  0: The NEWEST articles, 1:Articles from pageno to pageno, 2:Articles from certain page, 3: Articles by keyword')
    parser.add_argument('-c', '--count', type=int, default=10, help='Article count (default: 10)')
    parser.add_argument('-f', '--from_pageno', type=int, default=1, help='Article count (default: 1)')
    parser.add_argument('-t', '--to_pageno', type=int, default=1, help='Article count (default: 1)')
    parser.add_argument('-r', '--get_responses', type=int, default=0, help='Get response (default:0)  0:No responses, 1:With response')
    parser.add_argument('-k', '--keyword', default='THOR', help='Keyword')
    args = parser.parse_args()

    data = []
    check=True

    if (args.mode not in [0, 1, 2, 3]):
        print('[mode] can only be 0, 1, 2, 3')
        check=False

    if (args.get_responses not in [0, 1]):
        print('[get_responses] can only be 0, 1.')
        check=False

    if (args.count == 0):
        print('[count] should bigger than 0.')
        check=False
    else:
        if (args.count>1000):
            print('[count] can only smaller or equals 1000.')
            args.count=1000

    s = str(datetime.datetime.now())

    if (check==True):
        if (args.mode==0):
            data = ptt_crawl(board=args.board, last_aritlce_id=args.article_id, is_get_responses = args.get_responses, count=args.count)
        else:
            if (args.mode==1):
                data = crawl_by_pages(board=args.board,from_pageno=args.from_pageno, to_pageno=args.to_pageno,is_get_responses = args.get_responses)
            elif (args.mode==2):
                data = crawl_by_single_page(board=args.board,pageno=args.from_pageno, is_get_responses = args.get_responses)
            else:
                data = ptt_crawl_by_keyword(keyword=args.keyword, is_get_responses= args.get_responses,  board=args.board, from_pageno=args.from_pageno, to_pageno=args.to_pageno)

        for article in data:
            print(article.title)
            for i in article.responses:
                print('  ' + i.push_tag + i.content)
        print('from ' + s)
        print('to ' + str(datetime.datetime.now()))
