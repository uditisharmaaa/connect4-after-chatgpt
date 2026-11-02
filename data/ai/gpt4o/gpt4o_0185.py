import random

# Constants
COLS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
PLAYER_SYMBOLS = CHECKERS[:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def clear_screen():
    import os
    os.system('clear')

def is_valid_input(input_char):
    return input_char.isalpha() and 'A' <= input_char <= chr(65 + COLS - 1)

def place_checker(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            return True
    return False

def check_for_win(board, player_symbol):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] == player_symbol:
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
    
    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
    
    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True
    
    return False

def check_for_draw(board):
    return all(all(col != ' ' for col in row) for row in board)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    player_symbols = PLAYER_SYMBOLS
    clear_screen()
    print_board(board)

    while True:
        player_symbol = player_symbols[current_player]
        input_char = input(f"Player {player_symbol}, please enter a column: ").upper()
        
        while not is_valid_input(input_char):
            input_char = input(f"Invalid input. Player {player_symbol}, please enter a valid column: ").upper()
        
        column = ord(input_char) - 65
        
        if not place_checker(board, column, player_symbol):
            print(f"Column {input_char} is full. Player {player_symbol} you lose your turn.")
        else:
            clear_screen()
            print_board(board)
            if check_for_win(board, player_symbol):
                print(f"Player {player_symbol} won!")
                break
            if check_for_draw(board):
                print("The game is a draw!")
                break
        
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
