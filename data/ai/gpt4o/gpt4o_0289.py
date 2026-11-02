import random
import os

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    header = "  " + "   ".join(chr(65 + i) for i in range(COLUMNS))
    separator = "+---" * COLUMNS + "+"
    print(header)
    for row in board:
        print(separator)
        print("| " + " | ".join(row) + " |")
    print(separator)

def is_valid_input(col_input):
    if len(col_input) != 1:
        return False
    column = ord(col_input.upper()) - 65
    return 0 <= column < COLUMNS

def get_column_index(col_input):
    return ord(col_input.upper()) - 65

def make_move(board, player, col_input):
    col = get_column_index(col_input)
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return True
    return False

def check_winner(board, player):
    def check_line(sequence):
        count = 0
        for cell in sequence:
            if cell == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
        return False

    for row in board:
        if check_line(row):
            return True

    for col in range(COLUMNS):
        if check_line([board[row][col] for row in range(ROWS)]):
            return True

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
            if all(board[row+3-i][col+i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = create_board()
    current_player_index = random.randint(0, PLAYERS - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_player = CHECKERS[current_player_index]

        col_input = input(f"Player {current_player}, please enter a column: ")
        while not is_valid_input(col_input):
            col_input = input(f"Invalid input. Player {current_player}, please enter a valid column: ")

        if make_move(board, current_player, col_input):
            print_board(board)
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif check_draw(board):
                print("The game is a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % PLAYERS
        else:
            print(f"Column {col_input.upper()} is full. Player {current_player} loses the turn.")

if __name__ == "__main__":
    play_game()
