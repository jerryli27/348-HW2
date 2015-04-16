# File: Player.py
# Author(s) names AND netid's:
# Date: 
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    node_expanded=0;
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply
        self.node_expanded=0
    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Evaluate the Mancala board for this player """
        if board.hasWon(self.num):
            return INFINITY
        elif board.hasWon(self.opp):
            return -INFINITY
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        totalScore=-INFINITY
        if self.num==1:
            cupsIndex=0
            for i in board.P1Cups[0:5]:
                freeMove=0;opponent=0;capture=0;beCaptured=0;
                if (i==6-cupsIndex):
                    freeMove=1 #whether player earns a free move
                opponent=max(0,i+cupsIndex-6) #number of pieces given to opponent
                #calculate how much can a move capture 
                if i+cupsIndex<=5 and i>0 and board.P1Cups[cupsIndex+i]==0:
                    capture=1+board.P2Cups[5-(i+cupsIndex)]
                elif i+cupsIndex>=13 and i<14 and (board.P1Cups[cupsIndex+i-13]==0 or i==13):
                    capture=2+board.P2Cups[18-(i+cupsIndex)]
                    opponent+=5
                
                index2=0
                for j in board.P2Cups[0:5]:
                    if j+index2<=5 and j>0 and board.P2Cups[j+index2]==0:
                        beCaptured=1+board.P1Cups[5-(j+index2)]
                    elif j+index2>=13 and j<14 and (board.P2Cups[index2+j-13]==0 or j==13):
                        beCaptured=2+board.P1Cups[18-(j+index2)]
                    index2+=1
                cupsIndex+=1
                totalScore=max(totalScore,1*(board.scoreCups[0]-board.scoreCups[1])+2*freeMove+(-0.8)*opponent+1.5*capture+(-1.5)*beCaptured)        
        elif self.num==2:
            cupsIndex=0
            for i in board.P2Cups[0:5]:
                freeMove=0;opponent=0;capture=0;beCaptured=0;
                if (i==6-cupsIndex):
                    freeMove=1 #whether player earns a free move
                opponent=max(0,i+cupsIndex-6) #number of pieces given to opponent
                #calculate how much can a move capture 
                if i+cupsIndex<=5 and i>0 and board.P2Cups[cupsIndex+i]==0:
                    capture=1+board.P1Cups[5-(i+cupsIndex)]
                elif i+cupsIndex>=13 and i<14 and (board.P2Cups[cupsIndex+i-13]==0 or i==13):
                    capture=2+board.P1Cups[18-(i+cupsIndex)]
                    opponent+=5
        
                index2=0
                for j in board.P1Cups[0:5]:
                    if j+index2<=5 and j>0 and board.P1Cups[j+index2]==0:
                        beCaptured=1+board.P2Cups[5-(j+index2)]
                    elif j+index2>=13 and j<14 and (board.P1Cups[index2+j-13]==0 or j==13):
                        beCaptured=2+board.P2Cups[18-(j+index2)]
                    index2+=1
                cupsIndex+=1
                totalScore=max(totalScore,1*(board.scoreCups[1]-board.scoreCups[0])+2*freeMove+(-0.8)*opponent+1.5*capture+(-1.5)*beCaptured)
                #totalScore+=board.scoreCups[0]-board.scoreCups[1]
        return totalScore


    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.

    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.betaValue(nb, ply-1, turn, score)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        if move==-1:
            move=board.legalMoves(self)[0]
        return score, move

    def alphaValue(self, board, ply, turn, upperBound):
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.betaValue(nextBoard, ply-1, turn, score)
            #print "s in maxValue is: " + str(s)
            if s >= upperBound:
                return s
            elif s > score:
                score = s
        return score

    def betaValue(self, board, ply, turn, lowerBound):
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.alphaValue(nextBoard, ply-1, turn, score)
            #print "s in minValue is: " + str(s)
            if s <= lowerBound:
                return s
            elif s < score:
                score = s
        return score

                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "Player ",self.num, " chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.

            print "Custom player not yet implemented"
            return -1
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class jlt709(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """
    def __init__(self, playerNum, playerType, ply=5,parameterFreeMove=2,parameterOpponent=-0.8,parameterCapture=1.5,parameterBeCaptured=-1.5):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply
        self.node_expanded=0
        self.parameterFreeMove=parameterFreeMove
        self.parameterOpponent=parameterOpponent
        self.parameterCapture=parameterCapture
        self.parameterBeCaptured=parameterBeCaptured
    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
    def chooseMove(self, board):
        val,move=self.alphaBetaMove(board,self.ply)
        print "Player ",self.num, " chose move", move, " with value", val
        return move
