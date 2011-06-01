#!/usr/bin/env python
'''
Created on May 15, 2011

@author: ben
'''
import sys, getopt, world, plugins

def main(argv):
    world_to_run = 'PrisonersDilemma'
    track_critter = None
    iterations = 15
    try:
        opts, args = getopt.getopt(argv, 'ht:i:','--help,--track,--iterations')
        
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage()
            sys.exit()
        elif opt in ('-t','--track'):
            track_critter = arg
        elif opt in ('-i','--iterations'):
            iterations = int(arg)
            
    world_to_run = "".join(args) or world_to_run
    
    print "running world %s" % world_to_run
    
    xworld = instantiate_world(world_to_run)
    xworld.add_plugin(plugins.StrategyTabularReporter())
    
    if track_critter:
        xworld.add_plugin(plugins.CritterTracker(track_critter))
    xworld.run(iterations) 
    
    

def usage():
    '''prints usage instructions'''
    print('Usage: main.py [world]')
    print('options:')
    print('-i,iterations\tNumber of iterations to run')
    print('-t,track\ttrack a named critter')        

def instantiate_world(name_of_world):
    '''instantiates the named world (class = world.[name_of_world]World)'''
    return world.PrisonersDilemmaWorld()


if __name__ == '__main__':
    main(sys.argv[1:])
    

    
