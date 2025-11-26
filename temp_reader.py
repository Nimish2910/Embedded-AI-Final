f = open("clean_temp.txt", "r")

total = 0
count = 0

for line in f:
    value = int(line.strip())
    total += value
    count += 1

avg = total / count
print("Average Temp:", avg)

f.close()

