import sys

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python bricks.py <num_bricks>"
    sys.exit(0)

# get the starting number of bricks
bricks = int(sys.argv[1])

# ------- create the  code ----------- #

linebreak = lambda a,b: a+"\n"+b

# module declaration and variable declaration
main = """MODULE main
VAR
    bricks : 0..{0}; 
    i : 1..3;
    j : 1..3;
    turn : boolean;
    winner : {{none, a, b}};
ASSIGN""".format(bricks)

#TODO the initialization of variables
init= reduce(linebreak, ["    init(bricks):= {0};".format(bricks),
	"    init(turn):= TRUE;","    init(winner):= none;"])

#TODO transitions
next_bricks = reduce(linebreak, [
	"    next(bricks):= case",
	"        bricks - i - j > 0 : bricks - i - j;",
	"        bricks - i - j <= 0 : 0;",
	"        esac;"])
# turn represents "it's player A's turn to take bricks"
next_turn = reduce(linebreak, [
	"    next(turn):= case", 
	"        turn : FALSE;",
	"        !turn : TRUE;", 
	"        esac;"])
next_winner = reduce(linebreak, [
	"    next(winner):= case", 
	"        turn=TRUE &  bricks=0 : a;",
	"        turn=FALSE & bricks=0 : b;",
	"        TRUE: winner;"
	"        esac;"])
next = reduce (linebreak, [next_turn, next_bricks, next_winner])


#TODO the specifications 
spec = "SPEC AF (winner = a | winner = b)"

# put it all together
print reduce(linebreak, [main,init,next,spec])

