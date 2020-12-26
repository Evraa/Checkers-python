import constants
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--board_size", required=True)
    parser.add_argument("-g", "--greedy", required=False)
    parser.add_argument("-ag", "--against", required=False)
    parser.add_argument("-l", "--level", required=True)
    parser.add_argument("-v", "--verbose", required=False)
    parser.add_argument("-gfx", "--gfx", required=False)
    parser.add_argument("-p", "--prune", required=True)
    parser.add_argument("-vd", "--verbose_deep", required=False)    
    args = parser.parse_args()
    
    if args.board_size != None: constants.N = int(args.board_size) 
    if args.greedy != None and args.greedy == 'True': constants.GREEDY = True 
    if args.against != None and args.against == 'True': constants.AGAINST = True
    if args.level != None:
        if args.level == 'too_easy':
            constants.TUNE = 0.1
        elif args.level == 'easy':
            constants.TUNE = 2
        elif args.level == 'normal':
            constants.TUNE = 5
        elif args.level == 'hard':
            constants.TUNE = 10
    if args.verbose != None and args.verbose == 'True': constants.VERBOSE = True
    if args.verbose_deep != None and args.verbose_deep == 'True': constants.VERBOSE_DEEP = True
    if args.gfx != None and args.gfx == 'True': constants.GFX = True
    if args.prune != None and args.prune == 'False': constants.PRUNE = False
    
    print (f'Game States are as follows: \n \
            Board Size: {constants.N} \n \
            Greedy: {constants.GREEDY} \n \
            Draw: {not constants.GREEDY} \n \
            Against: {constants.AGAINST} \n \
            Level: {args.level} \n \
            Prune: {constants.PRUNE} \n \
            GFX: {constants.GFX} \n \
            Verbose: {constants.VERBOSE} \n \
            Verbose deep: {constants.VERBOSE_DEEP} \n')
    
    input ("If you want to continue press any key, otherwise press ctrl+c and repeat")
    from solve import main

    main()
    