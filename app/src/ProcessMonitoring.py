'''
Created on 30-Jul-2014

@author: nikita
'''
import subprocess
import json
import psutil
import shlex
import sys
import datetime
from time import sleep
from DataSender import send_process_information

search_string = "wait_proc"
cpu = []
memory = []
start_time = []
process_Status = []
process_name = []
process_command = []
json_list = {}

def run_ps_cmd():
    try:
        proc1 = subprocess.Popen(shlex.split('ps aux'),stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(shlex.split('grep [c]ron'),stdin=proc1.stdout,
                                 stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
        out=proc2.communicate()[0]
        #print('{0}'.format(out))
        return out
    except Exception, e:
        print >>sys.stderr, "Execution failed:", e
        return None

def retrieve_process_id():
    out = run_ps_cmd()

    for line in out.splitlines():
        fields = line.split()
        pid = fields[1]
    
    return pid

def get_child_process(child):
    cron_children_pid = []
    
    for child_process in child:
        cron_p = psutil.Process(int(child_process))
        cmdline = cron_p.cmdline()   
        
        proc_child = cron_p.children()
        if proc_child:
            for proc in proc_child:
                cron_children_pid.append(proc.pid)
    flag = check_string(cmdline) 
    if flag:
        return cron_children_pid
    else:
        return get_child_process(cron_children_pid)
                
def check_string(cmdline):
    for index in cmdline:
        if search_string in index:
            return True
   
def process_information(child_process_pid):
    for proc in child_process_pid:
        cron_task = psutil.Process(int(proc))
        cpu.append(cron_task.cpu_percent())
        memory.append( ("%.2f" %cron_task.get_memory_percent()))
        start_time.append(datetime.datetime.fromtimestamp(cron_task.create_time()).strftime("%Y-%m-%d %H:%M:%S"))
        process_Status.append(cron_task.status()) 
        process_name.append(cron_task.name())
        process_command.append(cron_task.cmdline()[1])
                        
def format_process_information(child_process_pid):  
    
    j_list = {}
    for index in range(len(child_process_pid)):
        process_info = {}
        process_info['process_id']= child_process_pid[index]
        process_info['cpu_usage']= cpu[index]
        process_info['memory_usage']= memory[index]
        process_info['start_time']= start_time[index]
        process_info['process_Status']= process_Status[index]
        process_info['process_name']= process_name[index]
        process_info['process_command']= process_command[index]
        
        j_list[child_process_pid[index]] = json.dumps(process_info, separators=(',',':'),sort_keys=True)
        
    return j_list

def main():
    while 1:
        
        pid = []
        pid.append(retrieve_process_id())
        
        child_process_pid = get_child_process(pid)
        
        process_information(child_process_pid)   
        json_list['Processes'] = format_process_information(child_process_pid)
        
        send_process_information(json_list)
        
        sleep(120)
        
if __name__ == '__main__':
    res = main()
    sys.exit(res)
