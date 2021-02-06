import numpy as np
import scipy.stats
import csv
import time

def mean_confidence_interval(data, confidence=0.95):
    
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    
    return m, m-h, m+h

def export_stats_to_csv(samples, input_file, output_file):

    m, m_l, m_u = mean_confidence_interval(samples)
    median = np.median(samples)

    with open(output_file, mode='a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([input_file, str(median), str(m_l), str(m), str(m_u)])


def export_system_stats(cpu_usage, ram_usage, input_file, output_file):

    with open(output_file, mode='a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([input_file, str(np.median(cpu_usage)), str(np.median(ram_usage))])