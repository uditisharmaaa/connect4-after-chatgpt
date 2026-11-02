import os
import random

# Constant variables for board dimensions and number of players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2

# Players' checkers
player_checkers = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    column_labels = " ".join([chr(65 + i) for i in range(len(board[0]))])
    print(f"  {column_labels}")
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def check_valid_input(input, cols):
    return input.isalpha() and len(input) == 1 and 65 <= ord(input.upper()) < 65 + cols

def place_checker(board, col, player):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return True
    return False

def check_win(board, player):
    # Horizontal check
    for row in board:
        for col in range(len(row) - 3):
            if row[col:col+4] == [player] * 4:
                return True

    # Vertical check
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Diagonal checks
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

        for col in range(3, len(board[0])):
            if all(board[row+i][col-i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

def main():
    board = create_board(ROWS, COLUMNS)
    players = player_checkers[:NUM_PLAYERS]
    
    current_player = random.choice(players)
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        player_input = input().strip().upper()
        
        if not check_valid_input(player_input, COLUMNS):
            print("Invalid input, try again.")
            continue
        
        col_index = ord(player_input) - 65
        if not place_checker(board, col_index, current_player):
            print("Column full, turn lost.")
        else:
            print_board(board)
            
            if check_win(board, current_player):
                print(f"Player {current_player} won!")
                break
            
            if check_draw(board):
                print("The game is a draw!")
                break
        
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
