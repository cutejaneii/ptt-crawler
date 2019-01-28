# encoding=UTF-8
class ptt_article_model:
    def __init__(self):
        self.fromweb=''
        self.board=''
        self.url=''
        self.title=''
        self.content=''
        self.article_id=''
        self.date=''
        self.image_urls=[]
        self.responses=[]
        self.author=''
        self.image_count=0

class ptt_response_model:
    def __init__(self):
        self.content=''
        self.push_tag=''
        self.date=''
        self.author=''
