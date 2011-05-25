'''
Created on May 25, 2011

@author: bendavies
'''
import critters, strategies

#constants
    
ITERATION_FOOD_CONSUMPTION = 5


class Environment(object):
    '''Hosts all of the objects in the simulation'''
    
    def __init__(self):
        '''
        Initialises the environment
        Usage:
        >>> env = Environment()
        '''
        self.iteration_no = 0
        self.population = list()
        self.strategy_counts = dict()
     
    def start_iteration(self):
        self.iteration_no += 1

    def end_iteration(self):
        '''
        Ends the iteration and forces all critters to consume food
        '''
        
        #all critters consume food
        for critter in self.population:
            critter.remove_food(ITERATION_FOOD_CONSUMPTION)
            
            #if a critter has 0 or less food, he dies :(
            if critter.food <= 0:
                self.population.remove(critter)
        
    def add_critter(self, critter):
        '''
        Adds a critter to the environment
        
        >>> e = Environment()
        >>> sucker = critters.Critter('s1', strategies.SuckerStrategy())
        >>> cheater = critters.Critter('c1', strategies.CheatStrategy())
        >>> e.add_critter(sucker)
        >>> len(e.population)
        1
        '''
        
        if critter not in self.population:
            self.population.append(critter)
        
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
    
if __name__ == '__main__':
    import doctest
    doctest.testmod() 
    
    
    
    
