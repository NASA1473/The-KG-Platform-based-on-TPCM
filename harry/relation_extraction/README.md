# 介绍
follow了 https://github.com/taorui-plus/OpenNRE
使用哈工大的BERT-wwm在20w中文人物关系数据上训练关系抽取模型；
将《哈利波特》原文进行分句，并根据此前在哈利波特维基上爬取的实体名筛选出含有多个实体的句子；
使用训练完成的关系抽取模型抽取每个句子中实体间的关系；
对得到的关系进行数据清洗，得到最终干净的关系数据。

# 文件说明
extract_relation_and_clean.ipynb 关系的抽取，以及进行清理后进行简单推理
Harry_Potter.txt 《哈利波特》原文
./data/harryid.csv 从网站上爬取的实体名
./data/harryRel.csv 从网站上爬取的关系
./data/relation_raw.csv 从原文中提取出的原生关系
./data/relation_clean.csv 对上一个文件进行清洗
./data/relation_infered.csv 对清洗过的文件进行简单的推理，例如 A 师生 B 关系能倒退回 B 学生 A 关系等
train_people_chinese_bert_softmax.py 训练BERT中文关系抽取模型

# 模型训练
## 使用前准备
1.bert模型下载：在./pretrain/下面放置chinese_wwm_pytorch模型，下载地址：https://github.com/ymcui/Chinese-BERT-wwm
2.生成数据集：在./benchmark/people-relation/下执行gen.py,生产中文人物关系数据，具体脚本中有说明。
3.配置环境变量：配置环境变量openNRE=项目位置，或在./opennre/pretrain.py中将
  default_root_path = os.path.join(os.getenv('openNRE'), '.')
  改成自己的目录路径
## 开始训练
运行train_people_chinese_bert_softmax.py训练BERT中文关系抽取模型

# 关系抽取
1.对《哈利波特》原文进行分句，并根据此前在哈利波特维基上爬取的实体名筛选出含有多个实体的句子；
2.导入训练好的关系抽取模型，抽取每个句子中的关系；

# 数据清洗
1.抽取的关系中包括父母亲、夫妻、祖父母等，但从网站上爬取的关系数据中亲属关系已经非常详细的，因此我们这里主要关注师生、合作等关系；
2.由于不同句子可能会包含相同的实体对，导致最终可能一个实体对会存在多个关系，我们选择概率最高的一组作为最终的关系；
3.句子中的实体对还可能存在歧义，我们使用候选实体中在文章中出现频率最多的实体来替换；
4.最终手动剔除掉一些明显的错误，得到最终的关系数据；
5.对已抽取得到的关系进行简单推理，例如
  A 师生 B 关系能倒退回 B 学生 A 关系；
  A 同门 B  B 同门 C 能推理出 A 同门 C


-----

----
----



以下是原工程内容
# OpenNRE

OpenNRE is an open-source and extensible toolkit that provides a unified framework to implement relation extraction models. This package is designed for the following groups:

* **New to relation extraction**: We have hand-by-hand tutorials and detailed documents that can not only enable you to use relation extraction tools, but also help you better understand the research progress in this field.
* **Developers**: Our easy-to-use interface and high-performance implementation can acclerate your deployment in the real-world applications. Besides, we provide several pretrained models which can be put into production without any training.
* **Researchers**: With our modular design, various task settings and metric tools, you can easily carry out experiments on your own models with only minor modification. We have also provided several most-used benchmarks for different settings of relation extraction.
* **Anyone who need to submit an NLP homework to impress their professors**: With state-of-the-art models, our package can definitely help you stand out among your classmates!

This package is mainly contributed by [Tianyu Gao](https://github.com/gaotianyu1350), [Xu Han](https://github.com/THUCSTHanxu13), [Shulian Cao](https://github.com/ShulinCao), [Lumin Tang](https://github.com/Tsingularity), [Yankai Lin](https://github.com/Mrlyk423), [Zhiyuan Liu](http://nlp.csai.tsinghua.edu.cn/~lzy/)

## What is Relation Extraction

Relation extraction is a natural language processing (NLP) task aiming at extracting relations (e.g., *founder of*) between entities (e.g., **Bill Gates** and **Microsoft**). For example, from the sentence *Bill Gates founded Microsoft*, we can extract the relation triple (**Bill Gates**, *founder of*, **Microsoft**). 

Relation extraction is a crucial technique in automatic knowledge graph construction. By using relation extraction, we can accumulatively extract new relation facts and expand the knowledge graph, which, as a way for machines to understand the human world, has many downstream applications like question answering, recommender system and search engine. 

## How to Cite

A good research work is always accompanied by a thorough and faithful reference. If you use or extend our work, please cite the following paper:

```
    @inproceedings{han2019opennre,
      title={OpenNRE: An Open and Extensible Toolkit for Neural Relation Extraction},
      author={Han, Xu and Gao, Tianyu and Yao, Yuan and Ye, Deming and Liu, Zhiyuan and Sun, Maosong },
      booktitle={Proceedings of EMNLP},
      year={2019}
    }
```

It's our honor to help you better explore relation extraction with our OpenNRE toolkit!

## Papers and Document

If you want to learn more about neural relation extraction, visit another project of ours ([NREPapers](https://github.com/thunlp/NREPapers)).

You can refer to our [document](https://opennre-docs.readthedocs.io/en/latest/) for more details about this project.

## Install 

### Install as A Python Package

We are now working on deploy OpenNRE as a Python package. Coming soon!

### Using Git Repository

Clone the repository from our github page (don't forget to star us!)

```bash
git clone https://github.com/thunlp/OpenNRE.git
```

If it is too slow, you can try
```
git clone https://github.com/thunlp/OpenNRE.git --depth 1
```

Then install all the requirements:

```
pip install -r requirements.txt
```

Then install the package with 
```
python setup.py install 
```

If you also want to modify the code, run this:
```
python setup.py develop
```

Note that we have excluded all data and pretrain files for fast deployment. You can manually download them by running scripts in the ``benchmark`` and ``pretrain`` folders. For example, if you want to download FewRel dataset, you can run

```bash
bash benchmark/download_fewrel.sh
```

## Easy Start

Add `OpenNRE` directory to the `PYTHONPATH` environment variable, or open a python session under the `OpenNRE` folder. Then import our package and load pre-trained models.

```python
>>> import opennre
>>> model = opennre.get_model('wiki80_cnn_softmax')
```

Note that it may take a few minutes to download checkpoint and data for the first time. Then use `infer` to do sentence-level relation extraction

```python
>>> model.infer({'text': 'He was the son of Máel Dúin mac Máele Fithrich, and grandson of the high king Áed Uaridnach (died 612).', 'h': {'pos': (18, 46)}, 't': {'pos': (78, 91)}})
('father', 0.5108704566955566)
```

You will get the relation result and its confidence score.

For higher-level usage, you can refer to our [document](https://opennre-docs.readthedocs.io/en/latest/).

## Google Group

If you want to receive our update news or take part in discussions, please join our [Google Group](https://groups.google.com/forum/#!forum/opennre/join)
