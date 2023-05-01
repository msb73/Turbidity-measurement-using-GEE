dic = {
    'abc' :123,
    'def' : 456,
    'ghi' :789
}

new_dic = {i[:1]: j for i, j in dic.items()}
print(new_dic)