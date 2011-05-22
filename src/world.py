'''
Created on May 21, 2011

@author: bendavies
'''
import critters

class World(object):
    '''
    abstract class for defining an interface for world objects. World objects can be
    configured and run.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.plugins = list()
    
    def add_plugin(self, plugin):
        '''Adds a plugin
        >>> world = World()
        >>> len(world.plugins)
        0
        >>> world.add_plugin(EventPlugin())
        >>> len(world.plugins)
        1
        '''
        self.plugins.append(plugin)
        
        
    def run(self):
        '''
        Runs the world with the configuration provided
        '''
        return 0
    
        
    def send_population_start(self, population):
        '''triggers population start events in registered plugins'''
        for plugin in self.plugins:
            plugin.on_population_start(population)
        
    def send_population_end(self, population):
        '''triggers population end events in registered plugins'''
        for plugin in self.plugins:
            plugin.on_population_end(population)
        
    def send_iteration_start(self, iteration_no, population):
        '''sends iteration start events in registered plugins'''
        for plugin in self.plugins:
            plugin.on_iteration_start(iteration_no, population)
    
    def send_iteration_end(self, iteration_no, population):
        '''sends iteration end events in registered plugins'''
        for plugin in self.plugins:
            plugin.on_iteration_end(iteration_no, population)

    def send_interaction_end(self, agent1, agent1_outcome, agent2, agent2_outcome):
        '''send interaction end events to registered plugins'''
        for plugin in self.plugins:
            plugin.on_interaction_end(agent1, agent1_outcome,
                                      agent2, agent2_outcome)
    
    
class  PrisonersDilemmaWorld(World):
    '''
    creates a world with critters using different strategies to determine what 
    happens when they interact; Do they cooperate or not? Based on their mutual 
    decisions they are provided food
    '''
    
    def run(self, iterations=1500):
        '''
        executes the world
        >>> world = PrisonersDilemmaWorld()
        >>> world.run() # doctest:+ELLIPSIS
        simulation is commencing.
        simulation has finished.
        '''
        
        print 'simulation is commencing.'
        
        #create critter population
        sucker = critters.Critter('s1', critters.SuckerStrategy())
        cheater = critters.Critter('c1', critters.CheatStrategy())
        random = critters.Critter('r1', critters.RandomStrategy())
        grudger = critters.Critter('g1', critters.GrudgerStrategy())
        titter = critters.Critter('t1', critters.TitForTatStrategy())
        population = (sucker, cheater, random, grudger, titter)
        
        self.send_population_start(population)
          
        #execute iterations
        for i in range(1, iterations + 1):
            self.send_iteration_start(i, population)
            
            self.run_iteration(population)
            
            self.send_iteration_end(i, population)
                 
        self.send_population_end(population)    
        
        #finish simulation
        print('simulation has finished.')

    def run_iteration(self, population):
        '''
        runs a single iteration for population. The population itself is updated
        in the course of the exection. A population is a list of critters
        >>> world = PrisonersDilemmaWorld()
        >>> c1 = critters.Critter('c1', critters.CheatStrategy())
        >>> c2 = critters.Critter('c2', critters.CheatStrategy())
        >>> population = (c1,c2)
        >>> world.run_iteration(population)
        >>> population[1].food
        5

        '''
    
        interaction_list = self.determine_interactions(population)
        #print [(c1.name,c2.name) for (c1,c2) in interaction_list]
        
        for (c1, c2) in interaction_list:
            self.interact_critters(c1,c2)

    def determine_interactions(self, population):
        '''determines which interactions will happen within the population'''
        
        interactions = list()
        for critter in population:
            for other_critter in population:
                if (other_critter.name !=  critter.name and (critter,other_critter) not in interactions
                and (other_critter,critter) not in interactions):
                    interactions.append((critter, other_critter))
        return interactions


    def interact_critters(self, critter1, critter2):
        '''
        executes an interaction between 2 critters. Based on their own 
        response to the interaction, each is rewarded food (or not) based on 
        their response
        >>> world = PrisonersDilemmaWorld()
        >>> c1 = critters.Critter('c1', critters.CheatStrategy())
        >>> c2 = critters.Critter('c2', critters.CheatStrategy())
        >>> world.interact_critters(c1,c2)
        '''
        COOPERATE_FOOD = 3
        CHEATER_FOOD = 5
        SUCKER_FOOD = -1
        
        COOPERATE = critters.AbstractStrategy.COOPERATE
        UNCOOPERATE = critters.AbstractStrategy.UNCOOPERATE
        
        
        critter1_interaction = critter1.interact(critter2)
        critter2_interaction = critter2.interact(critter1)
        
        if (critter1_interaction == COOPERATE & 
            critter2_interaction == COOPERATE):
            
            critter1.add_food(COOPERATE_FOOD)
            critter2.add_food(COOPERATE_FOOD)
            
        elif (critter1_interaction == UNCOOPERATE &
                 critter2_interaction == UNCOOPERATE):
            #neither gets food
            pass
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
        self.send_interaction_end(critter1,critter1_interaction,
                                  critter2,critter2_interaction)
        

class EventPlugin(object):
    '''An archetype for plugin types'''

    def on_population_start(self, population):
        '''called prior to the start of iterations with the initial population'''
        pass
    
    def on_iteration_start(self, iteration_no, population):
        '''called at the start of the iteration'''
        pass
    
    def on_iteration_end(self, iteration_no, population):
        '''called at the end of the iteration'''
        pass
    
    def on_population_end(self, population):
        '''called at the end of the simulation when the population will no longer
        change'''
        pass
    
    def on_interaction_end(self, agent1, agent1_outcome, agent2, agent2_outcome):
        '''called at the end of an interaction between two agents'''
        pass
    
class TabularReporter(EventPlugin):
    '''Provides basic text output to the standard out'''

    def on_population_start(self, population):
        '''called prior to the start of iterations with the initial population'''
        self.print_headers(population)
    
    def on_iteration_start(self, iteration_no, population):
        '''called at the start of the iteration'''
        pass
    
    def on_iteration_end(self, iteration_no, population):
        '''called at the end of the iteration'''
        if iteration_no == 1 or iteration_no % 5 == 0:
            self.print_iteration_line(iteration_no, population)
    
    def on_population_end(self, population):
        '''called at the end of the simulation when the population will no longer
        change'''
        print 'Final Food Totals'
        self.print_iteration_line(0, population)
        self.print_headers(population)
        max_food = max([critter.food for critter in population])
        winners = [critter.name + ' ' for critter in population 
                   if (critter.food == max_food)]
        print('winners are %s' % ''.join(winners))
    
    def print_headers(self, population):
        '''Write the headers'''
        header_line = 'p:\t'
        for critter in population:
            header_line += '%s\t' % critter.name
        print header_line
        
    def print_iteration_line(self, iteration_no, population):
        '''Write a reporting line for the iteration with current food values'''        
        report_line = ('%d:\t' % iteration_no)
        for critter in population:
            report_line += '%d\t' % critter.food
        print report_line
        
class CritterTracker(EventPlugin):
    '''Keeps track of an individual critter and summarises their interaction at
    the conclusion of the population'''
    
    def __init__(self, critter_name):
        self.critter_name = critter_name
        self.interactions = list()
        super(CritterTracker, self).__init__()
 
    def on_population_end(self, population):
        '''
        Display a summary of what the tracked critter interacted
        '''
        UNCOOPERATE = critters.AbstractStrategy.UNCOOPERATE
        COOPERATE = critters.AbstractStrategy.COOPERATE
        
        print 'Detailed interaction tracking of %s:' % self.critter_name
        
        for interaction in self.interactions:
            our_action = interaction[1]
            their_action = interaction[3]
            their_name = interaction[2]
            
            if our_action == UNCOOPERATE and their_action == UNCOOPERATE:
                outcome_description = 'had no interaction with'
            elif our_action == COOPERATE and their_action == COOPERATE:
                outcome_description = 'cooperated with'
            elif our_action == COOPERATE:
                outcome_description = 'was suckered by'
            else:
                outcome_description = 'cheated'
                
            print '%s\t%d %d\t%s\t%s %s %s' % (self.critter_name, our_action,
                                               their_action, their_name, 
                                               self.critter_name, outcome_description, 
                                               their_name)
        
    
    def on_interaction_end(self, agent1, agent1_outcome, agent2, agent2_outcome):
        '''called at the end of an interaction between two agents'''
        if agent1.name == self.critter_name:
            self.interactions.append((agent1.name,
                                      agent1_outcome,
                                      agent2.name,
                                      agent2_outcome))               
        elif agent2.name == self.critter_name:
            self.interactions.append((agent2.name,
                                      agent2_outcome,
                                      agent1.name,
                                      agent1_outcome))               
            
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()    

