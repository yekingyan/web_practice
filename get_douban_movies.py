from getStatuscode_headers_body import (
    get,
    log,
)


def page_of_movies():
    """
    获取top250的所有url
    :return: URL字典
    """
    a = 0
    s = {}
    while a < 250:
        url = f"https://movie.douban.com/top250?start={a}&filter="
        a += 25
        key = int(a/25)
        s[key] = str(url)
    # log(s)
    return s


def get_movies_title(url):
    """
    获取电影标题
    :param url: 豆瓣电影top250url
    :return: 电影标题的字典
    """
    code, header, body = get(url)
    a = body.split('<span class="title">')
    n = 0
    s = {}
    for i in a:
        # log(i, "______________", n)
        n += 1
        s[n] = i
    # 只取电影正标题
    titles = {}
    num = 0
    for key in s:
        title = s[key].split('<')[0]
        # 副标题带分号;
        if ";" not in title:
            titles[num] = title
            num += 1
    # 第0个不是电影，删掉
    del titles[0]
    # log(titles)
    return titles


def get_grade_and_quote(url):
    """
    返回分数的字典,和短评的字典
    """
    code, header, body = get(url)
    ratting_nums = body.split('<span class="rating_num" property="v:average">')
    i = 0
    grades = {}
    quotes = {}
    for rootnum in ratting_nums:
        grade = rootnum.split('<')[0]
        grades[i] = grade

        # quote
        if "quote" in rootnum:
            quote = rootnum.split('<p class="quote">')[1]
            quote = quote.split('</span>')[0]
            quote = quote.split('>')[1]
        else:
            quote = "没有短评"
        quotes[i] = quote

        i += 1

    del quotes[0]
    del grades[0]
    # log("_______\n", grades, quotes)
    return grades, quotes


def people_num(url):
    """
    返回评论人数的字典 
    """
    code, header, body = get(url)
    people_nums = body.split("人评价</span>")
    nums = {}
    i = 0
    for num in people_nums:
        num = num.split("span>")
        a = len(num)
        nums[i+1] = num[a-1]
        i += 1
    del nums[26]
    return nums


def get_one_page(url):
    """
    返回一页的结果
    """
    titles = get_movies_title(url)
    grades, quotes = get_grade_and_quote(url)
    peopleNum = people_num(url)
    result = {}
    for i in range(1, 26):
        title = titles[i]
        grade = grades[i]
        quote = quotes[i]
        people = peopleNum[i]
        s = f"{title}   评分：{grade}\n{quote}\n{people}人评价\n\n"
        # log(s)
        result[i] = str(s)
    # log(result)
    return result


def get_all():
    result = {}
    for i in range(1, 11):
        url = page_of_movies()[i]
        s = get_one_page(url)
        result[i] = s
    # log(result)
    return result


def write_txt():
    """写入txt文件"""
    # 运行前清旧数据
    with open('movies_top250.txt', "w") as f:
        f.truncate()

    s = get_all()
    # 解开字典
    for sonDict in s:
        for key in s[sonDict]:
            movie = s[sonDict][key]
            # 写入
            with open('movies_top250.txt', 'a', encoding='utf-8') as f:
                f.write(movie)
                log(movie)


if __name__ == '__main__':
    write_txt()