# author:Demon
# time:2018/6/9
# function:获取笑话信息(http://www.jokeji.cn/)
import re
import random
import pymysql
import requests

headers = []
list_type_name = []
list_type_number = []
list_type_url = []
list_type_page = []
list_more_info = []


def init():
    h1 = {'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Chrome/55.0.2883.87 Safari/537.36'}
    h2 = {'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}
    h3 = {'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0; DigExt)'}
    headers.append(h1)
    headers.append(h2)
    headers.append(h3)


def gethtml(html):
    max_index = headers.__len__()-1
    index = random.randint(0, max_index)
    browser_header = headers[index]
    req = requests.get(html)
    if req.status_code == 200:
        req.encoding = 'GBK'
        return req.text
    else:
        print('get request failed')


def get_type_info():
    index_url = "http://www.jokeji.cn/Keyword.htm"
    url = "http://www.jokeji.cn"
    text = gethtml(index_url)
    # 获取每种类型的入口URL
    type_index_url = r'<a href="(.*?)" target="_self" class="user_14">'
    type_index_object = re.compile(type_index_url)
    type_index_url_list = re.findall(type_index_object, text)
    for item in type_index_url_list:
        item = url+item
        list_type_url.append(item)

    # 获取每种类型的名称和数量
    type_name = r'class="user_14">(.*?)</a>'
    type_name_object = re.compile(type_name, re.S)
    type_name_list = re.findall(type_name_object, text)
    for item in type_name_list:
        name = re.sub('\(.*?\)', '', item)
        number = re.findall('.*?\((.+?)\).*?', item)
        list_type_name.append(name)
        list_type_number.append(number[0])

    # 获取每种类型笑话的page页数
    type_page = r'<a href="list29_104.htm">尾页</a>'

    for item, number in zip(list_type_url, list_type_number):
        if int(number) <= 21:
            list_type_page.append(1)
        else:
            text = gethtml(item)
            type_page = r'<a href=".*?_(.*?).htm">尾页</a>'
            type_page_object = re.compile(type_page)
            type_page_list = re.findall(type_page_object, text)
            page = type_page_list[0]
            list_type_page.append(page)

    # 查看一下list_type name/number/url
    """
    for (name, number, url) in zip(list_type_name, list_type_number, list_type_url):
        print('{}:{}:{}:'.format(name, number, url))
    print('总有:{}条记录!'.format(list_type_name.__len__()))
    """
    # 查看page
    """
    for item in list_type_page:
        print(item) 
    """
    # 把笑话type信息插入joke_type表
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='jokes_data_analysis', port=3306, charset='utf8')
    cur = conn.cursor()
    cur.execute('set sql_safe_updates=0;')
    conn.commit()  # 只有提交才可以，对下面生效
    cur.execute('start transaction')  # 事务处理
    print('正在写入type_info表......')
    for (name, number, url, page) in zip(list_type_name, list_type_number, list_type_url, list_type_page):
        sql = "insert into joke_type(style,number,index_url,page) values('{}',{},'{}',{})".format(name, number, url, page)
        cur.execute(sql)

    cur.execute('set sql_safe_updates=1')
    conn.commit()
    conn.close()
    print('写入type_info表完成!!!!!!')

    # 获取类型笑话标题和访问量
    for joke_type, type_url, type_page in zip(list_type_name, list_type_url, list_type_page):
        for page_index in range(1, int(type_page)+int(1)):

            url = type_url[:-5]+str(page_index)+".htm"
            text = gethtml(url)
            # 标题
            title = r'target="_blank" >(.*?)</a>'
            title_object = re.compile(title,  re.S)
            title_list = re.findall(title_object, text)
            # 访问量
            title_visit = r'<span>浏览：(.*?)次</span>'
            type_visit_object = re.compile(title_visit)
            visit_list = re.findall(type_visit_object, text)
            # url
            title_url = r'<a href="(.*?)"target="_blank" >'
            title_url_object = re.compile(title_url)
            url_list = re.findall(title_url_object, text)
            index_url = "http://www.jokeji.cn"

            for title, visit, url in zip(title_list, visit_list, url_list):
                url = index_url+url
                list_more_info.append([joke_type, title, visit, url])

            for (j_type, title, visit, url) in list_more_info:
                print('{}:{}:{}:{}'.format(j_type, title, visit, url))

    # 把list_more_info 数据写入joke_more_info表
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='jokes_data_analysis', port=3306,
                           charset='utf8')
    cur = conn.cursor()
    cur.execute('set sql_safe_updates=0;')
    conn.commit()  # 只有提交才可以，对下面生效
    cur.execute('start transaction')  # 事务处理
    print('正在写入joke_more_info表......')
    for (style, title, visit, url) in list_more_info:
        sql = "insert into joke_more_info(type,title,visit,url) values('{}','{}',{},'{}')".format(style, title, visit, url)
        cur.execute(sql)

    cur.execute('set sql_safe_updates=1')
    conn.commit()
    conn.close()
    print('写入joke_more_info表完成!!!!!!')


if __name__ == '__main__':
    init()
    get_type_info()
