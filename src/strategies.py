'''
Created on May 24, 2011

@author: bendavies
'''

class AbstractStrategy(object):
    '''A strategy that provides a response to events'''
    
    UNCOOPERATE = 0
    COOPERATE = 1
    
    def interact(self, other_agent):
        '''
        perform an interaction with another agent and return a result code
        if not implemented in subclass, this always returns 0 for the default response
        >>> strategy = AbstractStrategy()
        >>> strategy.interact(Critter(None, None))
        0
        '''
        return AbstractStrategy.UNCOOPERATE
    
    def observe_interaction(self, me, agent1, agent1_action, agent2, agent2_action):
        '''
        provides information to the strategy about what transpired in an interaction.
        Does not return anything
        >>> strategy = AbstractStrategy()
        >>> strategy.observe_interaction(Critter(None, None), Critter(None, None), 1, Critter(None, None), 0)
        
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

class RandomStrategy(AbstractStrategy):
    '''A strategy that randomly decides to cooperate or not each time'''
    
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
        return random.choice((RandomStrategy.COOPERATE, 
                             RandomStrategy.UNCOOPERATE))

class GrudgerStrategy(AbstractStrategy):
    '''
    A strategy that never cooperates again with an agent that has failed
    to cooperate with this agent in the past
    >>> grudger_strategy = GrudgerStrategy()
    >>> grudger = Critter('g1', grudger_strategy)
    '''
    
    def __init__(self):
        ''' constructor'''
        super(GrudgerStrategy,self).__init__()
        self.agents_to_grudge = list()
        
    
    def interact(self, other_agent):
        '''
        Upon interacting, cooperate if the other agent has never not cooperated
        with this specific agent. If this is the first time of an interaction,
        cooperate
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
            return GrudgerStrategy.UNCOOPERATE
        return GrudgerStrategy.COOPERATE
    
    def observe_interaction(self, me, agent1, agent1_action, agent2, agent2_action):
        '''
        provides information to the strategy about what transpired in an interaction.
        Does not return anything
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
            if agent2_action == GrudgerStrategy.UNCOOPERATE:
                if self.agents_to_grudge.count(agent2.name) == 0:
                    self.agents_to_grudge.append(agent2.name)
        elif agent2.name == me.name:
            if agent1_action == GrudgerStrategy.UNCOOPERATE:
                if self.agents_to_grudge.count(agent1.name) == 0:
                    self.agents_to_grudge.append(agent1.name)
 
class TitForTatStrategy(AbstractStrategy):
    '''
    A strategy that will initially coperate with another agent, but will 
    punish an agent whose last action was to try to cheat tit for tat
    >>> t4t_strategy = TitForTatStrategy()
    >>> t4t = Critter('t1', t4t_strategy)
    '''
    
    def __init__(self):
        ''' constructor'''
        super(TitForTatStrategy,self).__init__()
        self.last_agent_interaction = dict()
        
    
    def interact(self, other_agent):
        '''
        Upon interacting, cooperate if the other agent was last known to cooperate.
        If the other agent last cheated, cheat back
        If this is the first time of an interaction cooperate
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
        return TitForTatStrategy.COOPERATE
    
    def observe_interaction(self, me, agent1, agent1_action, agent2, agent2_action):
        '''
        provides information to the strategy about what transpired in an interaction.
        Does not return anything
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
