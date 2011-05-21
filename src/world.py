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
        
    def run(self):
        '''
        Runs the world with the configuration provided
        '''
        return 0
    
    
class  PrisonersDilemmaWorld(World):
    '''
    creates a world with critters using different strategies to determine what 
    happens when they interact; Do they cooperate or not? Based on their mutual 
    decisions they are provided food
    '''
    
    def run(self):
        '''
        executes the world
        >>> world = PrisonersDilemmaWorld()
        >>> world.run() # doctest:+ELLIPSIS
        Critter_...Critter_...
        1:...0...200
        2:...0...400
        ...
        simulation complete.
        '''
        NUMBER_OF_ITERATIONS = 15
        
        #create critter population
        sucker = critters.Critter(critters.SuckerStrategy())
        cheater = critters.Critter(critters.CheatStrategy())
        population = (sucker, cheater)
        
        
        #write headers
        print('%s\t%s' %(population[0].name, population[1].name))
        
        #execute iterations
        for i in range(1,NUMBER_OF_ITERATIONS + 1):
            self.run_iteration(population)
            print('%d:\t%d\t%d' % 
                  (i,population[0].food,population[1].food))
        
        #finish simulation
        print('simulation complete.')

    def run_iteration(self, population):
        '''
        runs a single iteration for population. The population itself is updated
        in the course of the exection. A population is a list of critters
        >>> world = PrisonersDilemmaWorld()
        >>> c1 = critters.Critter(critters.CheatStrategy())
        >>> c2 = critters.Critter(critters.CheatStrategy())
        >>> population = (c1,c2)
        >>> world.run_iteration(population)
        >>> population[1].food
        0

        '''
        
        interaction_list = \
            [(c1,c2) for c1 in population for c2 in population if c1 < c2]
        
        for c1, c2 in interaction_list:
            self.interact_critters(c1,c2)


    def interact_critters(self, critter1, critter2):
        '''
        executes an interaction between 2 critters. Based on their own 
        response to the interaction, each is rewarded food (or not) based on 
        their response
        >>> world = PrisonersDilemmaWorld()
        >>> c1 = critters.Critter(critters.CheatStrategy())
        >>> c2 = critters.Critter(critters.CheatStrategy())
        >>> world.interact_critters(c1,c2)
        '''
        COOPERATE_FOOD = 100
        CHEATER_FOOD = 200
        SUCKER_FOOD = 0
        
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

if __name__ == '__main__':
    import doctest
    doctest.testmod()    
