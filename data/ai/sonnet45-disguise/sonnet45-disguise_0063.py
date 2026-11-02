import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print board
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(" " + cell + " |", end="")
        print()
    print("+---" * COLS + "+")

def is_valid_move(board, col):
    if col < 0 or col >= COLS:
        return False
    if board[0][col] != " ":
        return False
    return True

def drop_checker(board, col, checker):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = checker
            return i
    return -1

def check_win(board, row, col, checker):
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    start_row = row
    start_col = col
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    
    count = 0
    while start_row < ROWS and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_row += 1
        start_col += 1
    
    # Check diagonal (bottom-left to top-right)
    start_row = row
    start_col = col
    while start_row < ROWS - 1 and start_col > 0:
        start_row += 1
        start_col -= 1
    
    count = 0
    while start_row >= 0 and start_col < COLS:
        if board[start_row][start_col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_row -= 1
        start_col += 1
    
    return False

def check_draw(board):
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_move(player_checker):
    while True:
        move = input("Player " + player_checker + ", please enter a column: ")
        
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        move = move.upper()
        col = ord(move) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Please try again.")
            continue
        
        return col

def main():
    board = create_board()
    players = []
    for i in range(NUM_PLAYERS):
        players.append(CHECKERS[i])
    
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        checker = players[current_player]
        
        col = get_player_move(checker)
        
        if not is_valid_move(board, col):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        row = drop_checker(board, col, checker)
        print_board(board)
        
        if check_win(board, row, col, checker):
            print("Player " + checker + " won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

main()
