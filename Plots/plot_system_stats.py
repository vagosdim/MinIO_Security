# Usage: python3 plot_system_stats.py golang_encryption.csv sse_encryption.csv
import numpy as np
import csv
import sys
import matplotlib.pyplot as plt

f0 = sys.argv[1]
f1 = sys.argv[2]

index = []
cpu = []
with open(f0, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for lines in csv_reader:
        index.append(lines[0])
        cpu.append(lines[1])

# Golang encryption speed Median
cpu_golang = [float(cpu[i]) for i in range(1, len(cpu))]

cpu = []
with open(f1, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for lines in csv_reader:
        cpu.append(lines[1])

# SSE-C  MinIO encryption speed Median
cpu_minio = [float(cpu[i]) for i in range(1, len(cpu))]

# data to plot
index = index[1:]


# create plot
fig, ax = plt.subplots()
bar_width = 0.35
opacity = 0.9


rects1 = plt.plot(index, cpu_golang,
alpha=opacity,
color='b',
marker="^",
label='Golang C-shared Library')

rects2 = plt.plot(index, cpu_minio,
alpha=opacity,
color='r',
marker="o",
label='MinIO SSE-C')

plt.xlabel('Input File Size', weight='bold')
plt.ylabel('Re-Encryption Time (Second)', weight='bold')
plt.title('Golang Encryption vs MinIO SSE-C Key Rotation', weight='bold')
#plt.yticks(index + bar_width/2, ('10M Writes', '10M Reads', '10M Overwrites'), weight='bold')
plt.legend()

ax.yaxis.grid(color='gray', linestyle='dashed')
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()