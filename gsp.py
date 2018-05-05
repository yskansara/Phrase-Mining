import itertools

# lines = []
# flag = True
# while flag:
#     try:
#         line = input().split()
#         lines.append(line)
#     except EOFError:
#         flag = False

lines = []
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        break

# Minimum Support
min_sup = int(lines[0][0])
del lines[0]
stop_words = ['a', 'an', 'are', 'as', 'by', 'be', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on',
              'that', 'the', 'to', 'was', 'were', 'will', 'with']
lines1 = []
for i in lines:
    temp = [j.lower() for j in i if j.lower() not in stop_words]
    lines1.append(temp)
lines_2 = []
for i in range(len(lines1)):
    l3 = []
    for j in range(len(lines1[i])):
        lines1[i][j] = lines1[i][j].replace(".", "")
        if j == len(lines1[i]) - 1:
            temp = lines1[i][j]
            l3.append(temp)
            break
        else:
            if lines1[i][j][-1] == ',':
                lines1[i][j] = lines1[i][j][:-1]
                for idx, val in enumerate(lines1[i]):
                    if lines1[i][idx] == 'and':
                        temp1 = lines1[i][j:idx] + [lines1[i][idx + 1]]
                        l2 = ','.join(str(v) for v in temp1)
                        temp = l2
                        l3.append(temp)
                        del lines1[i][j:idx + 2]
            if lines1[i][j + 1] == 'and':
                l2 = ','.join(lines1[i][j:j + 3:2])
                temp = l2
                l3.append(temp)
                del lines1[i][j + 1:j + 3]
            else:
                l3.append(lines1[i][j])
    lines_2.append(l3)

lines_3 = []
for i in lines_2:
    temp = []
    for j in i:
        k = j.split(',')
        if len(k) > 1:
            p = 0
            while p < len(k):
                if k[p] not in temp:
                    temp.append(k[p])
                p += 1
        elif j not in temp:
            temp.append(j)
    lines_3.append(temp)
unique_list = []
for i in lines_3:
    for j in i:
        if not [j] in unique_list:
            unique_list.append([j])
u_list = list(map(frozenset, unique_list))
D = list(map(set, lines_3))

# Check for infrequent subsets
def has_infrequent_subsets(Da, Ck, MinimumSupport):
    C = {}
    for i in Da:
        for j in Ck:
            if j.issubset(i):
                if j in C:
                    C[j] += 1
                else:
                    C[j] = 1
    prune_list = []
    sup = {}
    for item in C:
        if C[item] >= MinimumSupport:
            prune_list.append(item)
            sup[item] = C[item]
    return (sorted(prune_list), sup)


p_list, p_sup = has_infrequent_subsets(D, u_list, min_sup)
p = list(map(list, p_list))
product_table = [i[0] + i[1] for i in list(itertools.product(p, repeat=2))]

# Return pruned list
def calculate(datab, p_table):
    C = {}
    mult_list = {}
    for p in datab:
        for i in range(len(p)):
            for q in p_table:
                for j in range(len(q)):
                    if q[j] in p[i]:
                        k = i + 1
                        flag = False
                        for m in range(k, len(p)):
                            if j + 1 < len(q):
                                if q[j + 1] in p[m]:
                                    flag = True
                                    if tuple(q) in C:
                                        C[tuple(q)] += 1
                                    else:
                                        C[tuple(q)] = 1
                        if flag == False:
                            break
                            # k +=1
                    else:
                        flag = False
                        break

    prune_list = []
    sup = {}
    for item in C:
        if C[item] >= min_sup:
            prune_list.append(item)
            sup[item] = C[item]

    return ([[list(i), j] for i, j in C.items()], [list(i) for i in prune_list], sup)

# Return pruned list for  a phrase with more than two items
def calculate1(datab1, p_table1):
    C = {}
    for p in datab1:
        for q in p_table1:
            temp = [False] * len(q)
            for j in range(len(q)):
                if temp or j == 0:
                    temp_index = 0
                    for i in range(temp_index, len(p)):
                        if q[j] in p[i]:
                            temp[j] = True
                            temp_index = i + 1
            if all(temp) == True:
                if tuple(q) in C:
                    C[tuple(q)] += 1
                else:
                    C[tuple(q)] = 1
    prune_list = []
    sup = {}
    for item in C:
        if C[item] >= min_sup:
            prune_list.append(item)
            sup[item] = C[item]

    return ([[list(i), j] for i, j in C.items()], [list(i) for i in prune_list], sup)


C2, prune_list2, sup2 = calculate(lines_2, product_table)
first_list = [i[0] for i in prune_list2]
last_list = [i[1] for i in prune_list2]
new_list = []
for i in range(len(last_list)):
    for j in range(len(first_list)):
        if first_list[i] == last_list[j] and i != j:
            new_list.append(prune_list2[j] + [prune_list2[i][1]])
if len(new_list) != 0:
    C3, prune_list3, sup3 = calculate1(lines_2, new_list)
    lex_L = sorted(sorted([(j, (' '.join(i))) for i, j in sup3.items()], key=lambda x: x[1]), key=lambda x: x[0],
                   reverse=True)
    for i in lex_L:
        print(i[0], "[" + i[1] + "]")
else:
    lex_L = sorted(sorted([(j, (' '.join(i))) for i, j in sup2.items()], key=lambda x: x[1]), key=lambda x: x[0],
                   reverse=True)
    for i in lex_L:
        print(i[0], "[" + i[1] + "]")