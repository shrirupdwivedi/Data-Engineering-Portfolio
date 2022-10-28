# The folder where airflow should store its log files
from argparse import ArgumentDefaultsHelpFormatter
from pathlib import Path

base_log_folder = 'opt/airflow/logs/marketvol'

file_list = Path(base_log_folder).rglob('*.log')

def analyze_file(file):

    log_list =[]
    for line in file:
        if line.startswith('['):
            l = line.split()
            if l[2] == 'ERROR':
                log_list.append(line)
    
    return log_list
                #logm1 = l[0] + l[1] + l[2] + l[3]
                #logm2 = l[4:]
                #log = " ".join(l)  

log_list =[]
for file in file_list:
    with open(file) as f:
        log_list = log_list.append(analyze_file(f))

c = len(log_list)
print(f'Total number of errors:{c}')
print(f'Here are all the errors: {log_list}')



            




