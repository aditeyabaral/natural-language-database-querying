with open("ids.txt") as ids, open("category.txt") as cat:
    id_content = [int(i) for i in ids.read().strip().split("\n")]
    cat_content = [int(i) for i in cat.read().strip().split("\n")]
    actual_cat = []
    for i in range(72):
        if i in id_content:
            actual_cat.append(cat_content[i])


with open("category.txt","w") as wr:
    for i in actual_cat:
        wr.write(str(i)+'\n')
