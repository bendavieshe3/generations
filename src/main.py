#!/usr/bin/env python
'''
Created on May 15, 2011

@author: ben
'''
import sys, getopt

def main(argv):
    name = 'world'
    try:
        opts, args = getopt.getopt(argv, 'h','--help')
        
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage()
            sys.exit()
    name = "".join(args) or name
    print "Hello, %s" % name
       

def usage():
    '''prints usage instructions'''
    print('Usage: main.py [name]')        

if __name__ == '__main__':
    main(sys.argv[1:])
    
    
