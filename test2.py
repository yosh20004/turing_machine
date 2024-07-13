import time
import dealwithtape

curr_list = []
curr_tar = None
state = 'trueStart'
input_tape = []
work_tape = []
output_tape = []
low = 0
high = 0
mid = 0
timesCount = 0




def update():
    global state, input_tape, work_tape, output_tape, low, high, mid, timesCount

    input_pointer = -1
    output_pointer = -1
    work_pointer = -1


    if (state == 'trueStart'):
        state = 'init low'

    elif (state == 'init low'):
        input_pointer = 0
        state = 'writeLow'

    elif (state == 'writeLow'):
        work_pointer = 0
        low = low
        work_tape.append(low)
        state = 'init high'

    elif (state == 'init high'):
        input_pointer = 1
        state = 'writeHigh'

    elif (state == 'writeHigh'):
        work_pointer = 1
        high = high
        work_tape.append(high)
        if len(work_tape) == 2:
            state = 'readK'
        else:
            state = 'compareLow'

    elif (state == 'readK'):
        input_pointer = 2
        state = 'compareLow'
        work_tape.append(curr_tar)

    elif (state == 'compareLow'):
        work_pointer = 0
        if low > high:
            logclass.Map.append((logclass.binary_search, curr_list, curr_tar, low, high))
            state = 'stop'
        else:
            state = 'calMid'

    elif (state == 'calMid'):
        work_pointer = 2
        mid = (low + high) // 2
        logclass.Map.append((logclass.binary_search, curr_list, curr_tar, low, high))
        # 叫web框架把栈更新一下
        work_tape[2] = mid
        state = 'readMid'

    elif (state == 'readMid'):
        input_pointer = mid + 3
        state = 'compareMid'
        
    elif (state == 'compareMid'):
        work_pointer = 2; input_pointer = mid + 3
        if curr_list[mid] == curr_tar:
            state = 'success'
        elif curr_list[mid] > curr_tar:
            state = 'updateHigh'
            high = mid - 1
        else:
            state = 'updateLow'
            low = mid + 1

    elif (state == 'updateHigh'):
        work_pointer = 1
        high = high
        work_tape[1] = high
        state = 'compareLow'

    elif (state == 'updateLow'):
        work_pointer = 0
        low = low
        work_tape[0] = low
        state = 'compareLow'

    elif (state == 'success'):
        output_pointer = 0
        output_tape.append(mid)
        state = 'trueEND'

    
    elif (state == 'stop'):
        output_pointer = 0
        output_tape.append(-1)
        state = 'trueEND'

    elif (state == 'trueEND'):
        output_pointer = 0
        timesCount -= 1
        pass

    elif (state == 'error'):
        print('what can i say')

    timesCount += 1
   
    data = {
        'state': state,
        'input_tape': input_tape,
        'work_tape': work_tape,
        'output_tape': output_tape,
        'times': timesCount,
        'grids': len(work_tape),
        'stack': dealwith_func_stack(),
        'input_pointer': input_pointer,
        'work_pointer': work_pointer,
        'output_pointer': output_pointer
    }

    return data


def popfunc(data):
    try:
        l = data['stack']
        if len(l) == 0:
            l.append(" ans = {}".format(output_tape[0]))
            print('im here')

        else:
            l.pop()
            _top = l.pop()
            _top += ' ans = {}'.format(output_tape[0])
            l.append(_top)

        print(l)
        data['stack'] = l
    except:
        ...

    return data







class logclass:

    Map = []

    ans = None

    @staticmethod
    def binary_search(l, x, low, high):
        if low > high:
            logclass.ans = -1
            return -1
        else:
            mid = (low + high) // 2
            if l[mid] == x:
                logclass.ans = mid
                return mid
            elif l[mid] > x:
                logclass.Map.append((logclass.binary_search, l, x, low, mid-1))
            else:
                logclass.Map.append((logclass.binary_search, l, x, mid+1, high))
    
            return None


def init(l, x):
    clear()
    global curr_list, curr_tar, input_tape, low, high, mid, state
    input_tape = dealwithtape.dealwith_input_tape(l,x)
    curr_list = l
    curr_tar = x
    low = 0
    high = len(curr_list) - 1
    logclass.Map = []
    logclass.ans = None
    # t = (logclass.binary_search, curr_list, x, 0, len(curr_list)-1)
    # logclass.Map.append(t)



def init_():
    global curr_list, curr_tar, input_tape, low, high, mid, state, timesCount, desk
    l = [0,1,2,3,4,6,7,8,9,10]
    # l = list(range(3, 1000))
    x = 5
    # curr_list = l
    # curr_tar = x
    clear()
    init(l, x)


def reset():
    clear()
    init(curr_list, curr_tar)




def clear():
    logclass.Map = []
    logclass.ans = None
    global state, input_tape, work_tape, output_tape, low, high, mid, timesCount, desk
    state = 'trueStart'
    input_tape = []
    work_tape = []
    output_tape = []
    low = 0
    high = 0
    mid = 0
    timesCount = 0
    data = {
        'state': state,
        'input_tape': input_tape,
        'work_tape': work_tape,
        'output_tape': output_tape,
        'times': timesCount,
        'grids': len(work_tape),
        'stack': dealwith_func_stack(),
        'input_pointer': -1,
        'work_pointer': -1,
        'output_pointer': -1
    }
    return data



def dealwith_func_stack():
    l = []
    for _ in logclass.Map:
        line = str(_[0].__name__) + " " + "left=" + str(_[3]) + " " + "right=" + str(_[4])
        l.append(line)

    print(l)

    # if logclass.ans != None:
    #     try:
    #         temp = l.pop()
    #     except:
    #         temp = ""

    #     temp = temp + " ans = " + str(logclass.ans)
    #     l.append(temp)

    return l






def bench():
    # init_()

    def run():
        while True:
            data = update()
            print(data)
            # time.sleep(0.2)
            print(timesCount)
            

            if data['state'] == 'trueEND':
                print(timesCount)
                break
    
    init_()
    run()
    # init_()
    # run()
    # init(list(range(3,1000)), 777)
    # run()

    



# bench()





