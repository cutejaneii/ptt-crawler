# -*- coding: utf-8 -*-
from model import ptt_article_model
from ptt_crawler import ptt_crawl, ptt_crawl_by_pageno
import sys
import uuid

if __name__ == '__main__':
    #text_file = open('gossip.txt', 'w')
    results = []
    newest_article_id=''

    board='Gossiping'
    article_id='-----'
    previous_day=0
    crawl_mode=0 # crawl from pageno to pageno
    from_pageno = 1
    to_pageno = 3

    try:
        crawl_mode=int(sys.argv[1])
    except:
        pass

    if (crawl_mode==0):
        try:
            from_pageno = int(sys.argv[2])
            to_pageno = int(sys.argv[3])
        except:
            pass
    else:
        try:
            board=sys.argv[2]
        except:
            pass
        try:
            article_id=sys.argv[3]
        except:
            pass
        try:
            previous_day=int(sys.argv[4])
        except:
            pass


    if (crawl_mode==0):
        print('Start to crawl from page:'+ str(from_pageno) + ' to page:'+str(to_pageno))
        for x in range(from_pageno, (to_pageno+1), 1):
            print('<------------------ Crawling data, pageno='+str(x) + '------------------>')
            newest_article_id, results = ptt_crawl_by_pageno(board=board,pageno=x)
            save_crawl_data(results)
    else:
        newest_article_id, results = ptt_crawl(board=board, keyword='', previous_day_count=previous_day,  last_aritlce_id=article_id)

    print('newest_article_id:' + newest_article_id)

    #while pageno > 0 :
    #    pageno, results = ptt_crawl('gossiping','', pageno)
    #    for i in results:
    #        for j in i:
    #            print(j)
    #            text_file.write(j+'\n')
#text_file.close()
