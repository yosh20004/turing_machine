from numpy import sort

def _select(w:list, v:list, cap:int, bestp:int, cw:int, cp:int, level:int):
    def Bound(level):
        bound = cp
        total_weight = cw 

        for i in range(level, len(w)):
            if total_weight + w[i] > cap:
                fraction = (cap - total_weight) / w[i]
                bound += v[i] * fraction
                break    # 当背包已满时，停止遍历
            else:
                bound += v[i]    # 如果背包还没有满，就取整个物品的价值
                total_weight += w[i]

        return bound

    if level >= len(v):
        return 0

    if Bound(level) < bestp:
        print(Bound(level))
        return 0
    else:
        print(Bound(level))

    ans = 0
    if cw + w[level] <= cap:
        buy = _select(w, v, cap, bestp, cw + w[level], cp + v[level], level + 1)
        dont_buy = _select(w, v, cap, bestp, cw, cp, level + 1)
        ans = max(buy + v[level], dont_buy)
    else:
        dont_buy = _select(w, v, cap, bestp, cw, cp, level + 1)
        ans = dont_buy

    bestp = max(bestp, ans)
    return ans
    


def select(l, cap):
    global cmp
    _l = sorted(l, key=lambda x: x[0] / x[1], reverse=False)

    l1 = []
    l2 = []
    for _ in _l:
        l1.append(_[0])
        l2.append(_[1])
    
    # print(_l, l1, l2)

    return _select(l1, l2, cap, 0, 0, 0, 0)


def sorttape(inputtape):
    len = inputtape[1]
    cap = inputtape[0]

    lw = inputtape[2::2]
    lv = inputtape[3::2]
    l = list(zip(lw, lv))

    _l = sorted(l, key=lambda x: x[0] / x[1], reverse=False)

    l = []
    for _ in _l:
        l.append(_[0])
        l.append(_[1])

    l.insert(0, cap)
    l.insert(1, len)
    
    return l


def Bound(level, cp, cw, v, w, cap, l=[]): # 可能有错 需注意

    bound = cp
    total_weight = cw 

    for i in range(level, len(w)):
        if total_weight + w[i] > cap:
            fraction = (cap - total_weight) / w[i]
            bound += v[i] * fraction
            break    # 当背包已满时，停止遍历

        else:
            bound += v[i]    # 如果背包还没有满，就取整个物品的价值
            total_weight += w[i]

    # print(level, cp, cw, cap, w, v, bound)

    return bound





def bench():
    # l = [(5, 12), (15, 30), (25, 44), (27, 46), (30, 50)]
    # print(select(l, 50))  # ok 92

    # l = [(2, 6), (3, 5), (5, 8), (2, 4)]
    # print(select(l, 5))  # ok 11

    # weights = [23, 31, 29, 44, 53, 38, 63, 85, 89, 82]
    # values  = [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]

    # # Combine weights and values into tuples
    # l = list(zip(weights, values))

    # print(select(l, 165))  # ok 309

    # print(sorttape([5,4,5,12,15,30,25,44,27,46]))

    ...

# bench()


    