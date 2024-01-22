"""
Course: Python for Scientists (Part-I)
"""


# %%
def author():
    '''
    return your name
    '''
    return 'Fnu Obi'


# %%
import random
import copy


# %%
def DrawBoard(Board):
    '''
    Parameter: Board is a 3x3 matrix (a nested list).
    Return: None
    Description: this function prints the chess board
    hint: Board[i][j] is ' ' or 'X' or 'O' in row-i and col-j
          use print function
    '''
    for i in range(len(Board)):
        print('|'.join(Board[i]))
        if i != len(Board) - 1:
            print('-+-+-')
    print()


# %%
def IsSpaceFree(Board, i, j):
    '''
    Parameters: Board is the game board, a 3x3 matrix
                i is the row index, j is the col index
    Return: True or False
    Description:
        (1) return True  if Board[i][j] is empty (' ')
        (2) return False if Board[i][j] is not empty
        (3) return False if i or j is invalid (e.g. i = -1 or 100)
        think about the order of (1) (2) (3)
    '''
    validRowsCols = (0, 1, 2)  # tuple to hold the valid inputs for rows and columns
    if i not in validRowsCols or j not in validRowsCols:
        return False
    elif Board[i][j] == ' ':
        return True
    else:
        return False


# %%
def GetNumberOfChessPieces(Board):
    '''
    Parameter: Board is the game board, a 3x3 matrix
    Return: the number of chess piceces on Board
            i.e. the total number of 'X' and 'O'
    hint: define a counter and use a nested for loop, like this
          for i in 0 to 3
              for j in 0 to 3
                  add one to the counter if Board[i][j] is not empty
    '''
    totalPieces = 0
    for i in range(3):
        for j in range(3):
            if Board[i][j] != ' ':
                totalPieces += 1
    return totalPieces


# %%
def IsBoardFull(Board):
    '''
    Parameter: Board is the game board, a 3x3 matrix
    Return: True or False
    Description:
        return True if the Board is fully occupied
        return False otherwise
    hint: use GetNumberOfChessPieces
    '''
    if GetNumberOfChessPieces(Board) == 9:
        return True
    return False


# %%
def IsBoardEmpty(Board):
    '''
    Parameter: Board is the game board, a 3x3 matrix
    Return: True or False
    Description:
        return True if the Board is empty
        return False otherwise
    hint: use GetNumberOfChessPieces
    '''
    if GetNumberOfChessPieces(Board) == 0:
        return True
    return False


# %%
def UpdateBoard(Board, Tag, Choice):
    '''
    Parameters:
        Board is the game board, a 3x3 matrix
        Tag is 'O' or 'X'
        Choice is a tuple (row, col) from HumanPlayer or ComputerPlayer
    Return: None
    Description:
         Update the Board after a player makes a choice
         Set an element of the Board to Tag at the location (row, col)
    '''
    i, j = Choice
    if IsSpaceFree(Board, i, j):
        Board[i][j] = Tag


# %%
def HumanPlayer(Tag, Board):
    '''
    Parameters:
        Tag is 'X' or 'O'. If Tag is 'X': HumanPlayer is PlayerX who goes first
        Board is the game board, a 3x3 matrix
    Return: ChoiceOfHumanPlayer, it is a tuple (row, col)
    Description:
        This function will NOT return until it gets a valid input from the user
    Attention:
        Board is NOT modified in this function
    hint:
        a while loop is needed, see HumanPlayer in rock-papper-scissors
        the user needs to input row-index and col-index, where a new chess will be placed
        use int() to convert string to int
        use try-except to handle exceptions if the user inputs some random string
        if (row, col) has been occupied, then ask the user to choose another spot
        if (row, col) is invalid, then ask the user to choose a valid spot
    '''
    ChoiceOfHumanPlayer = None

    while ChoiceOfHumanPlayer is None:
        try:
            print('make your choice\n')
            row = int(input('row = '))
            col = int(input('\ncol = '))

            while not IsSpaceFree(Board, row, col):
                print('Oops! That is not a valid spot. Try again...')
                print('make your choice\n')
                row = int(input('row = '))
                col = int(input('\ncol = '))

            ChoiceOfHumanPlayer = (row, col)
        except:
            print('Oops! That is not valid number. Try again...')

    print(f'HumanPlayer({Tag}) has made the choice')
    return ChoiceOfHumanPlayer


