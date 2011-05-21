#!/usr/bin/env python
'''
Created on May 15, 2011

@author: ben
'''
import sys, getopt, world

def main(argv):
    world_to_run = 'PrisonersDilemma'
    try:
        opts, args = getopt.getopt(argv, 'h','--help')
        
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage()
            sys.exit()
    world_to_run = "".join(args) or world_to_run
    
    print "running world %s" % world_to_run
    
    instantiate_world(world_to_run).run()
    

def usage():
    '''prints usage instructions'''
    print('Usage: main.py [world]')        

def instantiate_world(name_of_world):
    '''instantiates the named world (class = world.[name_of_world]World)'''
    return world.PrisonersDilemmaWorld()


if __name__ == '__main__':
    main(sys.argv[1:])
    

    
