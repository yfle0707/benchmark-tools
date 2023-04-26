import os
import sys
import datetime
import subprocess
import re
import time

def measure_tput(ifname):
    cmd = 'ethtool -S '+ifname+' | grep '
    for i in ['tx_bytes_phy', 'rx_bytes_phy']:
        cmd +=' -e '+ i
#    print(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
#    print("program output:", out)
    
    lines  = out.decode('utf-8').replace(':','\n').split('\n')
#    print(lines)
    return int(lines[1].rstrip()), int(lines[3].rstrip())

def main(ifname):
    (prev_tx_bytes, prev_rx_bytes) = measure_tput(ifname)
    prev = datetime.datetime.now().timestamp()
    while True:
        (tx_bytes, rx_bytes) = measure_tput(ifname)
        now = datetime.datetime.now().timestamp()
        time_diff = now - prev;
        tx_diff = tx_bytes - prev_tx_bytes;
        rx_diff = rx_bytes - prev_rx_bytes;
        #print('time_diff {}, tx_diff {}, rx_diff {}'.format(time_diff, tx_diff, rx_diff))
        print('time_diff {:.2f} s, tx_tput {:.2f} MB/s, rx_tput {:.2f} MB/s'.format(time_diff, (tx_diff/1000000)/time_diff, (rx_diff/1000000)/time_diff))
        prev_tx_bytes = tx_bytes
        prev_rx_bytes = rx_bytes
        prev = now
        time.sleep(1)        

if __name__ == "__main__":
    main(sys.argv[1])
