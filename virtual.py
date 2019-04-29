import sys

def FIFO(VM_size, PM_size, np, memory_accesses):
    faults=[0 for i in range(np)]
    cached=[False for i in range(VM_size+1)]

    from collections import deque

    q=deque()
    for access in memory_accesses:
        proc_id=access[0]
        address=access[1]

        if cached[address]: continue

        elif len(q)==PM_size:
            victim=q.popleft()
            cached[victim]=False

        faults[proc_id]+=1
        cached[address]=True
        q.append(address)

    return faults
    out='FIFO    '
    for i in range(np): out+='  '+str(faults[i])
    print(out)

    return faults

def LRU(VM_size, PM_size, np, memory_accesses):
    faults=[0 for i in range(np)]
    cached=[False for i in range(VM_size+1)]
    last_time=[0 for i in range(VM_size+1)]
    mp={}

    for i in range(len(memory_accesses)):
        proc_id, address=memory_accesses[i]
        
        if cached[address]:
            del mp[(last_time[address], address)]
            last_time[address]=i
            mp[(i, address)]=1
            continue

        elif len(mp)==PM_size:
            victim=min(mp)
            del mp[victim]
            cached[victim[1]]=False

        faults[proc_id]+=1
        cached[address]=True
        last_time[address]=i
        mp[(i, address)]=1

    return faults
    out='LRU    '
    for i in range(np): out+='  '+str(faults[i])
    print(out)

    return faults

def LFU(VM_size, PM_size, np, memory_accesses):
    faults=[0 for i in range(np)]
    cached=[False for i in range(VM_size+1)]
    count=[0 for i in range(VM_size+1)]
    mp={}

    for access in memory_accesses:
        proc_id=access[0]
        address=access[1]
        count[address]+=1

        if cached[address]:
            del mp[(count[address]-1, address)]
            mp[(count[address], address)]=1
            continue

        elif len(mp)==PM_size:
            victim=min(mp)
            del mp[victim]
            cached[victim[1]]=False

        faults[proc_id]+=1
        cached[address]=True
        mp[(count[address], address)]=1

    return faults
    out='LFU    '
    for i in range(np): out+='  '+str(faults[i])
    print(out)

    return faults

def OPTIMAL(VM_size, PM_size, np, memory_accesses):
    faults=[0 for i in range(np)]
    cached=[False for i in range(VM_size+1)]
    mp={}
    nxt_time=[10**10 for i in range(len(memory_accesses))]
    last_time=[10**10 for i in range(len(memory_accesses))]
    
    for i in range(len(memory_accesses)-1, -1, -1):
        proc_id, address=memory_accesses[i]
        nxt_time[i]=last_time[address]
        last_time[address]=i

    for i in range(len(memory_accesses)):
        proc_id, address=memory_accesses[i]
        if cached[address]:
            del mp[(last_time[address], address)]
            last_time[address]=nxt_time[i]
            mp[(last_time[address], address)]=1
            continue

        elif len(mp)==PM_size:
            victim=max(mp)
            del mp[victim]
            cached[victim[1]]=False

        faults[proc_id]+=1
        cached[address]=True
        last_time[address]=nxt_time[i]
        mp[(last_time[address], address)]=1

    return faults
    out='OPTIMAL'
    for i in range(np): out+='  '+str(faults[i])
    print(out)

    return faults

def Random(VM_size, PM_size, np, memory_accesses):
    faults=[0 for i in range(np)]
    cached=[False for i in range(VM_size+1)]
    queue=[]

    from random import randint
    for access in memory_accesses:
        proc_id=access[0]
        address=access[1]
        if cached[address]: continue

        elif len(queue)==PM_size:
            victim_id=randint(0, len(queue)-1)
            cached[queue[victim_id]]=False
            del queue[victim_id]
            
        faults[proc_id]+=1
        cached[address]=True
        queue.append(address)

    return faults
    out='Random '
    for i in range(np): out+='  '+str(faults[i])
    print(out)

    return faults

def get_args(argv):
    args={}
    for word in argv[1:]:
        param, value=word.split('=')
        args[param]=int(value)
    return args

if __name__=='__main__':
    args=get_args(sys.argv)

    VM_size=args['vm']//args['ps']
    PM_size=args['pm']//args['ps']
    n=args['n']
    number_of_accesses=n*VM_size*PM_size

    from random import randint
    
    seq=[]
    for i in range(number_of_accesses):
        seq.append((randint(0, n-1), randint(1, VM_size)))

    print('PM size =', PM_size, ' VM size=', VM_size, ' count of process=', n)
    
    fifo_fualts=FIFO(VM_size, PM_size, n, seq)
    lru_faults=LRU(VM_size, PM_size, n, seq)
    lfu_faults=LFU(VM_size, PM_size, n, seq)
    opt_faults=OPTIMAL(VM_size, PM_size, n, seq)
    rnd_faults=Random(VM_size, PM_size, n, seq)

    for i in range(np):
        print('FIFO    PROCESS '+str(i)+'   '+str(fifo_faults[i]))
        print('LRU     PROCESS '+str(i)+'   '+str(lru_faults[i]))
        print('LFU     PROCESS '+str(i)+'   '+str(lfu_faults[i]))
        print('OPTIMAL PROCESS '+str(i)+'   '+str(opt_faults[i]))
        print('RANDOM  PROCESS '+str(i)+'   '+str(rnd_faults[i]))
