'''
Created on May 16, 2011

@author: bendavies
'''
#constants
import random

BASE_OBJECT_NAME = 'object'
  

def get_new_id():
    '''
    determines a new id to assign to an object in the environment
    >>> get_new_id()     # doctest:+ELLIPSIS, +SKIP
    '''
    EnvironmentObject.number_of += 1
    return '%s_%d' % (BASE_OBJECT_NAME, EnvironmentObject.number_of)
    
class EnvironmentObject(object):
    '''
    A generic object within the environment. Ages with iterations and
    can send events
    '''
    
    #static variables
    number_of = 0
  
    def __init__(self, name):
        '''
        Constructor
        >>> o = EnvironmentObject(None)
        >>> p = EnvironmentObject('peter')
        >>> p.name 
        'peter'
        '''
        self.name = name if name else get_new_id()
        self.event_listener_map = dict()

    def add_listener(self, listener, event='*'):
        '''
        Attaches a listener to the object for all or specific events
        '''
        if not self.event_listener_map.has_key(event):
            self.event_listener_map[event] = list()
        self.event_listener_map[event].append(listener)
                
    def send_event(self, source, event, data):
        '''
        Dispatches the provided event with the data to registered listeners 
        for that event
        '''
        if self.event_listener_map.has_key(event):
            for listener in self.event_listener_map[event]:
                listener.receive_event(self, event, data)
        if self.event_listener_map.has_key('*'):
            for listener in self.event_listener_map['*']:
                listener.receive_event(self, event, data)        

class Listener(object):
    ''' 
    A generic listener
    '''
    
    def receive_event(self, source, event, data):
        pass

class Critter(EnvironmentObject):
    '''
    An agent within the simulation
    '''
    
    #events
    EVENT_REPRODUCING = 'reproducing'
    EVENT_DYING = 'dying'
    
    #other constants
    FOOD_REQUIRED_TO_REPRODUCE = 1000
    CHANCE_OF_RANDOM_MUTATION = 0.01 #1 percent

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
        self.food = 10
        self.offspring = 0
        self.strategy = strategy
        super(Critter,self).__init__(name)
    
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
        
        if self.food > Critter.FOOD_REQUIRED_TO_REPRODUCE:
            self.reproduce()
    
    def remove_food(self, food_amount):
        '''
        Removes food from the critter
        >>> critter = Critter(None, None)
        >>> critter.remove_food(10)
        >>> critter.food
        -5
        '''      
        self.food -= food_amount
        
        if self.food <= 0:
            self.send_event(self, Critter.EVENT_DYING, 
                            {'cause':'starvation'})

    def reproduce(self):
        '''
        Creates and returns one or more offspring
        >>> import strategies
        >>> c1 = Critter(None, strategies.CheatStrategy())
        >>> c1_1 = c1.reproduce()
        '''
        
        #update this critter
        self.offspring += 1
        self.remove_food(Critter.FOOD_REQUIRED_TO_REPRODUCE)
        
        if random.random() <= Critter.CHANCE_OF_RANDOM_MUTATION:
            #offspring is mutant
            offspring = self.random_mutation()
        else:
            offspring_name = '%s_%d' % (self.name, self.offspring)
            offspring = (Critter(offspring_name, self.strategy.create_new()))
        
        self.send_event(self, Critter.EVENT_REPRODUCING, 
                        {'offspring':offspring})
        
        return offspring
    
    def random_mutation(self):
        '''
        returns a randomly selected alternative 'mutant' offspring
        with a randomly selected strategy
        '''
        import strategies
        
        sucker = Critter(None, strategies.SuckerStrategy())
        cheater = Critter(None, strategies.CheatStrategy())
        random1 = Critter(None, strategies.RandomStrategy())
        random2 = Critter(None, strategies.RandomStrategy(3))
        grudger = Critter(None, strategies.GrudgerStrategy())
        titter = Critter(None, strategies.TitForTatStrategy())            
        
        possible_mutations = (sucker, cheater, random1, random2, grudger,
                              titter)
        return random.choice(possible_mutations)
        
            

if __name__ == '__main__':
    import doctest
    doctest.testmod()    
