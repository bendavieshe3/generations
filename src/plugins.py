'''
Created on May 24, 2011

@author: bendavies
'''
import strategies, critters
    
    
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
    
    def on_interaction_end(self, environment, agent1, agent1_outcome, agent2, agent2_outcome):
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

    def __init__(self, iteration_reporting_interval=5, output_filename=None):
        '''
        Constructor
        '''
        self.reporting_interval = iteration_reporting_interval
        self.output_filename = output_filename
        self.file = None

    def on_environment_start(self, environment):
        '''called prior to the start of iterations with the initial environment'''
        if self.output_filename:
            self.file = open(self.output_filename, 'w')
            
        self.print_headers(environment)
    
    def on_iteration_start(self, environment):
        '''called at the start of the iteration'''
        pass
    
    def on_iteration_end(self, environment):
        '''called at the end of the iteration'''
        if (environment.iteration_no == 1 or environment.iteration_no % 
            self.reporting_interval == 0):
            
            self.print_iteration_line(environment)
    
    def on_environment_end(self, environment):
        '''called at the end of the simulation when the environment will no longer
        change'''
        self.output_line('Final Population Totals')
        critter_count, food_count = self.calculate_strategy_totals(environment)
        
        self.print_iteration_line(environment)
        
        #print extra food totals line
        header_line = 'food:\t'
        total_food_in_population = 0
        for strategy in environment.strategy_counts.keys():
            header_line += '%s\t' % food_count[strategy]
            total_food_in_population += food_count[strategy]
        header_line += '%d' % total_food_in_population
        self.output_line(header_line)
                
        self.print_headers(environment)
        
        max_critters = max(critter_count.values())
        winners = [strategy + ' ' for strategy in critter_count.keys()
                   if critter_count[strategy] == max_critters]
        
        self.output_line('winners are %s' % ''.join(winners))
        
        if self.file:
            self.file.close()
        
    
    def print_headers(self, environment):
        '''Write the headers'''
        header_line = 'strat:\t'
        for strategy in environment.strategy_counts.keys():
            header_line += '%s\t' % strategy
        header_line += 'TOTAL'
        self.output_line(header_line)
        
    def print_iteration_line(self, environment):
        '''Write a reporting line for the iteration with current food values'''        
        
        #work out strategy totals
        critter_count, food_count = self.calculate_strategy_totals(environment)
        
        report_line = ('%d\t' % environment.iteration_no)
        for strategy in environment.strategy_counts.keys():
            report_line += '%d\t' % critter_count[strategy]
        report_line += '%d' % len(environment.population)
        self.output_line(report_line)
        
    def calculate_strategy_totals(self, environment):
        food_count = dict()
        for strategy in environment.strategy_counts.keys():
            food_count[strategy] = 0
            
        for critter in environment.population.values():
            food_count[critter.strategy.short_name] += critter.food

        return environment.strategy_counts, food_count
    
    def output_line(self, line):
        '''
        Outputs the provided line to the console, and, if configured, the 
        reporting file
        '''
        print line
        if self.file:
            self.file.write('%s\n' % line)
        
class CritterTracker(EventPlugin):
    '''Keeps track of an individual critter and summarises their interaction at
    the conclusion of the environment'''

    #constants
    LOG_ITEM_INTERACTION = 'interaction'
    LOG_ITEM_DEATH = 'death'
    LOG_ITEM_REPRODUCTION = 'reproduction'

    def __init__(self, critter_name):
        self.critter_name = critter_name
        self.log_items = list()
        self.attached = False
        self.iteration_no = 0
        super(CritterTracker, self).__init__()
  
    def on_environment_end(self, environment):
        '''
        Display a summary of what the tracked critter interacted
        '''
        UNCOOPERATE = strategies.UNCOOPERATE
        COOPERATE = strategies.COOPERATE
        
        print 'Detailed tracking of %s:' % self.critter_name
        
        print '-Log Items:'

        for log_item in self.log_items:
            if log_item[0] == CritterTracker.LOG_ITEM_INTERACTION:
                our_action = log_item[3]
                their_action = log_item[5]
                their_name = log_item[4]
                iteration_no = log_item[1]
                our_food = log_item[6]
                
                if our_action == UNCOOPERATE and their_action == UNCOOPERATE:
                    outcome_description = 'had no interaction with'
                elif our_action == COOPERATE and their_action == COOPERATE:
                    outcome_description = 'cooperated with'
                elif our_action == COOPERATE:
                    outcome_description = 'was suckered by'
                else:
                    outcome_description = 'cheated'
                    
                print '%d:\t%s\t%d\t%d %d\t%s\t\t%s %s %s' % (iteration_no,
                                                        self.critter_name, 
                                                        our_food, 
                                                        our_action,
                                                        their_action, 
                                                        their_name, 
                                                        self.critter_name, 
                                                        outcome_description, 
                                                        their_name)
            
            elif log_item[0] == CritterTracker.LOG_ITEM_DEATH:
                print '%d:\tCritter %s has died' % (log_item[1],self.critter_name)
            elif log_item[0] == CritterTracker.LOG_ITEM_REPRODUCTION:
                print '%d:\tCritter %s begot critter %s' % (log_item[1], 
                                                            self.critter_name, 
                                                            log_item[2])
            else:
                print 'Unknown log item'
                
    def on_iteration_start(self, environment):
        self.iteration_no = environment.iteration_no
        
        if not self.attached and environment.population.has_key(self.critter_name):
            self.attach_to_critter(environment.population[self.critter_name])
             
    
    
    def on_interaction_end(self, environment, agent1, agent1_outcome, agent2, agent2_outcome):
        '''called at the end of an interaction between two agents'''
        
        log_item = None
        
        if agent1.name == self.critter_name:
            log_item = (CritterTracker.LOG_ITEM_INTERACTION,
                        environment.iteration_no, 
                        agent1.name,
                        agent1_outcome,
                        agent2.name,
                        agent2_outcome,
                        agent1.food)               
        elif agent2.name == self.critter_name:
            log_item = (CritterTracker.LOG_ITEM_INTERACTION,
                        environment.iteration_no,
                        agent2.name,
                        agent2_outcome,
                        agent1.name,
                        agent1_outcome,
                        agent2.food)               
        
        if log_item:    
            self.log_items.append(log_item)
        

    def receive_event(self, source, event, data):
        
        if event == critters.Critter.EVENT_DYING:
            self.log_items.append((CritterTracker.LOG_ITEM_DEATH, self.iteration_no))
        elif event == critters.Critter.EVENT_REPRODUCING:
            self.log_items.append((CritterTracker.LOG_ITEM_REPRODUCTION, 
                                   self.iteration_no, 
                                   data['offspring'].name))    
            
    def attach_to_critter(self, critter):
        ''' 
        Attach this critter tracker to a specific critter
        '''
        critter.add_listener(self, critters.Critter.EVENT_DYING)
        critter.add_listener(self, critters.Critter.EVENT_REPRODUCING)
        
        self.attached = True
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()    

