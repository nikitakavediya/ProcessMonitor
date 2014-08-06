

import psutil
import sys
from subprocess import Popen, PIPE

pid = []
cpu = []
memory = []
start_time = []
process_status = []

script_name = "sh /home/nikita/wait_proc.sh$"

def run_ps_cmd(script_name):
    try:
        p1 = Popen(["ps", "aux"], stdout=PIPE)
        p2 = Popen(["grep", script_name], stdin=p1.stdout, stdout=PIPE)
        output = p2.communicate()[0]
        return output
    except Exception, e:
        print >>sys.stderr, "Execution failed:", e
        return None
    
def process_information(script_name):
    output = run_ps_cmd(script_name)
    
    for line in output.splitlines():
        fields = line.split()
        pid.append(fields[1])
        cpu.append(fields[2])
        memory.append(fields[3])
        start_time.append(fields[8])
 
        for index in range(len(pid)):
            cron_p = psutil.Process(int(pid[index]))
            process_status.append(cron_p.status())
             
        
        
def main():
    
    process_information(script_name)
    print "pid : ", pid
    print "cpu : ", cpu
    print "memory : ", memory
    print "start_time : ", start_time
    print "process_status : ", process_status
    
    
if __name__ == '__main__':
    res = main()
    sys.exit(res)

