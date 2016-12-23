import commands
from multiprocessing.dummy import Pool as ThreadPool
from sys import argv
import os
 
def rsyncExec(ip):
    try:
        out = [ip]
        cmd = 'rsync '+ip+'::'
        (status,output) = commands.getstatusoutput('rsync '+ip+'::')
        if status == 0:
            model = output.split()
        else:
            model = '1'
        if model != '1':
            for x in model:
                (statusCheck,outputCheck) = commands.getstatusoutput('rsync '+ip+'::'+x+'/')
                if statusCheck == 0:
                    out.append(x)
        if len(out) > 1:
            return out
    except Exception as e:
        raise e
 
if __name__ == '__main__':
    try:
        ip,threed_num,password = argv[1:]
    except:
        ip,threed_num = argv[1:]
        password = 0
    if password != 0:
        os.environ['RSYNC_PASSWORD']=str(password)
    ips = [str(ip)+ '.' +str(x) for x in range(255)]
    pool = ThreadPool(int(threed_num))
    results = pool.map(rsyncExec,ips)
    pool.close()
    pool.join()
    fp = open('rsyncOut.txt','w')
    ret =  [str for str in results if str not in ['', ' ', None]]
    for x in ret:
        fp.write(x[0]+'    ')
        for i in x[1:]:
            fp.write(" '"+i+"'")
        fp.write('\n')
    fp.close