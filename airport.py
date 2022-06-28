
from priority_queue import AdaptableHeapPriorityQueue
from airport_base import AirportBase



class Airport(AirportBase):

    """
        Implement all the necessary methods of the Airport here
    """

        
        
    class Shuttle(AirportBase.ShuttleBase):
        """
            Implement all the necessary methods of the Shuttle here
        """
        
        def __init__(self, origin, destination, time):
            self.source = origin
            self.destination = destination
            self.time = time
            self.cap = 0
 
        
  
        
       
    class Terminal(AirportBase.TerminalBase):
        """
            Implement all the necessary methods of the Terminal here
        
        """
        
        def __init__(self, id: str, waiting_time: int):
            self.id = id
            self.waiting_time = waiting_time
            self.outgoing = []
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.terminals = []
        self.shuttles = []
        
        
    def opposite(self, shuttle, terminal):
        if shuttle.source.id == terminal.id:
            return shuttle.destination
        elif shuttle.destination.id == terminal.id:
            return shuttle.source
        return None
    
    def insert_terminal(self, terminal):
        self.terminals = self.terminals + [terminal]
        return terminal
    
    def insert_shuttle(self, origin, destination, time):
        shuttle = Airport.Shuttle(origin, destination, time)
        self.shuttles = self.shuttles + [shuttle]
        shuttle.cap = self.capacity
            
        origin.outgoing = origin.outgoing + [shuttle]  
        destination.outgoing = destination.outgoing + [shuttle]
        return shuttle
    
    def remove_terminal(self, terminal):
        if terminal in self.terminals:
            shuttles_copy = list(self.shuttles)
            for s in shuttles_copy:
                if self.opposite(s, terminal) is not None:
                    self.remove_shuttle(s)
            self.terminals.remove(terminal)
            return True
        return False

    def remove_shuttle(self, shuttle):
        if shuttle in self.shuttles:
            self.shuttles.remove(shuttle)
            shuttle.source.outgoing.remove(shuttle)
            shuttle.destination.outgoing.remove(shuttle)
            return True
        return False
        
    
    def outgoing_shuttles(self, terminal):
        return terminal.outgoing

    def find_shortest_path(self, origin, destination):
        visited_terminal = []
        visited_shuttle = []
        Q = [([origin], origin.waiting_time, [])]
        while len(Q) != 0:
            front = Q.pop(0)
            path = front[0]
            time = front[1]
            shuttles = front[2]
            v = path[-1]
            outgoing = self.outgoing_shuttles(v)
            for e in outgoing:
                if e not in visited_shuttle:
                    visited_shuttle.append(e)
                    w = self.opposite(e, v)
                    if w not in visited_terminal:
                        new_shuttles = list(shuttles)
                        new_shuttles.append(e)
                        new_path = list(path)
                        new_path.append(w)
                        new_time = time + e.time + w.waiting_time
                        Q.append((new_path, new_time, new_shuttles))
                        visited_terminal = visited_terminal + [w]
                        if w.id == destination.id:
                            for s in new_shuttles:
                                s.cap = s.cap - 1
                                if s.cap == 0:
                                    self.remove_shuttle(s)                             
                            return (new_path, new_time - w.waiting_time)            
        return (None, None)
        
    
    def find_fastest_path(self, origin, destination):
        PQ = AdaptableHeapPriorityQueue()
        visited = []
        locators = {}
        paths = {origin: [origin]}
        shuttles = {origin: []}
        num_outgoing = len(self.outgoing_shuttles(destination))
        if num_outgoing == 0:
            return (None, None)
        for v in self.terminals:
            if v.id == origin.id:
                distance = 0
            else:
                distance = float('inf')   
            loc = PQ.add(distance, v)
            locators[v] = (loc, distance)
        while PQ.is_empty() == False:
            u = PQ.remove_min()
            term = u[1]
            for e in self.outgoing_shuttles(term):
                if e not in visited:
                    visited.append(e)
                    z = self.opposite(e, term)
                    r = locators[term][1] + term.waiting_time +  e.time
                    if locators[z][1] == float('inf') and term not in paths:
                        return (None, None)
                    if locators[z][1] == float('inf') or r < locators[z][1]:
                        PQ.update(locators[z][0], r, z)
                        loc = locators[z][0]
                        locators[z] = (loc, r)
                        new_path = list(paths[term])
                        new_shuttles = list(shuttles[term])
                        new_path.append(z)   
                        new_shuttles.append(e)
                        paths[z] = new_path
                        shuttles[z] = new_shuttles
            if term.id == destination.id:
                for s in shuttles[destination]:
                    s.cap = s.cap - 1
                    if s.cap == 0:
                        self.remove_shuttle(s) 
                return (paths[destination], locators[destination][1])   
        return (None, None)
            

    

    
  
    
  


