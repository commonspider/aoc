with open("input") as f:
    data = f.read()

ranges = map(lambda r: r.split("-"), data.split(","))

password = 0

for start, end in ranges:
    start = int(start)
    end = int(end)
    for product_id in range(start, end + 1):
        product_id = str(product_id)
        middle, rest = divmod(len(product_id), 2)
        if rest == 1:
            continue
        first = int(product_id[:middle])
        second = int(product_id[middle:])
        if first == second:
            password += int(product_id)

print(password)
