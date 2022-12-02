
value = 13

result = ''

while value>0:
    remains = value % 2
    value = value // 2
    # Prepend the remainder
    result = str(remains) + result

print(result)