'''
Created on May 16, 2011

@author: bendavies
'''

class Critter(object):
    '''
    An agent within the simulation
    '''
    number_of = 0


    def __init__(self, strategy):
        '''critter constructor
        >>> Critter.number_of = 0
        >>> critter = Critter(None)
        >>> critter.name
        'Critter_1'
        >>> critter.food
        0
        >>> critter2 = Critter(None)
        >>> critter2.name
        'Critter_2'
        '''
        self.food = 0
        self.strategy = strategy
        Critter.number_of += 1
        self.name = "Critter_%d" % Critter.number_of
    
    def interact(self, other_critter):
        '''Interact with another critter
        >>> c1 = Critter(CheatStrategy())
        >>> c2 = Critter(CheatStrategy())
        >>> c1.interact(c2)
        0
        '''
        return self.strategy.interact(other_critter)
    
    def observe_interaction(self, critter1, critter1_action, 
                            critter2, critter2_action):
        '''
        take into account an interaction
        >>> c1 = Critter(CheatStrategy())
        >>> c2 = Critter(CheatStrategy())
        >>> c1.observe_interaction(c1,0,c2,0)
        '''
        self.strategy.observe_interaction(critter1, critter1_action, 
                                          critter2, critter2_action)
    
    def add_food(self, food_amount):
        '''
        Adds food to the critter
        >>> critter = Critter(None)
        >>> critter.add_food(10)
        >>> critter.food
        10
        '''
        self.food += food_amount
    
    def remove_food(self, food_amount):
        '''
        Removes food from the critter
        >>> critter = Critter(None)
        >>> critter.remove_food(10)
        >>> critter.food
        -10
        '''      
        self.food -= food_amount

class AbstractStrategy(object):
    '''A strategy that provides a response to events'''
    
    UNCOOPERATE = 0
    COOPERATE = 1
    
    def interact(self, other_agent):
        '''
        perform an interaction with another agent and return a result code
        if not implemented in subclass, this always returns 0 for the default response
        >>> strategy = AbstractStrategy()
        >>> strategy.interact(Critter(None))
        0
        '''
        return AbstractStrategy.UNCOOPERATE
    
    def observe_interaction(self, agent1, agent1_action, agent2, agent2_action):
        '''
        provides information to the strategy about what transpired in an interaction.
        Does not return anything
        >>> strategy = AbstractStrategy()
        >>> strategy.observe_interaction(Critter(None), 1, Critter(None), 0)
        
        '''
        pass
        
class CheatStrategy(AbstractStrategy):
    '''A strategy that always fails to cooperate'''
    
    def interact(self, other_agent):
        '''
        Upon interacting this agent always fails to cooperate (ie return 0)
        >>> taker_strategy = CheatStrategy()
        >>> taker_strategy.interact(None)
        0
        '''
        return CheatStrategy.UNCOOPERATE
    
class SuckerStrategy(AbstractStrategy):
    '''A strategy that never fails to cooperate'''
    
    def interact(self, other_agent):
        '''
        Upon interacting this agent never fails to cooperate (ie return 1)
        >>> sucker_strategy = SuckerStrategy()
        >>> sucker_strategy.interact(None)
        1
        '''
        return SuckerStrategy.COOPERATE

if __name__ == '__main__':
    import doctest
    doctest.testmod()    