# The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Evaluate the Mancala board for this player """
        if board.hasWon(self.num):
            return INFINITY
        elif board.hasWon(self.opp):
            return -INFINITY
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        totalScore=-INFINITY
        if self.num==1:
            cupsIndex=0
            for i in board.P1Cups[0:5]:
                freeMove=0;opponent=0;capture=0;beCaptured=0;
                if (i==6-cupsIndex):
                    freeMove=1 #whether player earns a free move
                opponent=max(0,i+cupsIndex-6) #number of pieces given to opponent
                #calculate how much can a move capture
                if i+cupsIndex<=5 and i>0 and board.P1Cups[cupsIndex+i]==0:
                    capture=1+board.P2Cups[5-(i+cupsIndex)]
                elif i+cupsIndex>=13 and i<14 and (board.P1Cups[cupsIndex+i-13]==0 or i==13):
                    capture=2+board.P2Cups[18-(i+cupsIndex)]
                    opponent+=5

                index2=0
                for j in board.P2Cups[0:5]:
                    if j+index2<=5 and j>0 and board.P2Cups[j+index2]==0:
                        beCaptured=1+board.P1Cups[5-(j+index2)]
                    elif j+index2>=13 and j<14 and (board.P2Cups[index2+j-13]==0 or j==13):
                        beCaptured=2+board.P1Cups[18-(j+index2)]
                    index2+=1
                cupsIndex+=1
                totalScore=max(totalScore,1*(board.scoreCups[0]-board.scoreCups[1])+self.parameterFreeMove*freeMove+self.parameterOpponent*opponent+self.parameterCapture*capture+self.parameterBeCaptured*beCaptured)
        elif self.num==2:
            cupsIndex=0
            for i in board.P2Cups[0:5]:
                freeMove=0;opponent=0;capture=0;beCaptured=0;
                if (i==6-cupsIndex):
                    freeMove=1 #whether player earns a free move
                opponent=max(0,i+cupsIndex-6) #number of pieces given to opponent
                #calculate how much can a move capture
                if i+cupsIndex<=5 and i>0 and board.P2Cups[cupsIndex+i]==0:
                    capture=1+board.P1Cups[5-(i+cupsIndex)]
                elif i+cupsIndex>=13 and i<14 and (board.P2Cups[cupsIndex+i-13]==0 or i==13):
                    capture=2+board.P1Cups[18-(i+cupsIndex)]
                    opponent+=5

                index2=0
                for j in board.P1Cups[0:5]:
                    if j+index2<=5 and j>0 and board.P1Cups[j+index2]==0:
                        beCaptured=1+board.P2Cups[5-(j+index2)]
                    elif j+index2>=13 and j<14 and (board.P1Cups[index2+j-13]==0 or j==13):
                        beCaptured=2+board.P2Cups[18-(j+index2)]
                    index2+=1
                cupsIndex+=1
                totalScore=max(totalScore,1*(board.scoreCups[1]-board.scoreCups[0])+self.parameterFreeMove*freeMove+self.parameterOpponent*opponent+self.parameterCapture*capture+self.parameterBeCaptured*beCaptured)
                #totalScore+=board.scoreCups[0]-board.scoreCups[1]
        return totalScore


    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.

    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY

        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = jlt709(self.opp, self.type, self.ply)
            s = opp.betaValue(nb, ply-1, turn, -INFINITY, INFINITY)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        if move==-1:
            move=board.legalMoves(self)[0]
        return score, move

    def alphaValue(self, board, ply, turn, lowerBound,upperBound):
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = jlt709(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            if nextBoard.makeMove(self, m)==True:
                s=self.alphaValue(nextBoard, ply-1, turn, lowerBound,upperBound)
            else:
                s = opponent.betaValue(nextBoard, ply-1, turn, lowerBound,upperBound)
            #print "s in maxValue is: " + str(s)
            score=max(score,s)
            lowerBound=max(lowerBound,score)
            if upperBound<=lowerBound:
                return score
        return score

    def betaValue(self, board, ply, turn, lowerBound,upperBound):
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = jlt709(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            if nextBoard.makeMove(self, m)==True:
                s=self.betaValue(nextBoard, ply-1, turn, lowerBound,upperBound)
            else:
                s = opponent.alphaValue(nextBoard, ply-1, turn, lowerBound,upperBound)
            score=min(score,s)
            #print "s in minValue is: " + str(s)
            upperBound=min(upperBound,score)
            if upperBound<=lowerBound:
                return score
        return score
