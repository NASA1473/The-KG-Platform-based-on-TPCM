from bs4 import BeautifulSoup
import requests
import re
root = 'https://harrypotter.fandom.com/zh/wiki/'


def clean_string(s):
    s = re.sub(r'\[\d*\]', '', s)
    return s


def extract_entity(ent):
    url = root + ent
    response = requests.get(url=url).content
    soup = BeautifulSoup(response, 'html.parser')
    e1 = ent
    relations = []
    for p in soup.find_all('div', attrs={'class': 'pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background'}):
        if p.text == '家庭信息':
            for np in p.next_siblings:
                if np.find_all('div')[0].text == '家庭成员':
                    for relation in np.find_all('li'):
                        tmp = relation.text.split()
                        if len(tmp) >= 2:
                            r = (clean_string(tmp[1][1:-1]), clean_string(tmp[0]))
                            relations.append(r)
        elif p.text == '关系信息':
            for np in p.next_siblings:
                r = clean_string(np.find_all('div')[0].text)
                for e2 in np.find_all('li'):
                    e = clean_string(e2.text)
                    if len(e.split()) > 1:
                        for ee in e.split():
                            relations.append((r, ee))
                    else:
                        relations.append((r, e))
    relations = [(e1, r[0], r[1]) for r in relations]
    return relations



all_relations = set()

with open('entities.txt', 'r', encoding='utf-8') as f:
    ents = [e.strip() for e in f.readlines()]
    for e in ents:
        print('processing', e)
        relations = extract_entity(e)
        for r in relations:
            all_relations.add(r)


all_relations = sorted(list(all_relations))
with open('relations.txt', 'w', encoding='utf-8') as f:
    for r in all_relations:
        f.write('%s\t%s\t%s\n' % (r[0], r[1], r[2]))

