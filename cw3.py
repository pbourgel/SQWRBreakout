twos_memo = {1:1}  
threes_memo = {1:1}   
twothrees_memo = {1:1}
fives_memo = {1:1}
threefives_memo = {1:1}

def twos(k):   
    if not k in twos_memo.keys():
        twos_memo[k] = 2 * twos(k-1)
    else:
        print twos_memo[k]
        return twos_memo[k]

def twothrees(k):
    if not k in twothrees_memo:
        twothrees_memo[k] = (2*3) * twothrees(k-1)
    else:
        return twothrees_memo[k]


def threes(k):
    if not k in threes_memo:    
        threes_memo[k] = 3 * threes(k-1)
    else:
        return threes_memo[k]

    
def merge():
    lst = [1]
    i = 2
    for num2,num23,num3 in twos_memo, threes_memo, twothrees_memo:
        if num2 == min(num2,num23,num3):
            lst.append(num2)
        if num23 == min(num2,num23,num3):
            lst.append(num23)
        else:
            lst.append(num3)
    return lst

def hamming(n):
    if n == 1: return 1
    else:
        twos(n)
        threes(n)
        twothrees(n)
        hammings = merge()
        return hammings

print hamming(5)
