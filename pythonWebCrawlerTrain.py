# encoding=utf8
import requests
import os
import time
from lxml import etree


def get_base_info(url):
    """
    This function is edited to get target url to retur a Parse web html.(using requests, etree)

    :param url: orgin url
    :return: a Parse web html
    """

    html = requests.get(url)
    html.encoding = 'utf-8'
    # print(html.content)
    # print('该响应状态码:', html.status_code)
    et = etree.HTML(html.content)
    return et


def show_ms(et):
    """
    This function is edited to print a Parse web html using utf-8 format.
    :param et: a Parse web html
    """

    result = etree.tostring(et, encoding="utf-8", pretty_print=True, method="html")
    print(result.decode('utf-8'))


def get_href(et, xpathi):
    """
    This function is to get the tag a href
    :param et: a Parse web html
    :param xpathi:
    :return: a list that lists all href
    """

    try:
        xpatho = xpathi + '/@href'
        href = et.xpath(xpatho)
    except:
        return ''
    else:
        # print(href)
        return href


def get_content(et, xpathi):
    """

    :param et: a Parse web html
    :param xpathi:
    :return: the content you need
    """
    xpatho = xpathi + '/text()'
    et = et.xpath(xpatho)
    return et


def get_book():
    """

    :return: a dict that contains the book's url and name
    """

    bk_all = []
    for i in range(1, 4):
        base_url = 'https://so.gushiwen.org/guwen/Default.aspx?p={}&type=%e6%ad%a3%e5%8f%b2%e7%b1%bb'.format(i)
        xpatha = '/html/body/div[2]/div[1]/div/div[1]/p[1]/a'
        xpathc = '/html/body/div[2]/div[1]/div/div[1]/p[1]/a/b'
        et = get_base_info(base_url)
        a = get_href(et, xpatha)
        c = get_content(et, xpathc)
        # print(c)
        # print(len(a), len(c))
        bk = {}
        bk_info = []
        for i in range(0, len(a)):
            bk['bk_url'] = 'https://so.gushiwen.org' + a[i]
            bk['bk_name'] = c[i]
            bk_info.append(bk)
            bk = {}
        bk_all = bk_all + bk_info
    return bk_all


def get_article_content(article_url):
    """

    :param article_url:
    :return: a string content
    """

    ch_url = article_url
    xpathch = '/html/body/div[2]/div[1]/div/div[1]/div/p'
    et = get_base_info(ch_url)
    t = get_content(et, xpathch)
    return '\n'.join(t)


def get_book_chapter(bk_url='https://so.gushiwen.org/guwen/book_46653FD803893E4F9B29D6AEC1BFD4EA.aspx'):
    """
    get all the chapter in the book'url and the article 's name, url, content

    :param bk_url: the book's index url
    :return: a dic , the key of it is its chapter, the value of the key is a list that contains articles dic, inside it is "name  url  content"
    """

    bk_xpathc = '/html/body/div[2]/div[1]/div[3]/div/div[1]/strong'
    et = get_base_info(bk_url)
    bk_chapter = get_content(et, bk_xpathc)
    bk_chapter_all = {}
    for j in range(0, len(bk_chapter)):
        bk_article_all = []
        bk_xpathar = '/html/body/div[2]/div[1]/div[3]/div[{}]/div[2]/span/a'.format(j + 1)
        bk_article_name = get_content(et, bk_xpathar)
        bk_article_url = get_href(et, bk_xpathar)
        for i in range(0, len(bk_article_url)):
            bk_article = {}
            bk_article['name'] = bk_article_name[i]
            bk_article['url'] = bk_article_url[i]
            bk_article['content'] = get_article_content(bk_article_url[i])
            bk_article_all.append(bk_article)
        # print(bk_article_all)
        # print(bk_article_name)
        bk_chapter_all[bk_chapter[j]] = bk_article_all
    # print(bk_article_all)
    # print(len(bk_article_all))
    print(bk_chapter_all)
    # print(len(bk_chapter_all))
    return bk_chapter_all


def get_bk_article():
    """
    This methond is used to get all the book's chapter and its detail , finally write it in the files
    :return:
    """

    # 全部书籍的名称和url地址
    bk = get_book()
    # print(bk)
    # print(len(bk))
    if not os.path.exists('电协爬虫作业'):
        os.mkdir('电协爬虫作业')
    for i in range(0, len(bk)):
        # print(bk[i])
        bk_dir = os.path.join('电协爬虫作业', bk[i]['bk_name'])
        if not os.path.exists(bk_dir):
            os.mkdir(bk_dir)
        bk_chapter = get_book_chapter(bk[i]['bk_url'])
        dic_keys = list(bk_chapter.keys())
        time.sleep(0.1)
        for j in range(0, len(dic_keys)):
            chapter_dir = os.path.join(bk_dir, dic_keys[j])
            if not os.path.exists(chapter_dir):
                os.mkdir(chapter_dir)
            bk_ch_articles = bk_chapter[dic_keys[j]]
            for k in range(0, len(bk_ch_articles)):
                chdir_name = bk_ch_articles[k]['name'] + '.txt'
                article_dir = os.path.join(chapter_dir, chdir_name)
                with open(article_dir, 'w+', encoding='utf-8') as f:
                    f.write('book:  ' + bk[i]['bk_name'] + '\n' + 'chapter:  ' + dic_keys[j] + '\n' + 'name:  ' +
                            bk_ch_articles[k]['name'] + '\n' + 'url:  ' + bk_ch_articles[k][
                                'url'] + '\n' + 'content: \n ' + bk_ch_articles[k]['content'])
    return 0


if __name__ == '__main__':
    get_bk_article()

    # 书籍中章节的和其文章的url
    # bk_chapter_all = get_book_chapter()
    # print(bk_chapter_all)
    # print(list(bk_chapter_all.keys())[1])
