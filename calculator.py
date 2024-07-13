
def solve(ans):
    if(len(ans) == 0): return 
    num_count = 0
    s = []
    i = 0
    while i < len(ans):

        if((ans[i] >= "0" and ans[i] <= "9") or (ans[i] == ".")):
            numtmp = ""
            while (i < len(ans)) and ((ans[i] >= "0" and ans[i] <= "9") or (ans[i] == ".")):
                numtmp += ans[i]
                i += 1
            i-=1
            s.append(numtmp)
            num_count += 1

        elif (ans[i] == " "): 
            i += 1
            continue

        elif (ans[i] == "+"):
            if(num_count < 2):
                return "NAN"
            tmp1 = s.pop()
            tmp2 = s.pop()
            s.append(str(float(tmp1) + float(tmp2)))

        elif (ans[i] == "*"):
            if(num_count < 2) :
                return "NAN"
            tmp1 = s.pop()
            tmp2 = s.pop()
            s.append(str(float(tmp1) * float(tmp2)))
            num_count -= 1;

        elif (ans[i] == "/"):
            if(num_count < 2) :
                return "NAN"
            tmp1 = s.pop()
            tmp2 = s.pop()
            if(float(tmp1) != 0):
                s.append(str(float(tmp2) / float(tmp1)))
                num_count -= 1
            else: return "NAN"

        elif(ans[i] == "-"):
            if(num_count < 2) :
                return "NAN"
            tmp1 = s.pop()
            tmp2 = s.pop()
            s.append(str(float(tmp2) - float(tmp1)))
            num_count -= 1

        elif(ans[i] == "%"):
            if(num_count < 2) :
                return "NAN"
            tmp1 = s.pop()
            tmp2 = s.pop()
            s.append(str(float(tmp2) % float(tmp1)))
            num_count -= 1


        elif(ans[i] == "^"):
            if(num_count < 2) :
                return "NAN"
            tmp1 = s.pop()
            tmp2 = s.pop()
            if "." in tmp1 or  "." in tmp2 :
                s.append(str(float(tmp2) ** float(tmp1)))
            else: s.append(int(tmp2) ** int(tmp1))
            num_count -= 1


        i += 1

    return s[-1]



def bench():
    l = "2 3 +"

    print(solve(l))


bench()