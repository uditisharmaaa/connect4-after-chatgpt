import random
import os

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = ' '.join(chr(65 + i) for i in range(COLUMNS))
    print(f"  {column_labels}")
    print('+' + '---+' * COLUMNS)
    for row in board:
        print('|' + ''.join(f" {cell} |" for cell in row))
        print('+' + '---+' * COLUMNS)

def is_valid_input(user_input):
    return user_input.isalpha() and len(user_input) == 1 and 'A' <= user_input <= chr(65 + COLUMNS - 1)

def get_valid_input():
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        if is_valid_input(user_input):
            return user_input
        print("Invalid input. Please enter a valid column letter.")

def drop_checker(board, column, player_checker):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_checker
            return True
    return False  # Column is full

def check_winner(board, player_checker):
    # Check horizontal, vertical and diagonal for four in a row with the player's checker
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (col <= COLUMNS - 4 and all(board[row][col + i] == player_checker for i in range(4)) or
                row <= ROWS - 4 and all(board[row + i][col] == player_checker for i in range(4)) or
                col <= COLUMNS - 4 and row <= ROWS - 4 and all(board[row + i][col + i] == player_checker for i in range(4)) or
                col >= 3 and row <= ROWS - 4 and all(board[row + i][col - i] == player_checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        player_checker = CHECKERS[current_player_index]
        print(f"Player {player_checker}, it's your turn.")
        
        while True:
            column_input = get_valid_input()
            column = ord(column_input) - 65
            if drop_checker(board, column, player_checker):
                break
            print(f"Column {column_input} is full. Choose another column.")
        
        print_board(board)
        
        if check_winner(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
