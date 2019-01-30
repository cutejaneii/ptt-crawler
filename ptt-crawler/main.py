# -*- coding: utf-8 -*-
from model import ptt_article_model
from ptt_crawler import ptt_crawl, ptt_crawl_by_pageno
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-b', '--board', default='movie', help='ptt board name (default: movie)')
    parser.add_argument('-a', '--article_id', default='**', help='Article id')
    parser.add_argument('-m', '--mode', type=int, default=0, help='Query mode (default:0)  0: The NEWEST articles, 1:Articles from pageno to pageno, 2:Certain page, 3:get articles by KEYWORD ')
    parser.add_argument('-c', '--count', type=int, default=10, help='Article count (default: 10)')
    parser.add_argument('-f', '--from_pageno', type=int, default=1, help='Article count (default: 1)')
    parser.add_argument('-t', '--to_pageno', type=int, default=1, help='Article count (default: 1)')
    parser.add_argument('-r', '--get_responses', type=int, default=0, help='Get response (default:0)  0:No responses, 1:With response')
    parser.add_argument('-k', '--keyword', default='pizza', help='Keyword')
    args = parser.parse_args()
    
    data = []
    newest_article_id=''
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

    if (check==True):
        if (args.mode==0):
            ptt_crawl(board=args.board, last_aritlce_id=args.article_id, count=args.count)
        else:
            if (args.mode==1):
                for x in range(args.from_pageno, (args.to_pageno+1), 1):
                    print('<------------------ Crawling data, pageno='+str(x) + '------------------>')
                    newest_article_id, results = ptt_crawl_by_pageno(board=args.board,pageno=args.from_pageno)
            elif (args.mode==2):
                newest_article_id, data = ptt_crawl_by_pageno(board=args.board,pageno=args.from_pageno)
            else:
                pass

        for article in data:
            print(article.title)
