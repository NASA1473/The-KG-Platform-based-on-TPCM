from os.path import join
from codecs import open
import re
import random


def build_corpus(split, add_words_list, add_tag_list, make_vocab=True, data_dir="./ResumeNER"):
    """读取数据"""
    assert split in ['train', 'dev', 'test']

    word_lists = []
    tag_lists = []
    with open(join(data_dir, split+".char.bmes"), 'r', encoding='utf-8') as f:
        word_list = []
        tag_list = []
        for line in f:
            if line != '\n':
                word, tag = line.strip('\n').split()
                word_list.append(word)
                tag_list.append(tag)
            else:
                word_lists.append(word_list)
                tag_lists.append(tag_list)
                word_list = []
                tag_list = []
            
    if split == 'train':
        word_lists = word_lists + add_words_list[: int(0.8 * len(add_words_list))]
        tag_lists = tag_lists + add_tag_list[: int(0.8 * len(add_tag_list))]
    elif split == 'dev':
        word_lists = word_lists + add_words_list[int(0.8 * len(add_words_list)): int(0.9 * len(add_words_list))]
        tag_lists = tag_lists + add_tag_list[int(0.8 * len(add_tag_list)): int(0.9 * len(add_words_list))]
    else:
        word_lists = word_lists + add_words_list[int(0.9 * len(add_words_list)): ]
        tag_lists = tag_lists + add_tag_list[int(0.9 * len(add_tag_list)): ]

    # 如果make_vocab为True，还需要返回word2id和tag2id
    if make_vocab:
        word2id = build_map(word_lists)
        tag2id = build_map(tag_lists)
        return word_lists, tag_lists, word2id, tag2id
    else:
        return word_lists, tag_lists

def build_corpus_origin(split, make_vocab=True, data_dir="./ResumeNER"):
    """读取数据"""
    assert split in ['train', 'dev', 'test']

    word_lists = []
    tag_lists = []
    with open(join(data_dir, split+".char.bmes"), 'r', encoding='utf-8') as f:
        word_list = []
        tag_list = []
        for line in f:
            if line != '\n':
                word, tag = line.strip('\n').split()
                word_list.append(word)
                tag_list.append(tag)
            else:
                word_lists.append(word_list)
                tag_lists.append(tag_list)
                word_list = []
                tag_list = []

    # 如果make_vocab为True，还需要返回word2id和tag2id
    if make_vocab:
        word2id = build_map(word_lists)
        tag2id = build_map(tag_lists)
        return word_lists, tag_lists, word2id, tag2id
    else:
        return word_lists, tag_lists

def build_map(lists):
    maps = {}
    for list_ in lists:
        for e in list_:
            if e not in maps:
                maps[e] = len(maps)

    return maps

def process_BosonNLP_data(data_dir="./ResumeNER"):
    with open(data_dir + "/BosonNLP_NER_6C.txt", "r", encoding="utf-8") as f:
        total_lines = [line.strip() for line in f.readlines()]

    total_lines = [line for line in total_lines if line != '']
    cutLineFlag = ["！", "。", "!"]
    sentenceList = []
    for words in total_lines:
        oneSentence = ""
        for word in words:
            if word not in cutLineFlag:
                oneSentence = oneSentence + word
            else:
                oneSentence = oneSentence + word
                if oneSentence.__len__() > 4:
                    sentenceList.append(oneSentence.strip())
                oneSentence = ""

    return transfer_str2label(sentenceList)

def seperate_ch(sequence):
    return [ch for ch in sequence]

def decode(seq):
    # new_seq = ""
    # new_tag = ""
    if "time" in seq:
        new_seq = seq[7:-2]
        new_tag = ["O"] * len(new_seq)
    elif "location" in seq:
        new_seq = seq[11:-2]
        if len(new_seq) == 2:
            new_tag = ["B-LOC", "E-LOC"]
        else:
            new_tag = ["B-LOC"] + ["M-LOC"] * (len(new_seq)-2) + ["E-LOC"]
    elif "person_name" in seq:
        new_seq = seq[14:-2]
        if len(new_seq) == 1:
            new_tag = ["S-NAME"]
        elif len(new_seq) == 2:
            new_tag = ["B-NAME", "E-NAME"]
        else:
            new_tag = ["B-NAME"] + ["M-NAME"] * (len(new_seq)-2) + ["E-NAME"]
    elif "org_name" in seq:
        new_seq = seq[11:-2]
        if len(new_seq) == 1:
            new_tag = ["S-ORG"]
        elif len(new_seq) == 2:
            new_tag = ["B-ORG", "E-ORG"]
        else:
            new_tag = ["B-ORG"] + ["M-ORG"] * (len(new_seq)-2) + ["E-ORG"]
    elif "company_name" in seq:
        new_seq = seq[15:-2]
        if len(new_seq) == 1:
            new_tag = ["S-COM"]
        elif len(new_seq) == 2:
            new_tag = ["B-COM", "E-COM"]
        else:
            new_tag = ["B-COM"] + ["M-COM"] * (len(new_seq)-2) + ["E-COM"]
    elif "product_name" in seq:
        new_seq = seq[15:-2]
        if len(new_seq) == 1:
            new_tag = ["S-PROD"]
        elif len(new_seq) == 2:
            new_tag = ["B-PROD", "E-PROD"]
        else:
            new_tag = ["B-PROD"] + ["M-PROD"] * (len(new_seq)-2) + ["E-PROD"]
    
    return new_seq, new_tag

def transfer_str2label(sentenceList):
    sent_list = []
    tag_list = []
    for sent in sentenceList:
        if "{{" in sent and len(sent) > 4:
            start = [item.start() for item in re.finditer("{{", sent)]
            end = [item.end() for item in re.finditer("}}", sent)]
            if len(start) != len(end):
                continue

            left = 0
            new_str = ""
            new_tag = []
            for i in range(len(start)):
                new_str = new_str + sent[left: start[i]]
                new_tag = new_tag + ['O'] * (start[i]-left)
                sub_str, sub_tag = decode(sent[start[i]: end[i]])
                new_str = new_str + sub_str
                new_tag = new_tag + sub_tag
                left = end[i]

            new_str = new_str + sent[left: len(sent)]
            new_tag = new_tag + ['O'] * (len(sent)-left)
        
        if len(new_str) == len(new_tag):
            sent_list.append(seperate_ch(new_str))
            tag_list.append(new_tag)
    
    shuffle_index = list(range(len(sent_list)))
    random.shuffle(shuffle_index)
    return [sent_list[i] for i in shuffle_index], [tag_list[i] for i in shuffle_index]

