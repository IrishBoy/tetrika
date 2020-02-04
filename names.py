with open("names.txt", "r") as file_names:
    names = file_names.read().replace('\n', '').split(',')
    names.sort()
    print(sum(list((sum(list(ord(k.lower()) - 96 for k in name.replace('"', ''))) * (idx + 1)) for idx, name in enumerate(names))))
# 871853874