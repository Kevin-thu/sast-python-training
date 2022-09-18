import argparse
from pathlib import Path

def parse_data():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a','--add',
        dest="add_words",
        type=str,
        default=None,
        help="add the given words to the word list"
    )
    parser.add_argument(
        '-r','--remove',
        dest="removed_words",
        type=str,
        default=None,
        help="remove the word group containing the given word from the word list"
    )
    args = parser.parse_args()
    return args.add_words, args.removed_words

def add(add_words: str):
    '''
    Add given words to the word list.
    '''
    with open(Path.cwd() / "collection.txt", "a") as f:
        f.write(add_words + '\n\n')

def remove(removed_words: str):
    '''
    Remove the word group containing the given word from the word list.
    '''
    with open(Path.cwd() / "collection.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()] # 清除列表中空行字符
    with open(Path.cwd() / "collection.txt", "w") as f:
        for line in lines:
            if removed_words not in line:
                f.write(line + '\n\n')

if __name__ == "__main__":
    add_words, removed_words = parse_data()
    if add_words is not None:
        add(add_words)
    if removed_words is not None:
        remove(removed_words)