'''
Created on Jan 4, 2013

@author: Praveen
'''

import re
import multiprocessing

from multiprocessing.managers import SyncManager

IP_ADDRESS = '10.104.1.51'
PORT_NUM = 50000

class MWorker(object):
    """ MulitProcessing Manager Client """
    
    def make_client(self):
        class QueueManager(SyncManager): pass
        QueueManager.register('get_job_q')
        QueueManager.register('get_result_q')
        m = QueueManager(address=(IP_ADDRESS, PORT_NUM), authkey='rackspace')
        m.connect()
        return m
    
    def run_client(self):
        manager = self.make_client()
        
        in_queue = manager.get_job_q()
        out_queue = manager.get_result_q()
        
        #procs_num = in_queue.get()
        procs = []
        
        #self.word_count(in_queue, out_queue)
        words_list = in_queue.get()
        if words_list == -1: return
        for i in words_list:
            p = multiprocessing.Process(
                    target=self.word_count,
                    args=(i, out_queue))
            procs.append(p)
            p.start()
     
        for p in procs:
            p.join()
        

    def word_count(self, text_blob, out_queue):
        """
        Tokenize a text blob into words
        """
        out_q_list = []
        out = re.split('(\W+)', text_blob)
        for i in out:
            if re.match(r'(\w+)', i.strip()):
                out_q_list.append(i)
        out_queue.put(out_q_list)

if __name__ == '__main__':
    print "Client connecting to a server....\n"
    mw_obj = MWorker()
    mw_obj.run_client()
    print "Job done."
