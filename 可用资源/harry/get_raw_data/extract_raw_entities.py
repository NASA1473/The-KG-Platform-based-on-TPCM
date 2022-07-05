from requests_html import HTMLSession

seeds = ['Category:霍格沃茨职工', 
         'Category:霍格沃茨学生',
         'Category:第一次凤凰社',
         'Category:魔法部雇员',
         'Category:食死徒',
         'Category:麻瓜']

root = 'https://harrypotter.fandom.com/zh/wiki/'
# # url = 'https://harrypotter.fandom.com/zh/wiki/Category:%E9%9C%8D%E6%A0%BC%E6%B2%83%E8%8C%A8%E5%AD%A6%E7%94%9F'
# session = HTMLSession()
# response = session.get(url)
# a_list = response.html.find('a')
# titles = []
# for a in a_list:
#     if a.attrs.get('class', '') == ('category-page__member-link', ):
#         titles.append(a.attrs['title'])
# print(titles)

# for t in titles:
#     if 'Category' in t:

all_entities = []
current_category = [x for x in seeds]
have_seen_categories = set([x for x in seeds])

while len(current_category) >= 1:
    seed = current_category.pop(0)
    print('visiting', seed)
    url = root + seed
    session = HTMLSession()
    response = session.get(url)
    a_list = response.html.find('a')
    cur_ents = []
    for a in a_list:
        if a.attrs.get('class', '') == ('category-page__member-link', ):
            cur_ents.append(a.attrs['title'])
    for t in cur_ents:
        if 'Template' in t: continue
        if 'Category' in t:
            if t not in have_seen_categories:
                current_category.append(t)
                have_seen_categories.add(t)
        else:
            all_entities.append(t)

all_entities = sorted(list(set(all_entities)))
with open('entities.txt', 'w', encoding='utf-8') as f:
    for t in all_entities:
        f.write(t.strip() + '\n')
