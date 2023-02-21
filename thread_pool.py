

class ThreadPool:
    
    
    def __init__(self):
        self.thread_pool = []
    
    def add_thread(self,thread):
        self.thread_pool.append(thread)
        
    def start_threading(self):
        
        for i in self.thread_pool:
            i.start()
            
    def join_thread(self):
        for i in self.thread_pool:
            i.join()
        
        