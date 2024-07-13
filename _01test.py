import _01packbag
import time

st_lv = None
st_lw = None
st_cap = None

bestp = None
bound = None
Times = 0


state = 'Wait'
inputtape = []
worktape = []
outputtape = []

input_pointer = -1
work_pointer = -1
output_pointer = -1


lv = []
lw = []
level = None

stack = []


def _update_pointers(_1, _2, _3):
    global input_pointer, work_pointer, output_pointer
    input_pointer = _1
    work_pointer = _2
    output_pointer = _3


# worktape = [cap, len, level(变), bestp(), cw(变), cp(变)]

def update():
    global state, inputtape, worktape, outputtape, lv, lw, level, bound, Times, input_pointer, work_pointer, output_pointer, stack

    if state == 'Wait':
        _update_pointers(0, -1, -1)
        state = 'initCap'

    elif state == 'initCap':
        _update_pointers(-1, 0, -1)
        worktape.append(inputtape[0])
        state = 'writeCap'

    elif state == 'writeCap':
        _update_pointers(1, -1, -1)
        state = 'initNum'

    elif state == 'initNum':
        worktape.append(inputtape[1])
        _update_pointers(-1, 1, -1)
        state = 'writeNum'

    elif state == 'writeNum':
        _update_pointers(2, -1, -1)
        state = 'sort'

    elif state == 'sort':
        inputtape = _01packbag.sorttape(inputtape)
        lw = inputtape[2::2]
        lv = inputtape[3::2] # 这里修改了lw lv
        # 这里直接改输入纸带了
        _update_pointers(-1, 2, -1)
        worktape.append(0)
        state = 'initLevel'

    elif state == 'initLevel':
        _update_pointers(-1, 3, -1)
        worktape.append(0)
        state = 'initBestp'

    elif state == 'initBestp':
        _update_pointers(-1, 4, -1)
        worktape.append(0)
        state = 'initCw'

    elif state == 'initCw':
        _update_pointers(-1, 5, -1)
        worktape.append(0)
        state = 'initCp'

    elif state == 'initCp':
        _update_pointers(-1, -1, 0)
        for _ in range(inputtape[1]):
            outputtape.append(0)
        state = 'initOutput'

    elif state == 'initOutput':
        _update_pointers(-1, 6, -1)
        for _ in range(inputtape[1]):
            worktape.append(0)
        state = 'initTemp'

    elif state == 'initTemp':
        _update_pointers(level * 2 + 2, -1, -1)
        state = 'choose'

    elif state == 'choose':
        _update_pointers(level * 2 + 2, 2, -1)
        state = 'cmpLevel'

    elif state == 'cmpLevel':
        _level = worktape[2]
        if _level >= inputtape[1]:
            global bestp
            bestp = worktape[5] # (bestp = cp)
            _update_pointers(-1, 3, 0)
            state = 'updateBestp'

        else:
            _update_pointers(level * 2 + 2, 2, -1)
            state = 'calBound'

    elif state == 'updateBestp':
        if bestp > worktape[3]: # 比当前最优解大
            worktape[3] = bestp
            _update_pointers(-1, 2, 0)
            state = 'goBack'
            for _ in range(len(outputtape)):
                outputtape[_] = worktape[6 + _]


        else: # 比当前最优解小
            _update_pointers(-1, 2, -1)
            state  = 'goBack'
            # 弹栈函数

    elif state == 'calBound':
        bound = _01packbag.Bound(worktape[2], worktape[5], inputtape[4], lv, lw, inputtape[0])
        # 计算上界函数
        _update_pointers(-1, 3, -1)
        state = 'cmpBound'

    elif state == 'cmpBound':
        if bound > worktape[3]: # 比当前最优解大
            bound = None
            _update_pointers(-1, 2, -1)
            state = 'goDown'

        else: # 比当前最优解小
            _update_pointers(-1, 2, -1)
            state = 'goBack'

    elif state == 'goDown':
        bound = None
        _update_pointers(level * 2 + 2, 4, -1)
        state = 'may I buy this one?'

    elif state == 'may I buy this one?':
        level = worktape[2]
        if worktape[4] + lw[level] <= worktape[0]: # 能买
            str = "cw = {},  cp = {},  level = {}, choose = 'buy'".format( worktape[4], worktape[5], worktape[2])
            stack.append(str)
            _update_pointers(level * 2 + 2, -1, -1)
            state = 'buy'
        
        else:
            str = "cw = {},  cp = {},  level = {}, choose = 'dont buy'".format( worktape[4], worktape[5], worktape[2])
            stack.append(str)
            _update_pointers(level * 2 + 2, -1, -1)
            state = 'cannot buy'

    elif state == 'buy':
        worktape[5 + level + 1] = 1
        _update_pointers(-1, 4, -1)
        state = 'updateCw'

    elif state == 'updateCw':
        worktape[4] += lw[level]
        _update_pointers(-1, 5, -1)
        state = 'updateCp'

    elif state == 'updateCp':
        worktape[5] += lv[level]
        _update_pointers(-1, 2, -1)
        state = 'updateLevel'

    elif state == 'updateLevel':
        worktape[2] += 1
        level += 1
        _update_pointers(level * 2 + 2,-1, -1)
        state = 'choose'
 
    elif state == 'cannot buy':
        worktape[5 + level + 1] = 0
        _update_pointers(-1, 2, -1)
        state = 'updateLevel'
        

    elif state == 'goBack':
        if level == 0:
            _update_pointers(-1, -1, -1)
            state = 'end'
        else:
            while level > 0: # 应该退不到0吧 试一下 不确定
                if worktape[5 + level] == 1:
                    worktape[5 + level] = 0
                    worktape[4] -= lw[level - 1]
                    worktape[5] -= lv[level - 1]
                    level -= 1
                    worktape[2] -= 1
                    stack.pop()
                    stack.append("cw = {},  cp = {},  level = {}, choose = 'dont buy'".format( worktape[4], worktape[5], worktape[2]))
                    _update_pointers(-1, 2, -1)
                    state = 'updateLevel'
                    break


                elif worktape[5 + level] == 0:
                    level -= 1
                    worktape[2] -= 1
                    stack.pop()




    elif state == 'end':
        _update_pointers(-1, -1, -1)
        Times -= 1


    else:
        state = '进入未知领域'


    Times += 1


    data = {
        'state': state,
        'input_tape': inputtape,
        'work_tape': worktape,
        'output_tape': outputtape,
        'level': level,
        'bound': bound,
        'times': Times,
        'input_pointer': input_pointer,
        'work_pointer': work_pointer,
        'output_pointer': output_pointer,
        'stack': stack,
        'lw':lw,
        'lv':lv,
    }

    try:
        data['equal'] = level == worktape[2]
    except:
        ...

    return data



