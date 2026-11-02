import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(i) for i in range(65, 65 + COLUMNS)))  # Column labels A-G
    print("+---" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "---+" * COLUMNS)

def get_valid_input(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").upper()
        if len(column) == 1 and 65 <= ord(column) < 65 + COLUMNS:  # A-G
            return ord(column) - 65
        print("Invalid input. Please enter a valid column letter (A-G).")

def place_checker(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player
            return (row, col)
    return None  # Column is full

def check_winner(board, player):
    # Check horizontal, vertical and diagonal matches
    for row in range(ROWS):
        for col in range(COLUMNS):
            if check_direction(board, row, col, player, 1, 0) or \
               check_direction(board, row, col, player, 0, 1) or \
               check_direction(board, row, col, player, 1, 1) or \
               check_direction(board, row, col, player, 1, -1):
                return True
    return False

def check_direction(board, row, col, player, delta_row, delta_col):
    count = 0
    for i in range(4):  # Check for 4 in a row
        r = row + i * delta_row
        c = col + i * delta_col
        if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
            count += 1
        else:
            break
    return count == 4

def check_draw(board):
    return all(board[0][col] != " " for col in range(COLUMNS))

def main():
    board = create_board()
    num_players = min(MAX_PLAYERS, 2) # Set to 2 players for submission
    players = PLAYERS[:num_players]
    turn = random.randint(0, num_players - 1)  # Randomly choose the first player

    print_board(board)

    while True:
        current_player = players[turn]
        col = get_valid_input(current_player)
        position = place_checker(board, col, current_player)

        if position is not None:
            print_board(board)

            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break

            if check_draw(board):
                print("The game is a draw!")
                break

            turn = (turn + 1) % num_players  # Switch to the next player
        else:
            print("Column is full. Try a different column.")

if __name__ == "__main__":
    main()
