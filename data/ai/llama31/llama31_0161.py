import os
import random

# Global constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create a 2D list to represent the game board."""
    board = []
    for _ in range(BOARD_ROWS):
        row = [" "] * BOARD_COLS
        board.append(row)
    return board

def print_board(board):
    """Print the game board to the console."""
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    for row in board:
        print("+---+---+---+---+---+---+---+")
        print("| {} | {} | {} | {} | {} | {} | {} |".format(*row))
    print("+---+---+---+---+---+---+---+")

def validate_input(input_str):
    """Check if the user input is a valid column letter."""
    return input_str.upper().isalpha() and "A" <= input_str.upper() <= chr(64 + BOARD_COLS)

def get_player_move(player, board):
    """Get the player's move and validate it."""
    while True:
        move = input("Player {}, please enter a column: ".format(player))
        if validate_input(move):
            col = ord(move.upper()) - 65
            if board[0][col]!= " ":
                print("Column is full, try again.")
            else:
                return col
        else:
            print("Invalid input, try again.")

def drop_checker(board, col, checker):
    """Drop the checker into the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            break

def check_win(board, checker):
    """Check if the specified player has won."""
    # Check horizontal locations for win
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row][col + 1] == checker and board[row][col + 2] == checker and board[row][col + 3] == checker:
                return True

    # Check vertical locations for win
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if board[row][col] == checker and board[row + 1][col] == checker and board[row + 2][col] == checker and board[row + 3][col] == checker:
                return True

    # Check positively sloped diagonals
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row + 1][col + 1] == checker and board[row + 2][col + 2] == checker and board[row + 3][col + 3] == checker:
                return True

    # Check negatively sloped diagonals
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if board[row][col] == checker and board[row - 1][col + 1] == checker and board[row - 2][col + 2] == checker and board[row - 3][col + 3] == checker:
                return True

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= " " for row in board for cell in row)

def game_loop():
    """The main game loop."""
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players)

    while True:
        print_board(board)
        col = get_player_move(current_player, board)
        drop_checker(board, col, current_player)

        if check_win(board, current_player):
            print_board(board)
            print("Player {} won!".format(current_player))
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

game_loop()
