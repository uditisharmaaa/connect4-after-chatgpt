import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')  # Clear screen

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    letters = [chr(i) for i in range(ord('A'), ord('A') + COLUMNS)]
    print("  " + "   ".join(letters))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column, board):
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == " "

def get_column_from_input(input_letter):
    if len(input_letter) != 1 or not input_letter.isalpha():
        return -1
    column = ord(input_letter.upper()) - ord('A')
    return column

def drop_checker(board, column, checker):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = checker
            return row

def check_for_win(board, row, col, checker):
    def check_direction(r_step, c_step):
        count = 0
        r, c = row, col
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += r_step
            c += c_step
        return count
    
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal /
    for dr, dc in directions:
        if check_direction(dr, dc) + check_direction(-dr, -dc) - 1 >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def play_game():
    # Initialization
    board = create_board()
    num_players = 2  # Default as per instructions
    players = CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)
    clear_screen()
    print_board(board)

    while True:
        print(f"Player {players[current_player]}, it's your turn.")
        user_input = input("Please enter a column (A-G): ")
        column = get_column_from_input(user_input)

        if column == -1 or not is_valid_column(column, board):
            print("Invalid input. Please try again!")
            continue  # Retry current player's turn

        # Place the checker
        row = drop_checker(board, column, players[current_player])
        clear_screen()
        print_board(board)

        # Check for a win
        if check_for_win(board, row, column, players[current_player]):
            print(f"Player {players[current_player]} won!")
            break
        
        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    play_game()
