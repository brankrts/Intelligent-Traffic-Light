class LightQueue:
  def __init__(self, queue=[]):
    self.queue = list(queue)
  
  def push(self, item):
    self.queue.append(item)
    return self.queue
  
  def pop(self):
    item_0 = self.queue[0]
    del self.queue[0]
    return item_0
  
  def length(self):
    return len(self.queue)
  
  def __repr__(self):
    return f"{self.queue}"
  
  def updateLight(self,light,density):
    if light != None:
      for i in self.queue:
        if i.getName() == light.getName():
          i.setDensity(density)
          
      
    
    
    
