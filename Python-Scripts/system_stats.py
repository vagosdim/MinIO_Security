# Execute python3 system_stats.py

# Import the required utilities
import psutil as ps
import time
from subprocess import PIPE

# define the command for the subprocess
cmd = ["python3", "sse_customer_file_upload.py", "/home/edimoulis//Master/Semester3/Security-of-Computer-Systems/Input/1KB.bin", "Keys/test_key.dat"]

# Create the process
process = ps.Popen(cmd, stdout=PIPE)

peak_mem = 0
peak_cpu = 0

# while the process is running calculate resource utilization.
while(process.is_running()):
    # set the sleep time to monitor at an interval of every second.
    #time.sleep(1)

    # capture the memory and cpu utilization at an instance
    mem = process.memory_info().rss/ (float)(2**30)
    cpu = process.cpu_percent()

    # track the peak utilization of the process
    if mem > peak_mem:
        peak_mem = mem
    if cpu > peak_cpu:
        peak_cpu = cpu

# Print the results to the monitor for each subprocess run.
print("Peak memory usage is: " + str(peak_mem) + " GB")
print("Peak CPU utilization is: " + str(peak_cpu)  + " %")