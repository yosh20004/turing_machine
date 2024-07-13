stack = []


def push(val):
    stack.append(val)


def pop():
    try:
        return stack.pop()
    except:
        print("Stack is empty")


def reset():
    global stack
    stack = []
    print("Stack is reset")








