with open('requirements.txt') as f:
    data = f.readlines()
print(data)

print([i.split()[0] for i in data])

