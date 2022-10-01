# from transformers import BertModel,BertTokenizer
# model = BertModel.from_pretrained('Luyu/co-condenser-wiki')
# tokenizer = BertTokenizer.from_pretrained('Luyu/co-condenser-wiki')


def get_auc(labels, preds):
    assert len(labels) == len(preds)
    # 这段代码基本上是沿着公式计算的：
    # 1. 先求正样本的rank和
    # 2. 再减去（m*(m+1)/2）
    # 3. 最后除以组合个数

    # 但是要特别注意，需要对预测值pred相等的情况进行了一些处理。
    # 对于这些预测值相等的样本，它们对应的rank是要取平均的

    # 先将data按照pred进行排序
    sorted_data = sorted(list(zip(labels, preds)), key=lambda item: item[1])
    print(sorted_data)
    pos = 0.0  # 正样本个数
    neg = 0.0  # 负样本个数
    auc = 0.0
    # 注意这里的一个边界值，在初始时我们将last_pre记为第一个数，那么遍历到第一个数时只会count++
    # 而不会立刻向结果中累加（因为此时count==0，根本没有东西可以累加）
    last_pre = sorted_data[0][1]
    count = 0.0
    pre_sum = 0.0  # 当前位置之前的预测值相等的rank之和，rank是从1开始的，所以在下面的代码中就是i+1
    pos_count = 0.0  # 记录预测值相等的样本中标签是正的样本的个数
    # 为了处理这些预测值相等的样本，我们这里采用了一种lazy计算的策略：
    # 当预测值相等时仅仅累加count，直到下次遇到一个不相等的值时，再将他们一起计入结果
    for i, (label, pred) in enumerate(sorted_data):
        # 注意：rank就是i+1
        if label > 0:
            pos += 1
        else:
            neg += 1
        if last_pre != pred:  # 当前的预测概率值与前一个值不相同
            # lazy累加策略被触发，求平均并计入结果，各个累积状态置为初始态
            auc += pos_count * pre_sum / count  # 注意这里只有正样本的部分才会被累积进结果
            print(pos_count * pre_sum / count,pos_count,pre_sum,count)
            count = 1
            pre_sum = i + 1  # 累积rank被清空，更新为当前数rank
            last_pre = pred
            if label > 0:
                pos_count = 1  # 如果当前样本是正样本 ，则置为1
            else:
                pos_count = 0  # 反之置为0
        # 如果预测值是与前一个数相同的，进入累积状态
        else:
            pre_sum += i + 1  # rank被逐渐累积
            count += 1  # 计数器也被累计
            if label > 0:  # 这里要另外记录正样本数，因为负样本在计算平均
                pos_count += 1  # rank的时候会被计入，但不会被计入rank和的结果

            # 注意这里退出循环后我们要额外累加一下。
    # 这是因为我们上面lazy的累加策略，导致最后一组数据没有累加
    auc += pos_count * pre_sum / count

    print(pos_count * pre_sum / count,pos_count, pre_sum , count)
    print(auc)
    print(pos)
    auc -= pos * (pos + 1) / 2  # 减去正样本在正样本之前的情况即公式里的(m+1)m/2
    print(auc)
    auc = auc / (pos * neg)  # 除以总的组合数即公式里的m*n
    return auc

v = get_auc([1,0,0,1,0],[0.8,0.5,0.4,0.4,0.2])
print(v)