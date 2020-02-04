with open("hits.txt", "r") as fileHits:
    hits = fileHits.read().split()
    del hits[::3]
    del hits[1::2]
    print(*sorted(set(hits), key=hits.count, reverse=True)[:5], sep='\n')
