import sys
sys.path.append('../')
from neo_db.config import graph


def query(name):
    data = graph.run(
    "match(p )-[r]->(n:Entity{Name:'%s'}) return  p.Name,r.relation,n.Name\
        Union all\
    match(p:Entity {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name"
        % (name, name)
    )
    data = list(data)
    return get_json_data(data)


def get_json_data(data):
    json_data={'data':[],"links":[]}
    d=[]
    for i in data:
        d.append(i['p.Name'])
        d.append(i['n.Name'])
        d=list(set(d))
    name_dict={}
    count=0
    for j in d:
        j_array=j.split("_")
    
        data_item={}
        name_dict[j_array[0]]=count
        count+=1
        data_item['name']=j_array[0]
        json_data['data'].append(data_item)
    for i in data:
        link_item = {}
        link_item['source'] = name_dict[i['p.Name']]
        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    return json_data


def get_KGQA_answer(array):
    # print('array', array)
    data_array=[]
    for i in range(1):
        if i==0:
            name=array[0]
        else:
            name=data_array[-1]['p.Name']
        data = graph.run(
            "match(p)<-[r:%s{relation: '%s'}]-(n:Entity{Name:'%s'}) return  p.Name,n.Name,r.relation" % (
                array[i+1], array[i+1], name)
        )
        data = list(data)
        data_array.extend(data)
        # print("data", data)
        # print("==="*36)

    return data_array


if __name__ == '__main__':
    a1 = ['哈米什·麦克法兰', '职业', '的']
    a2 = ['哈利·波特', '侄女', '的']
    a3 = ['乔治·韦斯莱', '从属']
    a4 = ['乔治·韦斯莱', '叔叔', '的']
    res = get_KGQA_answer(a2)
    for i in res:
        print(i[0])
