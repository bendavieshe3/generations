'''
Created on May 16, 2011

@author: bendavies
'''

class Critter(object):
    '''
    An agent within the simulation
    '''
    number_of = 0


    def __init__(self, name, strategy):
        '''critter constructor
        >>> Critter.number_of = 0
        >>> critter = Critter('c1', None)
        >>> critter.name
        'c1'
        >>> critter.food
        5
        >>> critter2 = Critter('c2', None)
        >>> critter2.name
        'c2'
        '''
        self.food = 5
        self.strategy = strategy
        Critter.number_of += 1
        if name is None:
            self.name = "Critter_%d" % Critter.number_of
        else:
            self.name = name
    
    def interact(self, other_critter):
        '''Interact with another critter
        >>> from strategies import CheatStrategy, SuckerStrategy
        >>> c1 = Critter('c1', CheatStrategy())
        >>> c2 = Critter('c2', CheatStrategy())
        >>> c1.interact(c2)
        0
        '''
        return self.strategy.interact(other_critter)
    
    def observe_interaction(self, critter1, critter1_action, 
                            critter2, critter2_action):
        '''
        take into account an interaction
        >>> from strategies import CheatStrategy, SuckerStrategy
        >>> c1 = Critter(None, CheatStrategy())
        >>> c2 = Critter(None, CheatStrategy())
        >>> c1.observe_interaction(c1,0,c2,0)
        '''
        self.strategy.observe_interaction(self, critter1, critter1_action, 
                                          critter2, critter2_action)
    
    def add_food(self, food_amount):
        '''
        Adds food to the critter
        >>> critter = Critter(None, None)
        >>> critter.add_food(10)
        >>> critter.food
        15
        '''
        self.food += food_amount
    
    def remove_food(self, food_amount):
        '''
        Removes food from the critter
        >>> critter = Critter(None, None)
        >>> critter.remove_food(10)
        >>> critter.food
        -5
        '''      
        self.food -= food_amount

if __name__ == '__main__':
    import doctest
    doctest.testmod()    
