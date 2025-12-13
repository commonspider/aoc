with open("input") as f:
    lines = f.readlines()

pointer = 50
password = 0

for line in lines:
    if len(line) < 2:
        continue
    direction = line[0]
    steps = int(line[1:])
    if direction == "R":
        sign = 1
    elif direction == "L":
        sign = -1
    else:
        raise Exception
    delta = sign * steps
    pointer = (pointer + delta) % 100
    if pointer == 0:
        password += 1

print(password)
