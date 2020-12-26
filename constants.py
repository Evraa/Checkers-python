
#board aspects
WIDTH, HEIGHT, SQR_SIZE = 720, 720, 30
N = 8
#max depth for tree
DEPTH = 1000
MIN_DEPTH = 6
#max and min winning costs
MAX_POS = pow(N,3)
MAX_NEG = -MAX_POS
#go greedy
GREEDY = True
#play against ai
AGAINST = True
#level of intelligence
TUNE = 5
#show some print outs
VERBOSE = False
#show board graphics
GFX = False
#prune
PRUNE = True
#show deeper print outs
VERBOSE_DEEP = False

def parse_constants (args):
    global N, GREEDY, AGAINST, TUNE, VERBOSE_DEEP, VERBOSE, GFX, PRUNE
    if args.board_size != None: N = int(args.board_size) 
    if args.greedy != None and args.greedy == 'True': GREEDY = True 
    if args.against != None and args.against == 'True': AGAINST = True
    if args.level != None:
        if args.level == 'too_easy':
            TUNE = 0.1
        elif args.level == 'easy':
            TUNE = 2
        elif args.level == 'normal':
            TUNE = 5
        elif args.level == 'hard':
            TUNE = 10
    if args.verbose != None and args.verbose == 'True': VERBOSE = True
    if args.verbose_deep != None and args.verbose_deep == 'True': VERBOSE_DEEP = True
    if args.gfx != None and args.gfx == 'True': GFX = True
    if args.prune != None and args.prune == 'True': PRUNE = True

    print (f'Game States are as follows: \n \
            Board Size: {N} \n \
            Greedy: {GREEDY} \n \
            Draw: {not GREEDY} \n \
            Against: {AGAINST} \n \
            Level: {args.level} \n \
            Prune: {PRUNE} \n \
            GFX: {GFX} \n \
            Verbose: {VERBOSE} \n \
            Verbose deep: {VERBOSE_DEEP} \n')
    
    
        