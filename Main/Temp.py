
inputFile = '0 Helpdesk.txt'
count = 0
countMax7 = 0
with open(inputFile, encoding='utf8') as f:
    for line in f:
        count += 1
        if count > 2:
            trace = line.strip().split('!@#')
            if len(trace) >= 7 and count >= 0.7*4580:
                countMax7 += 1
                print(trace[6:])

print('total trace: %d, traceLeng>7: %d' % (count-2, countMax7))
print('done!')