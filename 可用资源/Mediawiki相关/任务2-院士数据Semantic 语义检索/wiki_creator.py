"""
  @author Jay Liu
  @create_time 2021/10/26 18:27
  @email 1299870737@qq.com
"""

import mwclient
import csv
import time

ua = '849692951@qq.com'


# ！！！不要直接用！！！参数改成你自己的
# 第一个参数是IP地址，path参数是wiki的文件夹名，看看/var/www/html/下面wiki名字是啥
# site = mwclient.Site("47.117.143.163/", scheme='http', path='mediawiki/', clients_useragent=ua)

# 如果是本地安装的mediawiki的话，用下面这行
site = mwclient.Site("localhost/", scheme='http', path='mediawiki/', clients_useragent=ua)

# 在wiki上创建Bot用户，更改到Bot用户组下面
site.login("Bot", "868785836QQ.")

if __name__ == '__main__':
    origin_list = []
    with open('aca.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        origin_header = next(csv_reader)
        for row in csv_reader:
            origin_list.append(row)

    for item in origin_list:
        page = site.pages['首页/院士/{}'.format(item[1])]
        duplicate_count = 1
        while page.exists:
            page = site.pages['首页/院士/{}_{}'.format(item[1], duplicate_count)]
            print('发现重名院士{}'.format(duplicate_count))

        template1 = f'{{院士信息模板|头像={item[11]}' \
                    f'|性别={item[3]}' \
                    f'|出生日期={item[5]}'\
                    f'|当选年份={item[6].split()[1]}' \
                    f'|学部={item[7]}}}'

        template2 = f'{{院士内容模板|' \
                    f'个人简介={item[9]}' \
                    f'|学院评价={item[12]}' \
                    f'|主要学历={item[13]}' \
                    f'|主要经历={item[14]}' \
                    f'|人生点滴={item[15]}' \
                    f'}}'
        template3 = f'[[Category:{item[7]}]][[Category:{item[4]}]][[Category:{item[6].split()[0]}]]'
        template1 = '{' + template1 + '}'
        template2 = '{' + template2 + '}'
        page.edit(template1+template2+template3)

        print('已添加{}院士数据'.format(item[1]))
        # 这里可以调整循环的间歇时间
        # 我这里为了避免操作过快把服务器搞崩，设置了1s一次写入，本机的话可以调成0.1试试
        time.sleep(1)
