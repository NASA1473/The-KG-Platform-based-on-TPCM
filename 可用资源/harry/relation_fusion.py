raw_relations = 'get_raw_data/relations_clean.txt'
extracted_relations = 'relation_extraction/data/relation_clean.csv'
relations_final = 'relations_final.csv'

data = []
with open(raw_relations, 'r', encoding='utf-8') as f:
    for x in f.readlines():
        d = x.strip().split()
        data.append([d[0], d[-1], d[1]])

def replace_dot(s):
    return s.replace('.', '·')

def remove_repeated(data):
    res = set()
    for d in data:
        res.add((d[0],d[1],d[2]))
    return sorted(list(res))


with open(extracted_relations, 'r', encoding='utf-8') as f:
    for x in f.readlines():
        d = x.strip().split(',')
        data.append([replace_dot(d[0]), replace_dot(d[1]), replace_dot(d[2])])


data = remove_repeated(data)
with open(relations_final, 'w', encoding='utf-8') as f:
    for d in data:
        f.write('%s,%s,%s\n'%(d[0],d[1],d[2]))

