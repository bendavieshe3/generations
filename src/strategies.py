'''
Created on May 24, 2011

@author: bendavies
'''

#constants
UNCOOPERATE = 0
COOPERATE = 1
    
class AbstractStrategy(object):
    '''A strategy that provides a response to events'''
    
    short_class_name = 'ABS'

    def get_short_name(self):
        '''
        Return the short name to identify this strategy
        >>> s1 = SuckerStrategy()
        >>> s1.short_name
        'SCK'
        '''
        return self.__class__.short_class_name


    short_name = property(get_short_name)
    

    def interact(self, other_agent):
        '''
        perform an interaction with another agent and return a result code
        if not implemented in subclass, this always returns 0 for the default response
        >>> from critters import Critter
        >>> strategy = AbstractStrategy()
        >>> strategy.interact(Critter(None, None))
        0
        '''
        return UNCOOPERATE
    
    def observe_interaction(self, me, agent1, agent1_action, agent2, agent2_action):
        '''
        provides information to the strategy about what transpired in an interaction.
        Does not return anything
        >>> from critters import Critter
        >>> strategy = AbstractStrategy()
        >>> strategy.observe_interaction(Critter(None, None), Critter(None, None), 1, Critter(None, None), 0)
        
        '''
        pass
    
    def create_new(self):
        '''
        creates a new version of this strategy inheriting its traits (including
        constructor arguments, but not instance variables)
        >>> r1 = RandomStrategy(3)
        >>> r1_1 = r1.create_new()
        >>> r1_1.chance_to_cooperate
        0.75
        '''
        return self.__class__()
        
        
class CheatStrategy(AbstractStrategy):
    '''A strategy that always fails to cooperate'''
    
    short_class_name = 'CHT'
    
    def interact(self, other_agent):
        '''
        Upon interacting this agent always fails to cooperate (ie return 0)
        >>> taker_strategy = CheatStrategy()
        >>> taker_strategy.interact(None)
        0
        '''
        return UNCOOPERATE
    
class SuckerStrategy(AbstractStrategy):
    '''A strategy that never fails to cooperate'''
    
    short_class_name = 'SCK'
    
    def interact(self, other_agent):
        '''
        Upon interacting this agent never fails to cooperate (ie return 1)
        >>> sucker_strategy = SuckerStrategy()
        >>> sucker_strategy.interact(None)
        1
        '''
        return COOPERATE

class RandomStrategy(AbstractStrategy):
    '''A strategy that randomly decides to cooperate or not each time'''
    
    short_class_name = 'RND'
    
    def __init__(self, cooperation_weight = 1):
        self.cooperation_weight = cooperation_weight
        self.chance_to_cooperate = self.calc_coop_chance(cooperation_weight)
        super(AbstractStrategy, self).__init__()
    
    def get_short_name(self):
        '''
        Return the short name to identify this strategy
        >>> r1 = RandomStrategy(3)
        >>> r1.short_name
        'RND_3'
        '''
        return '%s_%d' % (self.__class__.short_class_name,
                          self.cooperation_weight)

    short_name = property(get_short_name)
    
    def calc_coop_chance(self, coop_weight):
        '''
        determine the chance of cooperation given a cooperation weight and an
        assumed uncooperate weight of 1. Thus:
        >>> RandomStrategy().calc_coop_chance(1)
        0.5
        '''
        return (float(coop_weight) / float(coop_weight + 1))
    
    def create_new(self):
        ''' 
        Create a new Random Strategy with the same chance to cooperate
        '''
        return self.__class__(self.cooperation_weight)
        
    
    def interact(self, other_agent):
        '''
        Upon interacting this strategy advising a random outcome
        >>> random_strategy = RandomStrategy()
        >>> random_strategy.interact(None) # doctest:+ELLIPSIS, +SKIP
        1
        >>> random_strategy = RandomStrategy()
        >>> random_strategy.interact(None) # doctest:+ELLIPSIS, +SKIP
        0
        '''
        
        import random
        if random.random() <= self.chance_to_cooperate:
            return COOPERATE
        else:
            return UNCOOPERATE