def bench():
    # init([92, 57, 49, 68, 60, 43, 67, 84, 87, 72], [23, 31, 29, 44, 53, 38, 63, 85, 89, 82], 165)
    # print(lv, lw, level, inputtape, worktape, outputtape)
    # while state != 'end':
    #     data = update()
    #     print(data)
    #     # time.sleep(0.007)

    # clear()

    # init( [20, 30, 65, 40, 60, 85, 25, 30, 55, 65, 75, 40, 50, 35, 10, 15, 20, 25, 30, 35], [3, 5, 20, 9, 6, 12, 4, 6, 8, 10, 5, 7, 3, 4, 2, 3, 4, 5, 6, 7], 100)
    # print(lv, lw, level, inputtape, worktape, outputtape)
    # while state != 'end':
    #     data = update()
    #     print(data)
    #     # time.sleep(0.007)

    # clear()
    init([825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902996, 1844992, 1049289, 1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261], [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684], 6404180)
    print(lv, lw, level, inputtape, worktape, outputtape)
    while state != 'end':
        data = update()
        #print(data)
        # time.sleep(0.007)

    data = update()
    print(data)


    # init()




def init(v, w, cap):
    global state, inputtape, worktape, outputtape, lv, lw, level, stack, st_lv, st_lw, st_cap
    stack = []
    state = 'Wait'
    inputtape = []
    worktape = []
    outputtape = []
    lv = v
    lw = w
    st_lv = v
    st_lw = w
    st_cap = cap
    level = 0

    inputtape.append(cap)
    inputtape.append(len(v))

    for _ in range(len(v)):
        inputtape.append(w[_])
        inputtape.append(v[_])




def clear():
    global state, inputtape, worktape, outputtape, lv, lw, level, Times, stack
    state = 'Wait'
    Times = 0
    inputtape = []
    worktape = []
    outputtape = []
    lv = []
    lw = []
    level = None
    stack = []

    data = {
        'state': state,
        'input_tape': [],
        'work_tape': [],
        'output_tape': [],
        'level': 0,
        'bound': 0,
        'times': 0,
        'input_pointer': -1,
        'work_pointer': -1,
        'output_pointer': -1,
        'stack':[]
    }

    return data
        

def reset():
    global state, inputtape, worktape, outputtape, lv, lw, level, Times, stack, st_lv, st_lw, st_cap
    state = 'Wait'
    Times = 0
    inputtape = []
    worktape = []
    outputtape = []
    lv = []
    lw = []
    level = None
    stack = []
    st_lv = None
    st_lw = None
    st_cap = None





def init_():
    if st_lv == None:
        # init([92, 57, 49, 68, 60, 43, 67, 84, 87, 72], [23, 31, 29, 44, 53, 38, 63, 85, 89, 82], 165)
        init([12,30,44,46,50], [5,15,25,27,30], 50)

    else:
        init(st_lv, st_lw, st_cap)

    # init([825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693, 1902996, 1844992, 1049289, 1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489, 577243, 466257, 369261], [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830, 610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684], 6404180)




# bench()


