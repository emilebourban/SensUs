import multiprocessing as mp
import os
import time



def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(conn):
    info('function f')
    
    name = conn.recv()
    for i in range(10):
        print('hello', name)
        time.sleep(1)
    conn.send(name*2)




if __name__ == '__main__':
    info('main line')
    parent_conn, child_conn = mp.Pipe()
    p = mp.Process(target=f, args=(child_conn,))
    parent_conn.send('bob')
    p.start()
    for i in range(5):
        print(i)

        time.sleep(1)
#    child_conn.close()
#    p.terminate()
    try:
        x = parent_conn.recv()
        print(x)
    except EOFError:
        print('e')
        
    p.join()

#def info(title):
#    print(title)
#    print('module name:', __name__)
#    print('parent process:', os.getppid())
#    print('process id:', os.getpid())
#
#def f(conn):
#    info('function f')
#    name = conn.recv()
#    print('hello', name)
#    conn.send(name*2)
#
#
#
#
#if __name__ == '__main__':
#    info('main line')
#    parent_conn, child_conn = mp.Pipe()
#    p = mp.Process(target=f, args=(child_conn,))
#    parent_conn.send('bob')
#    p.start()
#    x = parent_conn.recv()
#    print(x)
#    p.join()
    
#
#def main():
#    parent_conn, child_conn = mpPipe()
#
#    child = Process(target=work, args=(child_conn,))
#
#    for item in (
#        42,
#        'some string',
#        {'one': 1},
#        CustomClass(),
#        None,
#    ):
#        print(
#            "PRNT: send: {}".format(item)
#        )
#        parent_conn.send(item)
#
#    child.start()
#    child.join() 