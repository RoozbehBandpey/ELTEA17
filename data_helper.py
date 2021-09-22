import numpy as np
import pandas as pd
import pickle
import itertools
from collections import defaultdict
from collections import Counter
import re
import json
import os
from os.path import join, exists, split
from gensim.models import word2vec



def train_word2vec(data, vocabulary, num_features=300, min_word_count=1, context=10):
    """
    Trains, saves, loads Word2Vec model
    Returns initial weights for embedding layer.
    """
    num_workers = 2  # Number of threads to run in parallel
    downsampling = 1e-3  # Downsample setting for frequent words

    # Initialize and train the model
    print('Training Word2Vec model...')
    sentences = [i['tokens'] for i in data]
    embedding_model = word2vec.Word2Vec(sentences, workers=num_workers,
                                            size=num_features, min_count=min_word_count,
                                            window=context, sample=downsampling)

    # If we don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    embedding_model.init_sims(replace=True)



    # add unknown words
    embedding_weights = {word: np.array(embedding_model[word]) if word in embedding_model else
    np.random.uniform(-0.25, 0.25, embedding_model.vector_size)
                         for word in vocabulary}

    return embedding_weights



def build_data(data_train, train_ratio=0.9, clean_string=True):
    input_dir = "data"
    data_train_path = join(input_dir, data_train)
    if exists(data_train_path):
        json_file_annotation_all = open(data_train_path, 'r')
        annotation_all = json.load(json_file_annotation_all)

        tweets = []
        vocab = defaultdict(float)
        emo_labels = []
        sentences = []
        for item in annotation_all:
            sentence = item['text']
            tokens = item['tokens']
            emo_label = item['emotion']
            sentences.append(sentence)
            if emo_label == 'joy':
                emo_labels.append([1, 0, 0, 0, 0, 0])
                y = 0
            if emo_label == 'sad':
                emo_labels.append([0, 1, 0, 0, 0, 0])
                y = 1
            if emo_label == 'dis':
                emo_labels.append([0, 0, 1, 0, 0, 0])
                y = 2
            if emo_label == 'sup':
                emo_labels.append([0, 0, 0, 1, 0, 0])
                y = 3
            if emo_label == 'ang':
                emo_labels.append([0, 0, 0, 0, 1, 0])
                y = 4
            if emo_label == 'fea':
                emo_labels.append([0, 0, 0, 0, 0, 1])
                y = 5
            if clean_string:
                orig_tweet = clean_str(sentence)
            else:
                orig_tweet = sentence.lower()
            words = set(tokens)
            for word in words:
                vocab[word] += 1
            data = {'y': y,
                     'text': orig_tweet,
                     'num_words': len(tokens),
                     'split': int(np.random.rand() < train_ratio),
                     'tokens': tokens}
            tweets.append(data)

        return tweets, vocab
    else:
        print("File does not exist")


def get_W(word_vecs, k):
    """
    Get word matrix. W[i] is the vector for word indexed by i
    """
    vocab_size = len(word_vecs)
    word_idx_map = dict()
    W = np.zeros(shape=(vocab_size + 1, k), dtype=np.float32)
    W[0] = np.zeros(k, dtype=np.float32)
    i = 1
    for word in word_vecs:
        W[i] = word_vecs[word]
        word_idx_map[word] = i
        i += 1
    return W, word_idx_map


def load_bin_vec(fname, vocab):
    """
    Loads 300x1 word vecs from Google (Mikolov) word2vec
    """
    word_vecs = {}
    with open(fname, 'rb') as f:
        header = f.readline()
        vocab_size, layer1_size = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in range(vocab_size):
            word = []
            while True:
                ch = f.read(1)
                if ch == b' ':
                    word = ''.join(word)
                    break
                if ch != b'\n':
                    new_ch = str(ch).split('\'')[1]
                    word.append(new_ch)
            if word in vocab:
                word_vecs[word] = np.fromstring(f.read(binary_len), dtype='float32')
            else:
                f.read(binary_len)
    return word_vecs


def load_glove_wordvecs(fname, vocab):
    word_vecs = {}
    with open(fname, 'r', encoding="utf8") as f:
        for line in f:
            splitLine = line.split()
            word = splitLine[0]
            embedding = np.array([float(val) for val in splitLine[1:]])
            if word in vocab:
                word_vecs[word] = embedding

    return word_vecs

def append_vectors(fname, vocab, w2v):
    Matrix_dir = 'Matrix'
    matrix_path = join(Matrix_dir, fname)
    w2v_dict_file_name = open(matrix_path, "rb")
    w2v_dict = pickle.load(w2v_dict_file_name)
    w2v_dict_file_name.close()

    new_w2v = {}
    for word, y_v, z_v in zip(vocab, w2v, w2v_dict):
        new_vec = np.concatenate((w2v[word],w2v_dict[word]))
        new_w2v.__setitem__(word, new_vec)

    return new_w2v

def add_unknown_words(word_vecs, vocab, k, min_df=1):
    """
    For words that occur in at least min_df documents, create a separate word vector.
    0.25 is chosen so the unknown vectors have (approximately) same variance as pre-trained ones
    """
    i = 0
    for word in vocab:
        if word not in word_vecs and vocab[word] >= min_df:
            i += 1
            word_vecs[word] = np.random.uniform(-0.25, 0.25, k)
    return i, word_vecs

def random_word_vectors(vocab, k, min_df=1):
    """

    """
    word_vecs = {}
    for word in vocab:
        word_vecs[word] = np.random.uniform(-0.5, 0.5, k)
    return word_vecs


def clean_str(string):
    """
    Tokenization/string cleaning for the dataset.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

