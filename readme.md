## Requirements:
    + pip install graphics
    + pip install numpy

## How To Run
    + python main.py
        -n : int the board size you want                ~REQUIRED   ~Def: 8
        -g : True -> go greedy, False: Propose Draw                 ~Def: False
        -ag: True -> play against AI                                ~Def: False
        -l: the level of difficulty ['too_easy', 'easy', 'normal', 'hard'] ~REQUIRED  ~Def: normal
        -v: Verbose, for information                                ~Def: False
        -gfx: graphics interface, click the mouse to proceed        ~Def: False
        -p: Prune                                       ~REQUIRED   ~Def: True
        -vd: verbose deeper, to show more info                      ~Def: False

    +Example:
        python main.py -n 4 -ag False  -l hard -gfx True -p True 

