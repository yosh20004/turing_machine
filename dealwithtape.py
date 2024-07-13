import copy

def dealwith_input_tape(l, x):
    # 本函数用于处理自动机第一个纸带(输入纸带) 给他加上初始左界限 初始右界限 要找的数 三个元素
    # 如 [0,1,2,3,4,5,6,7,8,9,10],5 初始左界限为0 右界限为9 要找的数是5 因此变为
    # [0,9,5, ......]
    # 本函数返回一个新的列表

    _l = copy.deepcopy(l)
    length = len(_l)
    _l.insert(0, 0)
    _l.insert(1, length - 1)
    _l.insert(2, x)
    return _l







