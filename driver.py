import os
import virtual

def read_file():
    tasks=[]
    for path, dirs, files in os.walk('vm_snapshots'):
        for f in files:
            fin=open(path+'\\'+f, 'r')
            data=fin.read()
            tasks.append([f, data])
    return tasks

def get_params(str):
    name, ext=str.split('.')
    return [int(s) for s in name.split('_')[1:]]

def get_memory_accesses(str):
    accesses=str.split(' ')
    seq=[]
    for access in accesses:
        if access=='' : continue
        if len(access.split(','))!=2 : continue
        proc_id, address=access.split(',')
        seq.append((int(proc_id), int(address, 16)))
    return seq

if __name__=='__main__':
    tasks=read_file()

    for task in tasks:
        filename, seq=task
        file_no, np, VM_size, PM_size=get_params(filename)
        print('Simulating file', file_no, '...\n')
        seq=get_memory_accesses(seq)

        print('PM size =', PM_size, ' VM size=', VM_size, ' count of process=', np)
            
        fifo_faults=virtual.FIFO(VM_size, PM_size, np, seq)
        lru_faults=virtual.LRU(VM_size, PM_size, np, seq)
        lfu_faults=virtual.LFU(VM_size, PM_size, np, seq)
        opt_faults=virtual.OPTIMAL(VM_size, PM_size, np, seq)
        rnd_faults=virtual.Random(VM_size, PM_size, np, seq)

        for i in range(np):
            print('FIFO    PROCESS '+str(i)+'   '+str(fifo_faults[i]))
            print('LRU     PROCESS '+str(i)+'   '+str(lru_faults[i]))
            print('LFU     PROCESS '+str(i)+'   '+str(lfu_faults[i]))
            print('OPTIMAL PROCESS '+str(i)+'   '+str(opt_faults[i]))
            print('RANDOM  PROCESS '+str(i)+'   '+str(rnd_faults[i]))
            print('')
