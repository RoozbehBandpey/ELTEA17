from os.path import join, exists, split
import csv
from collections import Counter
from collections import OrderedDict
import sqlite3
import json
import numpy as np


class DatabaseManager(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    def insert(self, arg, val):
        self.cur.execute(arg, val)
        self.conn.commit()
        return self.cur

    def __del__(self):
        self.conn.close()


def read_from_DB(file_dir, DB_file_name, raw_file):
    DB_path_tweets = join(file_dir, DB_file_name)
    raw_file_path = join(file_dir, raw_file)
    if exists(DB_path_tweets):
        print("\nReading from database...")
        dbmgr = DatabaseManager(DB_path_tweets)


        text = "%you to all of my mutuals who replied%"
        cur = text_select_query(dbmgr, text)

        print(cur.fetchall())


        dbmgr.__del__()
    else:
        print("Database {0} does not exist!")

def text_select_query(DB_Object, text):
    # cur = DB_Object.query('''SELECT * FROM Tbl_Tweets WHERE text = %s''' % text)
    cur = DB_Object.query("SELECT * FROM Tbl_Tweets WHERE text LIKE '%s'" % text)
    return cur

def create_jason(processed_file_dir, file_name, data):
    file_path_tweets = join(processed_file_dir, file_name)
    if exists(file_path_tweets):
        print('\'%s\' file already exists' % split(file_path_tweets)[-1])
    else:

        if file_name.endswith('.json'):
            print('\'%s\' is been writing' % split(file_path_tweets)[-1])
            output = open(file_path_tweets, 'w')
            tweets = []
            for item in data.fetchall():
                datarow_full = {item[0]: {"text": item[1],
                                          "date": item[2],
                                          "link": item[3],
                                          "emoji": item[4],
                                          "hashtag": item[5],
                                          "num_words": item[6],
                                          "filter": item[7],
                                          "select":0 }}
                tweets.append(datarow_full)
            json.dump(tweets, output, indent=4)
        else:
            print("Output file should be a JSON file, e.g., output.json")

def data_builder(file_dir):
    WebannoTSV3_file_path = join(file_dir, "train.tsv")
    sent_anno_file_path = join(file_dir, "train.txt")
    sentence_counter = 0
    sentence_counter_2 = 0
    header = []
    i = 0
    output_1 = open('Input/sentence_level_annotation.json', 'w')
    output_2 = open('Input/token_level_annotation.json', 'w')
    sentence_level_annotation = []
    token_level_annotation = []
    if exists(WebannoTSV3_file_path) and exists(sent_anno_file_path):
        if WebannoTSV3_file_path.endswith('.tsv') and sent_anno_file_path.endswith('.txt'):
            print('Loading file {0} and {1}'.format(split(WebannoTSV3_file_path)[-1], split(sent_anno_file_path)[-1]))
            with open(WebannoTSV3_file_path) as token_anno, open(sent_anno_file_path) as sent_anno:
                token_anno = csv.reader(token_anno)
                sent_anno = sent_anno.readlines()

                previous_anger = ''
                previous_anticipation = ''
                previous_disgust = ''
                previous_fear = ''
                previous_joy = ''
                previous_other = ''
                previous_sadness = ''
                previous_surprise = ''
                previous_trust = ''
                previous_experiencer = ''
                previous_target = ''
                previous_cause = ''


                BIO_annotation = []
                full_data_structure = []
                for row in token_anno:
                    if len(row) != 0:  # Check for empty\n row
                        if '#T_SP' in row[0] or '#FORMAT' in row[0]:
                            header.append(row[0])
                        else:
                            new_row = row[0].split('\t')
                            if len(new_row) == 1: #Check for full sentence
                                BIO_sentence = []
                                sentence_counter += 1
                                sentence = new_row[0].split('#Text=')[1]
                                sent_anno_temp = sent_anno[sentence_counter - 1].split('\n')[0]
                                if '|' in sent_anno_temp:
                                    sentence_counter_2 += 1
                                    sent_anno_temp_list = sent_anno_temp.split('|')
                                    sent_anno_sentence = sent_anno_temp_list[2] #Better one
                                    emotion_tag = sent_anno_temp_list[0]
                                    sarcasm_tag = sent_anno_temp_list[1]
                                    datarow_sentence_level = {"sent_num": str(sentence_counter_2), "text": sent_anno_sentence, "emotion": emotion_tag , "sarcasm":sarcasm_tag}
                                    sentence_level_annotation.append(datarow_sentence_level)
                                else:
                                    print(sent_anno_temp)

                            elif len(new_row)== 6: #Check for annotation
                                sent_number = new_row[0].split('-')[0]
                                token_number = new_row[0].split('-')[1]
                                token_starts = new_row[1].split('-')[0]
                                token_ends = new_row[1].split('-')[1]
                                token = new_row[2]
                                emotion_annotation = new_row[3].split('|')
                                role_annotation = new_row[4].split('|')


                                anger = 'O'
                                anticipation = 'O'
                                disgust = 'O'
                                fear = 'O'
                                joy = 'O'
                                other = 'O'
                                sadness = 'O'
                                surprise = 'O'
                                trust = 'O'

                                experiencer = 'O'
                                target = 'O'
                                cause = 'O'

                                emotion_item_buffer = []
                                role_item_buffer = []

                                for item in emotion_annotation:
                                    if 'anger' in item:
                                        emotion_item_buffer.append('anger')
                                        if '[' not in item:
                                            anger = 'B-anger'
                                        elif Counter(emotion_item_buffer)['anger'] <= 1:
                                            anger = 'B-anger'
                                            if item == previous_anger:
                                                anger = 'I-anger'
                                            else:
                                                previous_anger = item

                                    if 'anticipation' in item:
                                        emotion_item_buffer.append('anticipation')
                                        if '[' not in item:
                                            anticipation = 'B-anticipation'
                                        elif Counter(emotion_item_buffer)['anticipation'] <= 1:
                                            anticipation = 'B-anticipation'
                                            if item == previous_anticipation:
                                                anticipation = 'I-anticipation'
                                            else:
                                                previous_anticipation = item

                                    if 'disgust' in item:
                                        emotion_item_buffer.append('disgust')
                                        if '[' not in item:
                                            disgust = 'B-disgust'
                                        elif Counter(emotion_item_buffer)['disgust'] <= 1:
                                            disgust = 'B-disgust'
                                            if item == previous_disgust:
                                                disgust = 'I-disgust'
                                            else:
                                                previous_disgust = item

                                    if 'fear' in item:
                                        emotion_item_buffer.append('fear')
                                        if '[' not in item:
                                            fear = 'B-fear'
                                        elif Counter(emotion_item_buffer)['fear'] <= 1:
                                            fear = 'B-fear'
                                            if item == previous_fear:
                                                fear = 'I-fear'
                                            else:
                                                previous_fear = item


                                    if 'joy' in item:
                                        emotion_item_buffer.append('joy')
                                        if '[' not in item:
                                            joy = 'B-joy'
                                        elif Counter(emotion_item_buffer)['joy'] <= 1:
                                            joy = 'B-joy'
                                            if item == previous_joy:
                                                joy = 'I-joy'
                                            else:
                                                previous_joy = item

                                    if 'other' in item:
                                        emotion_item_buffer.append('other')
                                        if '[' not in item:
                                            other = 'B-other'
                                        elif Counter(emotion_item_buffer)['other'] <= 1:
                                            other = 'B-other'
                                            if item == previous_other:
                                                other = 'I-other'
                                            else:
                                                previous_other = item

                                    if 'sadness' in item:
                                        emotion_item_buffer.append('sadness')
                                        if '[' not in item:
                                            sadness = 'B-sadness'
                                        elif Counter(emotion_item_buffer)['sadness'] <= 1:
                                            sadness = 'B-sadness'
                                            if item == previous_sadness:
                                                sadness = 'I-sadness'
                                            else:
                                                previous_sadness = item

                                    if 'surprise' in item:
                                        emotion_item_buffer.append('surprise')
                                        if '[' not in item:
                                            surprise = 'B-surprise'
                                        elif Counter(emotion_item_buffer)['surprise'] <= 1:
                                            surprise = 'B-surprise'
                                            if item == previous_surprise:
                                                surprise = 'I-surprise'
                                            else:
                                                previous_surprise = item

                                    if 'trust' in item:
                                        emotion_item_buffer.append('trust')
                                        if '[' not in item:
                                            trust = 'B-trust'
                                        elif Counter(emotion_item_buffer)['trust'] <= 1:
                                            trust = 'B-trust'
                                            if item == previous_trust:
                                                trust = 'I-trust'
                                            else:
                                                previous_trust = item

                                for item in role_annotation:
                                    if 'experiencer' in item:
                                        role_item_buffer.append('experiencer')
                                        if '[' not in item:
                                            experiencer = 'B-experiencer'
                                        elif Counter(role_item_buffer)['experiencer'] <= 1:
                                            experiencer = 'B-experiencer'
                                            if item == previous_experiencer:
                                                experiencer = 'I-experiencer'
                                            else:
                                                previous_experiencer = item


                                    if 'target' in item:
                                        role_item_buffer.append('target')
                                        if '[' not in item:
                                            target = 'B-target'
                                        elif Counter(role_item_buffer)['target'] <= 1:
                                            target = 'B-target'
                                            if item == previous_target:
                                                target = 'I-target'
                                            else:
                                                previous_target = item

                                    if 'cause' in item:
                                        role_item_buffer.append('cause')
                                        if '[' not in item:
                                            cause = 'B-cause'
                                        elif Counter(role_item_buffer)['cause'] <= 1:
                                            cause = 'B-cause'
                                            if item == previous_cause:
                                                cause = 'I-cause'
                                            else:
                                                previous_cause = item

                                multilayer_annotation = (token, anger, anticipation, disgust, fear, joy, other, sadness, surprise, trust, experiencer, target, cause)
                                BIO_sentence.append(multilayer_annotation)
                                if BIO_sentence not in BIO_annotation:
                                    i += 1
                                    BIO_annotation.append(BIO_sentence)
                                    datarow_token_level = {"sent_num": str(i),
                                                              "BIO": BIO_sentence}
                                    token_level_annotation.append(datarow_token_level)


            json.dump(sentence_level_annotation, output_1, indent=4)
            json.dump(token_level_annotation, output_2, indent=4)
            return BIO_annotation

        else:
            print("Not a TSV file")
    else:
        print('Intended file does not exist!')

def merg_json_file():
    input = "Input"
    json_file_name_annotation_all = "annotation_all.json"
    json_file_path_annotation_all = join(input, json_file_name_annotation_all)

    if exists(json_file_path_annotation_all):
        print('\'%s\' file already exists' % split(json_file_path_annotation_all)[-1])
    else:
        json_file_sentence_level = open('Input/sentence_level_annotation.json', 'r')
        sentence_level_annotation = json.load(json_file_sentence_level)

        output = open(json_file_path_annotation_all, 'w')

        annotation_all = []
        json_file_token_level = open('Input/token_level_annotation.json', 'r')
        token_level_annotation = json.load(json_file_token_level)
        for token_level, sentence_level in zip(token_level_annotation, sentence_level_annotation):
            new_data_row = sentence_level
            new_data_row.__setitem__("tokens", [i[0] for i in token_level['BIO']])
            annotation_all.append(new_data_row)
        json.dump(annotation_all, output, indent=4)


if __name__ =="__main__":
    Input_dir = 'Input'
    read_from_DB(Input_dir, "tweet.db", "train_raw.txt")
    # merg_json_file()


