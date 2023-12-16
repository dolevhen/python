some_list = ['a', 'b', 'c', 'b', 'd', 'm', 'n', 'n']
newlist = []
duplist = []
for item in some_list:
    if item not in newlist:
        newlist.append(item)
    else:
        duplist.append(item)
print(duplist)
