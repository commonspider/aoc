with open("input") as f:
    data = f.read()

ranges = map(lambda r: r.split("-"), data.split(","))

lengths = {
    1: [],
    2: [1],
    3: [1],
    4: [1, 2],
    5: [1],
    6: [1, 2, 3],
    7: [1],
    8: [1, 2, 4],
    9: [1, 3],
    10: [1, 2, 5]
}

password = 0

for start, end in ranges:
    start = int(start)
    end = int(end)
    for product_id in range(start, end + 1):
        product_id = str(product_id)
        for length in lengths[len(product_id)]:
            pattern = int(product_id[:length])
            for i in range(length, len(product_id), length):
                if pattern != int(product_id[i:i + length]):
                    break
            else:
                password += int(product_id)
                break

print(password)
