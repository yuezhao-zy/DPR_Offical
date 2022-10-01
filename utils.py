import glob
import re
import json
import os
import jieba
import re
import logging
import sys


def ini_logger():
    import logging
    import sys
    # 设置输出格式
    if os.environ.get('LOG_PATH') is not None:

        logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO, handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(os.environ['LOG_PATH'])
            ]
                            )

    else:
        logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO, handlers=[
                logging.StreamHandler(sys.stdout),
            ]
                            )

    # 设置日志打印级别
    # 设置日志输出器的名字，可以在项目中配置多个不同的日志输出器

    logger = logging.getLogger(__name__)



    return logger

logger = ini_logger()

def pprint_dict(dict):
    return json.dumps(dict,indent=4,ensure_ascii=False)


def save_file(ret,save_file_path,file_type='json',version_control=False):

    make_dir(save_file_path)

    if version_control:
        save_file_name = save_file_path[:save_file_path.rfind('.')]
        suffix = save_file_path[save_file_path.rfind('.')+1:]
        files = sorted(glob.glob(f'{save_file_name}_v*.{suffix}'))
        version = len(files)+1
        save_file_path = f'{save_file_name}_v{version}.{suffix}'

    with open(save_file_path,'w',encoding='utf-8') as save_file:
        logger.info('Write {} lines to {}'.format(len(ret),save_file_path))
        if(file_type == 'json'):
            save_file.write(json.dumps(ret,indent=4,ensure_ascii=False))
        elif (file_type == 'jsonl'):
            save_file.write('\n'.join(json.dumps(l,ensure_ascii=False) for l in ret))
        elif(file_type == 'txt'):
            save_file.write('\n'.join(ret))
        else:
            raise NotImplementedError()


def load_file(file_path,file_type='json',version_control=False):

    if version_control:
        save_file_name = file_path[:file_path.rfind('.')]
        suffix = file_path[file_path.rfind('.') + 1:]
        files = sorted(glob.glob(f'{save_file_name}_v*.{suffix}'))
        version = len(files)
        file_path = files[-1]
        # file_path = f'{save_file_name}_v{version}.{suffix}'
        # print(file_path)

    ret = []

    with open(file_path,encoding='utf-8') as file:
        if (file_type == 'json'):
            ret = json.load(file)
        elif file_type == 'jsonl':
            ret = [json.loads(l)  for l in file]
        elif(file_type == 'txt'):
            for line in file:
                ret.append(line.strip())
        else:
            raise NotImplementedError()
    logger.info('Loading {} lines from {}'.format(len(ret),file_path))


    return ret

def is_child_seq(s_child,s_parent,code=0):

    assert code != 0,('is_child_seq 修改！','mention:',s_child,'parent:',s_parent)
    all_in = True
    start_index = 0
    s_child_tokenized = list(jieba.cut(s_child))
    for w in s_child_tokenized:
        if w not in s_parent[start_index:]:
            all_in = False
            break
        else:
            start_index = s_parent.find(w,start_index)

    return all_in

def find_parent_seq(s_child,s_parent):

    start_index = 0
    s_child_tokenized = list(jieba.cut(s_child))
    begin,end = None,None
    ret = []
    while True:
        # print(s_child,s_parent[start_index:])
        # print(start_index)
        all_in = True
        begin, end = None, None
        for w in s_child_tokenized:
            if w not in s_parent[start_index:]:
                all_in = False
                break
            else:
                start_index = s_parent.find(w, start_index)
                if begin is None:
                    begin = start_index
                end = start_index + len(w)
        if all_in:
            start_index = end
            if re.search('[，。,\.\?？！!]',s_parent[begin:end]) is None:
                ret.append((begin,end))
        else:
            break
    return ret if len(ret) != 0 else None


def is_sub_interval(i1, i2):
    '''
    :param i1: interval
    :param i2: interval
    :return: i1 in i2
    '''

    return i1[0] >= i2[0] and i1[1] <= i2[1]

def is_in_interval(i1, i2):
    '''
    :param i1: point
    :param i2: interval
    :return: point i1 in interval i2
    '''
    return i1 >= i2[0] and i1 <= i2[1]

def drop_duplicate(ret,drop_subseq=True):
    d_ret = []

    ret = sorted(ret, key=lambda i: len(i), reverse=True)
    for i in range(len(ret)):
        exist_ = False
        for j in range(i):
            if drop_subseq:
                if ret[i] in ret[j]:
                    exist_ = True
                    break
            else:
                if ret[i] == ret[j]:
                    exist_ = True
                    break

        if not exist_:
            d_ret.append(ret[i])

    return d_ret

def clean_answer(answer:str)->str:
    score_p = '[（][^（）]*\d+[^（）]*分[^）]*[）]'
    blank_p = '[ \n]'
    patterns = [score_p]+[blank_p]
    for p in patterns:
        answer = re.sub(p,'',answer)

    return answer

def sort_order(rg):
    for i in range(len(rg)):
        rg[i] = int(rg[i])
    return [min(rg[0], rg[1]), max(rg[0], rg[1])]

def make_dir(path):
    dirpath = path
    if '/' in path:
        file = path[path.rfind('/')+1:]
        if '.' in file:
            dirpath = path[:path.rfind('/')]

    else:
        return

    if dirpath != '.':
        print('making dir:{}'.format(dirpath))
        os.makedirs(dirpath,exist_ok=True)

def flatten(l):
    ret = []
    for ll in l:
        if isinstance(ll,list):
            ret += flatten(ll)
        else:
            ret.append(ll)
    return ret


def split_dataset(file):
    file = load_file(file)
    train = file[:int(0.8*len(file))]
    test = file[int(0.8*len(file)):]
    return train,test


def get_toy_data(file,toy_nb=100):
    f = load_file(file)
    return f[:toy_nb]



if __name__ == '__main__':
    s = "英国西部主要为畜牧业。原因：西部海拔较高，西风挟带来自海洋的湿润气流遇地形抬升，降水较多，而热量不足，适合发展畜牧业。英国东部主要为种植业。原因：东部地区降水相对较少，且主要为平原，因而适合发展种植业。"
    ret = find_parent_seq('种植业',s)
    for _ in ret:
        print(s[_[0]:_[1]])
    print(ret)

