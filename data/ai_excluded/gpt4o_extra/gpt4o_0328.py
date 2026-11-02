import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # Use between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # Adjust depending on number of players
PLAYER_CHECKERS = CHECKERS[:PLAYERS]

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = " " + "   ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_labels)
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def is_valid_input(input, columns_list):
    return input in columns_list

def get_lowest_empty_row(board, column):
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == " ":
            return r
    return None

def place_checker(board, column, checker):
    row = get_lowest_empty_row(board, column)
    if row is not None:
        board[row][column] = checker
        return True
    return False

def check_winning_combination(board, checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True
    
    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == checker for i in range(4)):
                return True
    
    # Diagonal checks
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True
    
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLUMNS)
    print_board(board)
    
    first_player_index = random.randint(0, PLAYERS - 1)
    players = PLAYER_CHECKERS[first_player_index:] + PLAYER_CHECKERS[:first_player_index]
    
    column_labels = [chr(65 + i) for i in range(COLUMNS)]

    game_over = False
    turn_index = 0
    
    while not game_over:
        current_player = players[turn_index % PLAYERS]
        print(f"Player {current_player}, please enter a column:")
        column_choice = input().strip().upper()
        
        while not is_valid_input(column_choice, column_labels):
            print("Invalid input. Please enter a valid column:")
            column_choice = input().strip().upper()
        
        column_id = ord(column_choice) - 65

        if not place_checker(board, column_id, current_player):
            print("Column is full. You lose the turn.")
        else:
            print_board(board)
            if check_winning_combination(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
        
        turn_index += 1

if __name__ == "__main__":
    main()
