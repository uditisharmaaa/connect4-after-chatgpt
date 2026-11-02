import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # This would be ['X', 'O', 'V', 'H', 'M'] for 5 players
EMPTY = ' '

def create_board():
    return [[EMPTY] * COLUMNS for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == EMPTY

def place_checker(column, player, board):
    for row in reversed(board):
        if row[column] == EMPTY:
            row[column] = player
            break

def check_for_win(player, board):
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == player and all(board[row][col + i] == player for i in range(4)):
                return True
    # Vertical Check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == player and all(board[row + i][col] == player for i in range(4)):
                return True
    # Diagonal Check (/)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == player and all(board[row + i][col + i] == player for i in range(4)):
                return True
    # Diagonal Check (\)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if board[row][col] == player and all(board[row + i][col - i] == player for i in range(4)):
                return True
    return False

def check_for_draw(board):
    return all(all(cell != EMPTY for cell in row) for row in board)

def next_player(current_player_index, total_players):
    return (current_player_index + 1) % total_players

def main():
    board = create_board()
    random_start = random.randint(0, len(PLAYERS) - 1)
    current_player_index = random_start
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        
        while True:
            try:
                column_input = input().strip().upper()
                column_choice = ord(column_input) - 65
                if not is_valid_column(column_choice, board):
                    print("Invalid column choice. Try again:")
                else:
                    break
            except (IndexError, ValueError):
                print("Invalid input. Enter a valid column letter:")
        
        place_checker(column_choice, current_player, board)
        print_board(board)
        
        if check_for_win(current_player, board):
            print(f"Player {current_player} won!")
            break
        
        if check_for_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = next_player(current_player_index, len(PLAYERS))

if __name__ == "__main__":
    main()