class GrudgerStrategy(AbstractStrategy):
    '''
    A strategy that never cooperates again with an agent that has failed
    to cooperate with this agent in the past
    >>> from critters import Critter
    >>> grudger_strategy = GrudgerStrategy()
    >>> grudger = Critter('g1', grudger_strategy)
    '''
    
    short_class_name = 'GRD'
    
    def __init__(self):
        ''' constructor'''
        super(GrudgerStrategy,self).__init__()
        self.agents_to_grudge = list()
        
    
    def interact(self, other_agent):
        '''
        Upon interacting, cooperate if the other agent has never not cooperated
        with this specific agent. If this is the first time of an interaction,
        cooperate
        >>> from critters import Critter
        >>> g = Critter('g', GrudgerStrategy())
        >>> c1 = Critter('c1', None)
        >>> c2 = Critter('c1', None)
        >>> g.interact(c1)
        1
        >>> g.interact(c2)
        1
        >>> g.observe_interaction(g, 1, c1, 0)
        >>> g.interact(c1)
        0
        >>> g.interact(c1)
        0
        '''
        if self.agents_to_grudge.count(other_agent.name): 
            return UNCOOPERATE
        else:
            return COOPERATE
    
    def observe_interaction(self, me, agent1, agent1_action, agent2, agent2_action):
        '''
        provides information to the strategy about what transpired in an interaction.
        Does not return anything
        >>> from critters import Critter
        >>> grudger_strategy = GrudgerStrategy()
        >>> grudger = Critter('g1', grudger_strategy)
        >>> other_critter1 = Critter('c1', None)
        >>> other_critter2 = Critter('c2', None)
        >>> #observer other interaction
        >>> grudger_strategy.observe_interaction(grudger, other_critter1, 1, other_critter2, 0)
        >>> grudger_strategy.observe_interaction(grudger, grudger, 1, other_critter2, 0)
        >>> grudger_strategy.observe_interaction(grudger, grudger, 0, other_critter1, 1)
        >>> grudger_strategy.agents_to_grudge
        ['c2']
        '''
        if agent1.name == me.name:
            if agent2_action == UNCOOPERATE:
                if self.agents_to_grudge.count(agent2.name) == 0:
                    self.agents_to_grudge.append(agent2.name)
        elif agent2.name == me.name:
            if agent1_action == UNCOOPERATE:
                if self.agents_to_grudge.count(agent1.name) == 0:
                    self.agents_to_grudge.append(agent1.name)
 
class TitForTatStrategy(AbstractStrategy):
    '''
    A strategy that will initially coperate with another agent, but will 
    punish an agent whose last action was to try to cheat tit for tat
    >>> from critters import Critter
    >>> t4t_strategy = TitForTatStrategy()
    >>> t4t = Critter('t1', t4t_strategy)
    '''
    
    short_class_name = 'T4T'
    
    def __init__(self):
        ''' constructor'''
        super(TitForTatStrategy,self).__init__()
        self.last_agent_interaction = dict()
        
    
    def interact(self, other_agent):
        '''
        Upon interacting, cooperate if the other agent was last known to cooperate.
        If the other agent last cheated, cheat back
        If this is the first time of an interaction cooperate
        >>> from critters import Critter
        >>> t = Critter('t', TitForTatStrategy())
        >>> c1 = Critter('c1', None)
        >>> c2 = Critter('c1', None)
        >>> t.interact(c1)
        1
        >>> t.interact(c2)
        1
        >>> t.observe_interaction(t, 1, c1, 0)
        >>> t.interact(c1)
        0
        >>> t.observe_interaction(t, 1, c1, 1)
        >>> t.interact(c1)
        1
        '''
        if self.last_agent_interaction.has_key(other_agent.name): 
            return self.last_agent_interaction[other_agent.name]
        else:
            return COOPERATE
    
    def observe_interaction(self, me, agent1, agent1_action, agent2, agent2_action):
        '''
        provides information to the strategy about what transpired in an interaction.
        Does not return anything
        >>> from critters import Critter
        >>> t4t_strategy = TitForTatStrategy()
        >>> t4t = Critter('t1', t4t_strategy)
        >>> other_critter1 = Critter('c1', None)
        >>> other_critter2 = Critter('c2', None)
        >>> #observer other interaction
        >>> t4t_strategy.observe_interaction(t4t, other_critter1, 1, other_critter2, 0)
        >>> t4t_strategy.observe_interaction(t4t, t4t, 1, other_critter2, 0)
        >>> t4t_strategy.observe_interaction(t4t, t4t, 0, other_critter1, 1)
        >>> t4t_strategy.last_agent_interaction
        {'c2': 0, 'c1': 1}
        '''
        if agent1.name == me.name:
            self.last_agent_interaction[agent2.name] = agent2_action
        elif agent2.name == me.name:
            self.last_agent_interaction[agent1.name] = agent1_action

    
if __name__ == '__main__':
    import doctest
    doctest.testmod()    
