from kgqa.query_graph import *
from kgqa.ltp import *

examples = [
    '乔治·韦斯莱的叔叔是谁？',
    '哈利·波特的侄女是谁？',
    '乔治·韦斯莱从属于哪里？',
    '哈米什·麦克法兰的职业是？',
]

print('This is an example:')
q = examples[0]
print('Q:%s'%(q))
array = get_target_array(q)
res = get_KGQA_answer(array)
print('A:')
for i in res:
    print(i[0])
print()

print('Have fun!')
while True:
    q = input('Q:')
    array = get_target_array(q)
    res = get_KGQA_answer(array)
    print('A:')
    for i in res:
        print(i[0])
    print()
