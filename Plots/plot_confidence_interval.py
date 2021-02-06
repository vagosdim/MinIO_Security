# Usage: python3 plot_confidence_interval.py golang_encryption.csv sse_encryption.csv
import numpy as np
import csv
import sys
import seaborn as sns
import matplotlib.pyplot as plt

f0 = sys.argv[1]
f1 = sys.argv[2]

# Golang encryption speed Median
index = []
mean = []
m_l = []
m_h = []

with open(f0, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for lines in csv_reader:
        index.append(lines[0])
        m_l.append(lines[2])
        mean.append(lines[3])
        m_h.append(lines[4])
        
mean_golang = [float(mean[i]) for i in range(1, len(mean))]
ml_golang = [float(m_l[i]) for i in range(1, len(m_l))]
mh_golang = [float(m_h[i]) for i in range(1, len(m_h))]


# SSE-C  MinIO encryption speed Median
mean = []
m_l = []
m_h = []

with open(f1, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for lines in csv_reader:
        m_l.append(lines[2])
        mean.append(lines[3])
        m_h.append(lines[4])

mean_minio = np.array([float(mean[i]) for i in range(1, len(mean))])
ml_minio = np.array([float(m_l[i]) for i in range(1, len(m_l))])
mh_minio = np.array([float(m_h[i]) for i in range(1, len(m_h))])

# data to plot
index = index[1:]


# create plot
fig, ax = plt.subplots()
bar_width = 0.35
opacity = 0.9

ax = sns.lineplot(index, mean_minio, ci=95)
ax.fill_between(index, ml_minio, mean_minio, mh_minio, color='b', alpha=.2)
ax.yaxis.grid(color='gray', linestyle='dashed')
ax.set_axisbelow(True)

plt.tight_layout()
plt.legend()
plt.show()