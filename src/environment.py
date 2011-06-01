'''
Created on May 25, 2011

@author: bendavies
'''
import critters, strategies

#constants
    
ITERATION_FOOD_CONSUMPTION = 3

FOOD_REQUIRED_TO_REPRODUCE = 150


class Environment(object):
    '''Hosts all of the objects in the simulation'''
    
    def __init__(self):
        '''
        Initialises the environment
        Usage:
        >>> env = Environment()
        '''
        self.iteration_no = 0
        self.population = dict()
        self.strategy_counts = dict()
     
    def start_iteration(self):
        self.iteration_no += 1

    def end_iteration(self):
        '''
        Ends the iteration and forces all critters to consume food
        '''
        
        #all critters consume food
        for critter in self.population.values():
            critter.remove_food(ITERATION_FOOD_CONSUMPTION)                
        
        
    def add_critter(self, critter):
        '''
        Adds a critter to the environment
        
        >>> e = Environment()
        >>> sucker = critters.Critter('s1', strategies.SuckerStrategy())
        >>> cheater = critters.Critter('c1', strategies.CheatStrategy())
        >>> e.add_critter(sucker)
        >>> len(e.population.values())
        1
        '''
        
        if not self.population.has_key(critter.name):
            self.population[critter.name] = critter
            critter.add_listener(self)
        
        strategy = critter.strategy.short_name        
        if strategy not in self.strategy_counts:
            self.strategy_counts[strategy] = 1
        else:
            self.strategy_counts[strategy] += 1 
    
    def add_critters(self, critter_list):
        '''
        Add multiple critters to the environment
        '''
        for critter in critter_list:
            self.add_critter(critter)
    
    def receive_event(self, source, event, data):
        '''
        Receive an event being listened for
        '''
        if event == critters.Critter.EVENT_DYING:
            # a critter has died, remove him from the list
            del self.population[source.name]
            
        elif event == critters.Critter.EVENT_REPRODUCING:
            # a critter has reproduced, add the offspring to the list
            self.add_critter(data['offspring'])
            
        else:
            print 'Received unknown event "%s"' % event
    
if __name__ == '__main__':
    import doctest
    doctest.testmod() 
    
    
    
    