# %%
def ComputerPlayer(Tag, Board, N=1):
    '''
    Parameters:
        Tag is 'X' or 'O'. If Tag is 'X': ComputerPlayer is PlayerX who goes first
        Board is the game board, a 3x3 matrix
        N: think N steps ahead, default N=1
    Return: ChoiceOfComputerPlayer, it is a tuple (row, col)
    Description:
        ComputerPlayer will choose an empty spot on the board
        a random strategy in a while loop:
            (1) randomly choose a spot on the Board
            (2) if the spot is empty then return the choice (row, col)
            (3) if the spot is not empty then go to (1)
    Attention:
        Board is NOT modified in this function
    '''
    ChoiceOfComputerPlayer = None

    # Chooses a corner if board is empty
    if IsBoardEmpty(Board):
        corners = ((0, 0), (0, 2), (2, 0), (2, 2))
        ChoiceOfComputerPlayer = random.choice(corners)

        return ChoiceOfComputerPlayer

    # Dictionary for possible outcomes
    outcome = {0: 'in progress',
               1: 'X',
               2: '0',
               3: 'tie'}

    # Assigns the tag for human player
    if Tag == 'X':
        opposite_tag = 'O'
    else:
        opposite_tag = 'X'

    # Checks for a spot where computer wins
    for row in range(3):
        for col in range(3):
            if IsSpaceFree(Board, row, col):
                choice = (row, col)
                new_board = copy.deepcopy(Board)
                UpdateBoard(new_board, Tag, choice)
                result = Judge(new_board)

                if outcome[result] == Tag:
                    ChoiceOfComputerPlayer = choice

                    return ChoiceOfComputerPlayer

    # Checks for a spot where human player wins inorder to take that stops
    for row in range(3):
        for col in range(3):
            if IsSpaceFree(Board, row, col):
                choice = (row, col)
                new_board = copy.deepcopy(Board)
                UpdateBoard(new_board, opposite_tag, choice)
                result = Judge(new_board)

                if outcome[result] == opposite_tag:
                    ChoiceOfComputerPlayer = choice

                    return ChoiceOfComputerPlayer

    # Chooses a spot randomly
    while ChoiceOfComputerPlayer is None:
        row, col = random.randint(0, 2), random.randint(0, 2)

        if IsSpaceFree(Board, row, col):
            ChoiceOfComputerPlayer = (row, col)

    print(f'ComputerPlayer({Tag}) has made the choice')
    return ChoiceOfComputerPlayer


# Minimax function scores the most optimal moves
def Minimax(board, depth, is_maximizing):
    scores = {
        1: 1,
        2: -1,
        3: 0
    }

    result = Judge(board)
    if result != 0:
        return scores[result]

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = Minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = Minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score
    

# Enhanced computer layer
def ComputerPlayerEnhanced(Tag, Board):
    if IsBoardEmpty(Board):
        corners = ((0, 0), (0, 2), (2, 0), (2, 2))
        print(f'ComputerPlayer({Tag}) has made the choice')
        return random.choice(corners)

    best_score = -float("inf")
    best_move = None
    for i in range(3):
        for j in range(3):
            if Board[i][j] == ' ':
                Board[i][j] = 'X'
                score = Minimax(Board, 0, False)
                Board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    print(f'ComputerPlayer({Tag}) has made the choice')
    return best_move




