with open('links.txt') as f:
    final_list = f.read().splitlines()

print len(set(final_list)), len(final_list)