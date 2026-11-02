import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    headers = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # A, B, C...
    print(headers)
    print("+" + "---+" * len(board[0]))
    
    # Print rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def is_valid_column(column, board):
    if column < 0 or column >= len(board[0]):
        return False
    return board[0][column] == " "

def drop_checker(board, column, symbol):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = symbol
            return True
    return False

def check_for_win(board, symbol):
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] == symbol and board[r][c+1] == symbol and board[r][c+2] == symbol and board[r][c+3] == symbol:
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] == symbol and board[r+1][c] == symbol and board[r+2][c] == symbol and board[r+3][c] == symbol:
                return True

    # Check diagonal (top left to bottom right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] == symbol and board[r+1][c+1] == symbol and board[r+2][c+2] == symbol and board[r+3][c+3] == symbol:
                return True

    # Check diagonal (bottom left to top right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if board[r][c] == symbol and board[r-1][c+1] == symbol and board[r-2][c+2] == symbol and board[r-3][c+3] == symbol:
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def get_player_input(player_symbols, current_player, board):
    while True:
        player_input = input(f"Player {player_symbols[current_player]}, please enter a column: ").strip().upper()
        if len(player_input) != 1 or not player_input.isalpha():
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        column = ord(player_input) - ord('A')
        if not is_valid_column(column, board):
            print("Invalid move. Column is either full or out of range.")
            continue
        
        return column

def main():
    clear_screen()
    # Initialize game settings
    num_players = 2  # Set to a constant for this assignment
    player_symbols = PLAYER_SYMBOLS[:num_players]
    board = create_board(BOARD_ROWS, BOARD_COLUMNS)
    
    # Randomly select first player
    current_player = random.randint(0, num_players - 1)
    
    # Main game loop
    while True:
        clear_screen()
        print_board(board)
        column = get_player_input(player_symbols, current_player, board)
        
        drop_checker(board, column, player_symbols[current_player])
        
        if check_for_win(board, player_symbols[current_player]):
            clear_screen()
            print_board(board)
            print(f"Player {player_symbols[current_player]} won!")
            break
        
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
