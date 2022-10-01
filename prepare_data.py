from utils import load_file,save_file
# for ds in ['nq','trivia']:
# for ds in ['webquestions']:
#     f = load_file(f'data/biencoder-{ds}-train.json')
#     ret = []
#     for l in f:
#         answer = '['+','.join([f'"{_}"' for _ in l['answers']]) + ']'
#         answer_list = eval(answer)
#         ret.append('\t'.join([l['question'],answer]))
#     save_file(ret,f'data/{ds}-train.tsv','txt')

from utils import load_file,save_file
# for ds in ['nq','trivia']:
# for ds in ['webquestions']:
# for ds in ['curatedtrec']:
for ds in ['squad1']:
    for cp in ['dev','train']:
        f = load_file(f'data/biencoder-{ds}-{cp}.json')
        ret = []
        cnt = 0
        for l in f:
            answer_text = "["
            for answer in l['answers']:
                if '"' in answer:
                    answer_text += "'" + answer + "'"+','
                else:
                    answer_text += '"' + answer + '"'+','
            answer_text += ']'
            try:
                answer_list = eval(fr'{answer_text}')
            except:
                print(l['answers'])
                print(answer_text)
                answer_text = '["answer"]'
                cnt += 1
            ret.append('\t'.join([l['question'],answer_text]))
        print(cnt)
        save_file(ret,f'data/{ds}-{cp}.tsv','txt')


# fmy = load_file('data/trivia-train.csv','txt')
# foff = load_file('downloads/data/retriever/qas/trivia-train.csv','txt')
# assert len(fmy) == len(foff),(len(fmy),len(foff))
# for lm,lo in zip(fmy,foff):
#     q1 = lm.split('\t')[0]
#     q2 = lo.split('\t')[0]
#     if(q1.strip() != q2.strip()):
#         print(q1)
#         print(q2)
#         print()


# f =load_file('outputs/2022-06-21/01-39-33/out/trivia/v1/test_pred.json')
# print(len(f[0]['ctxs']))
