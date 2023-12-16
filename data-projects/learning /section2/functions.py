def highest_even(list):
    even_num = []
    for item in list:
        if item % 2 == 0:
            even_num.append(item)
    return max(even_num)

print(highest_even([1,2,3,4,5]))
