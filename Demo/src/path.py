'''
Created on 21-Jul-2014

@author: nikita

'''
import subprocess
import psutil
import shlex
import sys


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

def main():
    
    pid = retrieve_process_id()
    cron_p = psutil.Process(int(pid))
    
    print "cron : ", cron_p.get_children()
    
    cron_children_pid = []
    
    for proc in cron_p.children():
        cron_children_pid.append(proc.pid)
        
    print cron_children_pid
    
    for child_process in cron_children_pid:
        cron_process =  psutil.Process(int(child_process))
        for cron_child in cron_process.children():
            cron_child_process = psutil.Process(int(cron_child.pid))
            print cron_child_process
            for cron_pid in cron_child_process.children():
                processes = psutil.Process(int(cron_pid.pid))
                print "child : " ,processes

if __name__ == '__main__':
    res = main()
    sys.exit(res)

