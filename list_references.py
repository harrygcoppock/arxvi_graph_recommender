"""
Reads txt files of all papers and computes tfidf vectors for all papers.
Dumps results to file tfidf.p
"""
import os
import pickle
from random import shuffle, seed
from tqdm import tqdm

import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer

from utils import Config, safe_pickle_dump

# import the graph constructor
from paper_graph import Graph


print('*'*20)
print('*'*20)
print('*'*20)

if not os.path.exists('data/txt_ref'):
  print('creating ', 'data/txt_ref')
  os.makedirs('data/txt_ref')

# read database
db = pickle.load(open(Config.db_path, 'rb'))


# Intilising Graph
ref_graph = Graph()
# read all text files for all papers into memory
txt_paths, pids = [], []
n = 0
for pid,j in tqdm(db.items()):

    ref_graph.add_vertex(j['title'].replace('\n',''))
    # print('*'*20)
    # print(j['title'])
    idvv = '%sv%d' % (j['_rawid'], j['_version'])
    txt_path = os.path.join('data', 'txt', idvv) + '.pdf.txt'
    if os.path.isfile(txt_path): # some pdfs dont translate to txt
        with open(txt_path, 'r') as f:
            paper_txt = f.read()
            paper_txt = paper_txt.replace('\n', '')
        for pid2, j2 in db.items():
            if j2['title'].replace('\n', '') in paper_txt and j2['title'].replace('\n', '') != j['title'].replace('\n', ''):
                ref_graph.add_edge((j['title'].replace('\n', ''), j2['title'].replace('\n', '')))


count = 0
num_edges = 0
for key, value in ref_graph.graph_dict.items():
    count += 1
    num_edges += len(value)
    if len(value) > 1:
        print(key, value)
    
print('total number of nodes: ', count)
print('average num edges per vertice: ',num_edges/count)
with open('graph_dict.pickle', 'wb') as handle:
    pickle.dump(ref_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

