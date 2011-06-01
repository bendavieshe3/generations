'''
Created on May 21, 2011

@author: bendavies
'''
import random
import critters, strategies, environment as env

class World(object):
    '''
    abstract class for defining the rules and actions of an environment
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.plugins = list()
    
    def add_plugin(self, plugin):
        '''Adds a plugin
        >>> import plugins
        >>> world = World()
        >>> len(world.plugins)
        0
        >>> world.add_plugin(plugins.EventPlugin())
        >>> len(world.plugins)
        1
        '''
        self.plugins.append(plugin)
        
        
    def run(self):
        '''
        Runs the world with the configuration provided
        '''
        return 0
    
        
    def send_environment_start(self, environment):
        '''triggers environment start events in registered plugins'''
        for plugin in self.plugins:
            plugin.on_environment_start(environment)
        
    def send_environment_end(self, environment):
        '''triggers environment end events in registered plugins'''
        for plugin in self.plugins:
            plugin.on_environment_end(environment)
        
    def send_iteration_start(self, environment):
        '''sends iteration start events in registered plugins'''
        for plugin in self.plugins:
            plugin.on_iteration_start(environment)
    
    def send_iteration_end(self, environment):
        '''sends iteration end events in registered plugins'''
        for plugin in self.plugins:
            plugin.on_iteration_end(environment)

    def send_interaction_end(self, environment, agent1, agent1_outcome, agent2, agent2_outcome):
        '''send interaction end events to registered plugins'''
        for plugin in self.plugins:
            plugin.on_interaction_end(environment, 
                                      agent1, agent1_outcome,
                                      agent2, agent2_outcome)
    
    
class  PrisonersDilemmaWorld(World):
    '''
    creates a world with critters using different strategies to determine what 
    happens when they interact; Do they cooperate or not? Based on their mutual 
    decisions they are provided food
    '''
    
    def run(self, iterations=15):
        '''
        executes the world
        >>> world = PrisonersDilemmaWorld()
        >>> world.run() # doctest:+ELLIPSIS
        simulation is commencing.
        simulation has finished.
        '''
        
        print 'simulation is commencing.'
        
        #create environment and critters to populate it
        environment = env.Environment()
        
        sucker = critters.Critter('s1', strategies.SuckerStrategy())
        cheater = critters.Critter('c1', strategies.CheatStrategy())
        random = critters.Critter('r1', strategies.RandomStrategy())
        random2 = critters.Critter('r2', strategies.RandomStrategy(3))
        grudger = critters.Critter('g1', strategies.GrudgerStrategy())
        titter = critters.Critter('t1', strategies.TitForTatStrategy())
        
        environment.add_critters((sucker, cheater, random, random2, grudger, titter))
        
        self.send_environment_start(environment)
        
        #execute iterations
        for i in range(iterations):

            environment.start_iteration()
            
            self.send_iteration_start(environment)
            
            self.run_iteration(environment)
            
            self.send_iteration_end(environment)
            
            environment.end_iteration()
                 
        self.send_environment_end(environment)    
        
        #finish simulation
        print('simulation has finished.')

    def run_iteration(self, environment):
        '''
        runs a single iteration for the provided environment. The population itself is updated
        in the course of the exection. A population is a list of critters
        >>> world = PrisonersDilemmaWorld()
        >>> c1 = critters.Critter('c1', strategies.CheatStrategy())
        >>> c2 = critters.Critter('c2', strategies.CheatStrategy())
        >>> environment = env.Environment()
        >>> environment.add_critters((c1,c2))
        >>> world.run_iteration(environment)
        >>> environment.population['c1'].food
        5

        '''
    
        interaction_list = self.determine_interactions(environment.population)
        #print [(c1.name,c2.name) for (c1,c2) in interaction_list]
        
        for (c1, c2) in interaction_list:
            self.interact_critters(environment, c1,c2)

    def determine_interactions(self, population):
        '''determines which interactions will happen within the population'''
        
        NUMBER_OF_INTERACTIONS = 5
        
        interactions = list()
        for critter in population.values():
            
            critters_to_interact_with = list(population.values())
            critters_to_interact_with.remove(critter)
            
            for i in range(0, NUMBER_OF_INTERACTIONS):
                
                if len(critters_to_interact_with) > 0:
                
                    other_critter = random.choice(critters_to_interact_with)
                    if (critter.name < other_critter.name and(critter,other_critter) not in interactions) or\
                        (other_critter.name > critter.name and (other_critter, critter) not in interactions):
                        
                        if critter.name < other_critter.name:
                            interactions.append((critter, other_critter))
                        else:
                            interactions.append((other_critter, critter))
                        
                        critters_to_interact_with.remove(other_critter)
                          
        return interactions


    def interact_critters(self, environment, critter1, critter2):
        '''
        executes an interaction between 2 critters. Based on their own 
        response to the interaction, each is rewarded food (or not) based on 
        their response
        >>> world = PrisonersDilemmaWorld()
        >>> c1 = critters.Critter('c1', strategies.CheatStrategy())
        >>> s1 = critters.Critter('s1', strategies.SuckerStrategy())
        >>> world.interact_critters(None,c1,s1)
        >>> c1.food
        35
        >>> s1.food
        4
        
        '''
        COOPERATE_FOOD = 4
        CHEATER_FOOD = 6
        SUCKER_FOOD = -1
        PASSIVE_FOOD = 0
        
        COOPERATE = strategies.COOPERATE
        UNCOOPERATE = strategies.UNCOOPERATE
        
        
        critter1_interaction = critter1.interact(critter2)
        critter2_interaction = critter2.interact(critter1)
        
        if (critter1_interaction == COOPERATE and 
            critter2_interaction == COOPERATE):
    
            critter1.add_food(COOPERATE_FOOD)
            critter2.add_food(COOPERATE_FOOD)
            
        elif (critter1_interaction == UNCOOPERATE and
                 critter2_interaction == UNCOOPERATE):
            #neither gets food
    
            critter1.add_food(PASSIVE_FOOD)
            critter2.add_food(PASSIVE_FOOD)                
        else:
            #one cheated the other
    
            if critter1_interaction == COOPERATE:
                #critter1 is the sucker
                critter1.add_food(SUCKER_FOOD)
                critter2.add_food(CHEATER_FOOD)
    
            else:
                #critter2 is the sucker
                critter2.add_food(SUCKER_FOOD)
                critter1.add_food(CHEATER_FOOD)
    
        #Critters observe the outcome
        critter1.observe_interaction(critter1,critter1_interaction,
                                     critter2,critter2_interaction)
        critter2.observe_interaction(critter1,critter1_interaction,
                                     critter2,critter2_interaction)
        
        #So do plugins!
        self.send_interaction_end(environment,
                                  critter1,critter1_interaction,
                                  critter2,critter2_interaction)

    
if __name__ == '__main__':
    import doctest
    doctest.testmod()    

