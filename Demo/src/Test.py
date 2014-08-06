'''
Created on 18-Jul-2014

@author: nikita
'''
import subprocess
import psutil
import shlex
import sys

search_string = "wait_proc"

def run_ps_cmd():
    try:
        proc1 = subprocess.Popen(shlex.split('ps aux'),stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(shlex.split('grep [c]ron'),stdin=proc1.stdout,
                                 stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
        proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
        out=proc2.communicate()[0]
        print('{0}'.format(out))
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
   
def main():
    pid = []
    pid.append(retrieve_process_id())
    
    child_process = get_child_process(pid)
    print child_process
    for proc in child_process:
        cron_task = psutil.Process(int(proc))
        print cron_task.cmdline()
   
if __name__ == '__main__':
    res = main()
    sys.exit(res)
       
