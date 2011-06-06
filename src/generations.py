#!/usr/bin/env python
'''
Created on May 15, 2011

@author: ben
'''
import sys, getopt, world, plugins

def main(argv):
    
    #defaults
    world_to_run = 'PrisonersDilemma'
    track_critter = None
    iterations = 600
    reporting_interval = 5
    filename = None
    
    try:
        opts, args = getopt.getopt(argv, 'ht:i:r:f:',['help','track=',
                                                    'iterations=',
                                                    'reporting=',
                                                    'filename='])
            
        for opt, arg in opts:
            if opt in ('-h','--help'):
                usage()
                sys.exit()
                
            elif opt in ('-t','--track'):
                track_critter = arg
            elif opt in ('-i','--iterations'):
                iterations = int(arg)
            elif opt in ('-r','--reporting'):
                reporting_interval = int(arg)
            elif opt in ('-f','--filename'):
                filename = arg
                
    except Exception, err:
        
        print('Error:')
        print(err)
        print('\n')
        usage()
        sys.exit(2)
            
    world_to_run = "".join(args) or world_to_run
    
    print "running world %s" % world_to_run
    
    xworld = instantiate_world(world_to_run)
    xworld.add_plugin(plugins.StrategyTabularReporter(reporting_interval,
                                                      filename))
    
    if track_critter:
        xworld.add_plugin(plugins.CritterTracker(track_critter))
    xworld.run(iterations) 
    
def usage():
    '''prints usage instructions'''
    print('generations.py')
    print('\nRun a simulated environment\n')
    print('Usage: generations.py [world]')
    print('options:')
    print('-h, --help\t\tThis help information')
    print('-i, --iterations\tNumber of iterations to run')
    print('-t, --track\t\ttrack a named critter')
    print('-r, --reporting\t\treporting interval in iterations')
    print('-f, --filename\t\toptional filename for tab-separated output')
    print('Written by Ben Davies (http://www.learningtechnicalstuff.com)')        

def instantiate_world(name_of_world):
    '''instantiates the named world (class = world.[name_of_world]World)'''
    return world.PrisonersDilemmaWorld()


if __name__ == '__main__':
    main(sys.argv[1:])
    

    
