from collections import Counter
from os.path import join, exists, split
import re
import numpy as np

def tag_counter():
    file_dir = 'Input'
    WebannoTSV3_file_path = join(file_dir, "train.tsv")
    sent_anno_file_path = join(file_dir, "train.txt")
    anno_sentence_counter = 0
    emo_labels = []
    sar_labels = []
    sad = []
    ang = []
    joy = []
    fea = []
    sup = []
    dis = []

    i = 0
    if exists(sent_anno_file_path):
        if sent_anno_file_path.endswith('.txt'):
            print('Loading file {0}'.format(split(sent_anno_file_path)[-1]))
            with open(sent_anno_file_path) as sent_anno:
                    for row in sent_anno:
                        i += 1
                        sent_no_break = row.split('\n')[0]
                        if '|' in sent_no_break:
                            anno_sentence_counter += 1
                            sentence = sent_no_break.split('|')[2]
                            emo_label = sent_no_break.split('|')[0]
                            sar_label = sent_no_break.split('|')[1]
                            # print(emo_label)
                            if emo_label == "joy":
                                joy.append(len(sentence.split()))
                            if emo_label == "sad":
                                sad.append(len(sentence.split()))
                            if emo_label == "fea":
                                fea.append(len(sentence.split()))
                            if emo_label == "dis":
                                dis.append(len(sentence.split()))
                            if emo_label == "ang":
                                ang.append(len(sentence.split()))
                            if emo_label == "sup":
                                sup.append(len(sentence.split()))
                            if emo_label != None:
                                emo_labels.append(emo_label)
                            if sar_label != None:
                                sar_labels.append(sar_label)

        else:
            print("Not a TSV file")
    else:
        print('Intended file does not exist!')

    emo_freq = Counter(emo_labels)
    sar_freq = Counter(sar_labels)
    print("All sentences", i)
    print("Annotated sentences", anno_sentence_counter)
    print("Emotion label distribution", emo_freq)
    print("Emotion label distribution",sar_freq)
    print()
    print("max min avg joy", max(joy), min(joy), np.average(joy))
    print("max min avg ang", max(ang), min(ang), np.average(ang))
    print("max min avg dis", max(dis), min(dis), np.average(dis))
    print("max min avg fea", max(fea), min(fea), np.average(fea))
    print("max min avg sad", max(sad), min(sad), np.average(sad))
    print("max min avg sup", max(sup), min(sup), np.average(sup))

    print("Proportion of tags")
    for i in Counter(emo_labels):
        print(i, Counter(emo_labels)[i]/len(emo_labels))

    return emo_labels

tag_counter()









