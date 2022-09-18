import argparse
from ast import parse
import os
import numpy as np
from pathlib import Path
from IPython import embed
import random
from pygtrans import Translate
from tqdm import tqdm

def parser_data():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r','--random',
        dest="rand",
        action="store_true",
        help="input -r to randomly shuffle the word list"
    )
    parser.add_argument(
        '-s','--start',
        dest="start",
        type=int,
        default=0,
        help="the starting position in the word list"
    )
    parser.add_argument(
        '-l','--length',
        dest="length",
        type=int,
        default=30,
        help="the length of the wordbook"
    )
    parser.add_argument(
        '-n','--num',
        dest="num",
        type=int,
        default=1,
        help="the number of wordbooks you want to generate\n(note: useful only while you input -r in the meantime)"
    )
    args = parser.parse_args()
    return args.rand, args.start, args.length, args.num

def words_generator(rand: bool, start: int, length: int, index: int):
    '''
    Generate the wordbook.
    rand(bool): whether to randomly shuffle the word list
    start(int): the starting position
    length(int): the length of the wordbook
    index(int): wordbook index
    '''
    root_path = Path.cwd()
    words_path = root_path / "collection.txt"
    trans_path = root_path / "trans_dict.npy"
    store_path = root_path / "WordBook"
    if not os.path.exists(store_path):
        os.mkdir(store_path)
    
    try:
        with open(words_path, "r") as f:
            words = f.read().strip().split('\n\n')  # f.read()读取文件内容
        if os.path.exists(trans_path):
            trans_dict = np.load(trans_path, allow_pickle=True).item() # item()方法脱去numpy对象的包装返回原生的dict
            # print(trans_dict)
        else:
            trans_dict = {}
        translator = Translate(proxies={'https': 'http://localhost:7890'})
        
        if rand:
            print("Randomly shuffle the word list")
            random.shuffle(words) # random.shuffle()混序排列

        if(start < 0): # 支持负号下标
            start = len(words) + start
        assert start >= 0 and start < len(words) and length >= 0
        if start + length > len(words):
            words = words[start:]
        else:
            words = words[start:start+length]
        
        with open(store_path / f"untraslated_{index}.txt", "w", encoding='utf8') as f: # 必须指明encoding='utf8'，否则中文可能出现乱码
            for i, word_group in enumerate(words):
                f.write(f"□ 第 {i+1} 组单词：")
                word_group = word_group.split(',')
                for word in word_group:
                    f.write(f"{word.strip()}  ")
                f.write('\n')
            print("Original wordbook generated succesfully :)")
        
        with open(store_path / f"traslated_{index}.txt", "w", encoding='utf8') as f:
            for i, word_group in tqdm(enumerate(words)):
                f.write(f"□ 第 {i+1} 组单词：")
                word_group = word_group.split(',')
                for word in word_group:
                    word = word.strip()
                    try:
                        if word in trans_dict: # 如果字典中有该单词，直接调用即可，无须联网翻译
                            trans_text = trans_dict[word]
                        else:
                            trans_text = translator.translate(word).translatedText
                            trans_dict[word] = trans_text
                        f.write(f"{word}-{trans_text}  ")
                    except:
                        print("Translation failed :(")
                        raise Exception("Trainlation failed")
                f.write('\n')
            print("Traslated successfully :)")
            np.save(trans_path, trans_dict) # 更新字典，存入trans_dict.npy文件中
        
    except Exception as e:
        embed(header=str(e))

if __name__ == "__main__":
    rand, start, length, num = parser_data()
    for i in range(num):
        words_generator(rand, start, length, i+1)