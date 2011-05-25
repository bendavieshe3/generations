'''
Created on May 24, 2011

@author: bendavies
'''
import strategies
    
    
class EventPlugin(object):
    '''An archetype for plugin types'''

    def on_environment_start(self, environment):
        '''called prior to the start of iterations with the initial environment'''
        pass
    
    def on_iteration_start(self, environment):
        '''called at the start of the iteration'''
        pass
    
    def on_iteration_end(self, environment):
        '''called at the end of the iteration'''
        pass
    
    def on_environment_end(self, environment):
        '''called at the end of the simulation when the environment will no longer
        change'''
        pass
    
    def on_interaction_end(self, agent1, agent1_outcome, agent2, agent2_outcome):
        '''called at the end of an interaction between two agents'''
        pass
    
class IndividualTabularReporter(EventPlugin):
    '''Provides basic text output to the standard out'''

    def on_environment_start(self, environment):
        '''called prior to the start of iterations with the initial environment'''
        self.print_headers(environment)
    
    def on_iteration_start(self, environment):
        '''called at the start of the iteration'''
        pass
    
    def on_iteration_end(self, environment):
        '''called at the end of the iteration'''
        if environment.iteration_no == 1 or environment.iteration_no % 5 == 0:
            self.print_iteration_line(environment)
    
    def on_environment_end(self, environment):
        '''called at the end of the simulation when the environment will no longer
        change'''
        print 'Final Food Totals'
        self.print_iteration_line(environment)
        self.print_headers(environment)
        
        population = environment.population
        max_food = max([critter.food for critter in population])
        winners = [critter.name + ' ' for critter in population 
                   if (critter.food == max_food)]
        print('winners are %s' % ''.join(winners))
    
    def print_headers(self, environment):
        '''Write the headers'''
        header_line = 'p:\t'
        for critter in environment.population:
            header_line += '%s\t' % critter.name
        print header_line
        
    def print_iteration_line(self, environment):
        '''Write a reporting line for the iteration with current food values'''        
        report_line = ('%d:\t' % environment.iteration_no)
        for critter in environment.population:
            report_line += '%d\t' % critter.food
        print report_line

class StrategyTabularReporter(EventPlugin):
    '''Provides basic output summarising strategy level numbers to the std out'''

    def on_environment_start(self, environment):
        '''called prior to the start of iterations with the initial environment'''
        self.print_headers(environment)
    
    def on_iteration_start(self, environment):
        '''called at the start of the iteration'''
        pass
    
    def on_iteration_end(self, environment):
        '''called at the end of the iteration'''
        if environment.iteration_no == 1 or environment.iteration_no % 5 == 0:
            self.print_iteration_line(environment)
    
    def on_environment_end(self, environment):
        '''called at the end of the simulation when the environment will no longer
        change'''
        print 'Final Population Totals'
        critter_count, food_count = self.calculate_strategy_totals(environment)
        
        self.print_iteration_line(environment)
        
        #print extra food totals line
        header_line = 'p:\t'
        for strategy in environment.strategy_counts.keys():
            header_line += '%s\t' % food_count[strategy]
        print header_line
                
        self.print_headers(environment)
        
        max_critters = max(critter_count.values())
        winners = [strategy + ' ' for strategy in critter_count.keys()
                   if critter_count[strategy] == max_critters]
        
        print('winners are %s' % ''.join(winners))
    
    def print_headers(self, environment):
        '''Write the headers'''
        header_line = 'p:\t'
        for strategy in environment.strategy_counts.keys():
            header_line += '%s\t' % strategy
        print header_line
        
    def print_iteration_line(self, environment):
        '''Write a reporting line for the iteration with current food values'''        
        
        #work out strategy totals
        critter_count, food_count = self.calculate_strategy_totals(environment)
        
        report_line = ('%d:\t' % environment.iteration_no)
        for strategy in environment.strategy_counts.keys():
            report_line += '%d\t' % critter_count[strategy]
        print report_line
        
    def calculate_strategy_totals(self, environment):
        food_count = dict()
        critter_count = dict()
        for strategy in environment.strategy_counts.keys():
            food_count[strategy] = 0
            critter_count[strategy] = 0
            
        for critter in environment.population:
            food_count[critter.strategy.short_name] += critter.food
            critter_count[critter.strategy.short_name] += 1
        
        return critter_count, food_count
        
class CritterTracker(EventPlugin):
    '''Keeps track of an individual critter and summarises their interaction at
    the conclusion of the environment'''
    
    def __init__(self, critter_name):
        self.critter_name = critter_name
        self.interactions = list()
        super(CritterTracker, self).__init__()
 
    def on_environment_end(self, environment):
        '''
        Display a summary of what the tracked critter interacted
        '''
        UNCOOPERATE = strategies.UNCOOPERATE
        COOPERATE = strategies.COOPERATE
        
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

