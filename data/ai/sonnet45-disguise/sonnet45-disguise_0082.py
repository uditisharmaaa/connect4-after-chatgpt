import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2

# Create empty board
def create_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board

# Print the board
def print_board(board):
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(COLS):
        print(chr(65 + i) + "   ", end="")
    print()
    
    # Print rows
    for i in range(ROWS):
        print("+---" * COLS + "+")
        print("| ", end="")
        for j in range(COLS):
            print(board[i][j] + " | ", end="")
        print()
    print("+---" * COLS + "+")

# Get player symbols
def get_player_symbols(num_players):
    symbols = ["X", "O", "V", "H", "M"]
    return symbols[:num_players]

# Drop checker in column
def drop_checker(board, col, symbol):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == " ":
            board[i][col] = symbol
            return True
    return False

# Check if column is valid and not full
def is_valid_column(board, col):
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

# Check for horizontal win
def check_horizontal(board, symbol):
    for i in range(ROWS):
        for j in range(COLS - 3):
            if board[i][j] == symbol and board[i][j+1] == symbol and board[i][j+2] == symbol and board[i][j+3] == symbol:
                return True
    return False

# Check for vertical win
def check_vertical(board, symbol):
    for i in range(ROWS - 3):
        for j in range(COLS):
            if board[i][j] == symbol and board[i+1][j] == symbol and board[i+2][j] == symbol and board[i+3][j] == symbol:
                return True
    return False

# Check for diagonal win (down-right)
def check_diagonal1(board, symbol):
    for i in range(ROWS - 3):
        for j in range(COLS - 3):
            if board[i][j] == symbol and board[i+1][j+1] == symbol and board[i+2][j+2] == symbol and board[i+3][j+3] == symbol:
                return True
    return False

# Check for diagonal win (down-left)
def check_diagonal2(board, symbol):
    for i in range(ROWS - 3):
        for j in range(3, COLS):
            if board[i][j] == symbol and board[i+1][j-1] == symbol and board[i+2][j-2] == symbol and board[i+3][j-3] == symbol:
                return True
    return False

# Check if player won
def check_win(board, symbol):
    if check_horizontal(board, symbol):
        return True
    if check_vertical(board, symbol):
        return True
    if check_diagonal1(board, symbol):
        return True
    if check_diagonal2(board, symbol):
        return True
    return False

# Check if board is full
def is_board_full(board):
    for j in range(COLS):
        if board[0][j] == " ":
            return False
    return True

# Main game
def play_game():
    board = create_board()
    players = get_player_symbols(NUM_PLAYERS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    game_over = False
    while not game_over:
        symbol = players[current_player]
        print("Player " + symbol + ", please enter a column: ", end="")
        user_input = input()
        
        # Validate input
        if len(user_input) != 1:
            print("Invalid input. Try again.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Try again.")
            continue
        
        user_input = user_input.upper()
        col = ord(user_input) - 65
        
        if col < 0 or col >= COLS:
            print("Invalid column. Try again.")
            continue
        
        if not is_valid_column(board, col):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        # Drop checker
        drop_checker(board, col, symbol)
        print_board(board)
        
        # Check for win
        if check_win(board, symbol):
            print("Player " + symbol + " won!")
            game_over = True
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % NUM_PLAYERS

play_game()