# %%
def Judge(Board):
    '''
    Parameter:
         Board is the current game board, a 3x3 matrix
    Return: Outcome, an integer
        Outcome is 0 if the game is still in progress
        Outcome is 1 if player X wins
        Outcome is 2 if player O wins
        Outcome is 3 if it is a tie (no winner)
    Description:
        this funtion determines the Outcome of the game
    hint:
        (1) check if anyone wins, i.e., three 'X' or 'O' in
            top row, middle row, bottom row
            lef col, middle col, right col
            two diagonals
            use a if-statment to check if three 'X'/'O' in a row
        (2) if no one wins, then check if it is a tie
            note: if the board is fully occupied, then it is a tie
        (3) otherwise, the game is still in progress
    '''
    # Check rows for X or O win
    for row in range(3):
        if Board[row][0] == Board[row][1] and Board[row][1] == Board[row][2]:
            if Board[row][0] == 'X':
                return 1
            elif Board[row][0] == 'O':
                return 2

    # Check columns for X or O win
    for col in range(3):
        if Board[0][col] == Board[1][col] and Board[1][col] == Board[2][col]:
            if Board[0][col] == 'X':
                return 1
            elif Board[0][col] == 'O':
                return 2

    # Check left diagonal for X or O win
    if Board[0][0] == Board[1][1] and Board[1][1] == Board[2][2]:
        if Board[0][0] == 'X':
            return 1
        elif Board[0][0] == 'O':
            return 2

    # Check right diagonal for X or O win
    if Board[0][2] == Board[1][1] and Board[1][1] == Board[2][0]:
        if Board[0][2] == 'X':
            return 1
        elif Board[0][2] == 'O':
            return 2

    # Check if game is tie
    if IsBoardFull(Board):
        return 3

    return 0


# %%
def ShowOutcome(Outcome, NameX, NameO):
    '''
    Parameters:
        Outcome is from Judge
        NameX is the name of PlayerX who goes first at the beginning
        NameO is the name of PlayerO
    Return: None
    Description:
        print a meassage about the Outcome
        NameX/NameO may be 'human' or 'computer'
    hint: the message could be
        PlayerX (NameX, X) wins
        PlayerO (NameO, O) wins
        the game is still in progress
        it is a tie
    '''
    if Outcome == 1:
        print(f'PlayerX ({NameX}, X) wins')
    elif Outcome == 2:
        print(f'PlayerO ({NameO}, O) wins')
    elif Outcome == 3:
        print('it is a tie')
    else:
        print('the game is still in progress')


# %% read but do not modify this function
def Which_Player_goes_first():
    '''
    Parameter: None
    Return: two function objects: PlayerX, PlayerO
    Description:
        Randomly choose which player goes first.
        PlayerX/PlayerO is ComputerPlayer or HumanPlayer
    '''
    if random.randint(0, 1) == 0:
        print("Computer player goes first")
        PlayerX = ComputerPlayerEnhanced
        PlayerO = HumanPlayer
    else:
        print("Human player goes first")
        PlayerO = ComputerPlayerEnhanced
        PlayerX = HumanPlayer
    return PlayerX, PlayerO


# %% the game
def TicTacToeGame():
    # ---------------------------------------------------
    print("Wellcome to Tic Tac Toe Game")
    Board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    DrawBoard(Board)
    # determine the order
    PlayerX, PlayerO = Which_Player_goes_first()
    # get the name of each function object
    NameX = PlayerX.__name__
    NameO = PlayerO.__name__
    # ---------------------------------------------------
    # suggested steps in a while loop:
    # (1)  get a choice from PlayerX, e.g. ChoiceX=PlayerX('X', Board)
    # (2)  update the Board
    # (3)  draw the Board
    # (4)  get the outcome from Judge
    # (5)  show the outcome
    # (6)  if the game is completed (win or tie), then break the loop
    # (7)  get a choice from PlayerO
    # (8)  update the Board
    # (9)  draw the Board
    # (10) get the outcome from Judge
    # (11) show the outcome
    # (12) if the game is completed (win or tie), then break the loop
    # ---------------------------------------------------
    # your code starts from here
    while True:
        ChoiceX = PlayerX('X', Board)
        UpdateBoard(Board, 'X', ChoiceX)
        DrawBoard(Board)
        outcome = Judge(Board)
        ShowOutcome(outcome, NameX, NameO)

        if outcome != 0:
            break

        ChoiceO = PlayerO('O', Board)
        UpdateBoard(Board, 'O', ChoiceO)
        DrawBoard(Board)
        outcome = Judge(Board)
        ShowOutcome(outcome, NameX, NameO)

        if outcome != 0:
            break


# %% play the game many rounds until the user wants to quit
# read but do not modify this function
def PlayGame():
    while True:
        TicTacToeGame()
        print('Do you want to play again? (yes or no)')
        if not input().lower().startswith('y'):
            break
    print("GameOver")


# %% do not modify anything below
if __name__ == '__main__':
    PlayGame()
