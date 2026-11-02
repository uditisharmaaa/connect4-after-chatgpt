import os
import random
import string

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
MAX_PLAYERS = 5
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    """Create a 2D board with whitespaces"""
    board = [[" " for _ in range(cols)] for _ in range(rows)]
    return board

def print_board(board, cols):
    """Print the current state of the board"""
    print("  " + " ".join(string.ascii_uppercase[:cols]))
    for row in board:
        print("+---" * cols + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * cols + "+")

def get_valid_move(player, board, cols):
    """Get a valid move from the player"""
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if move in string.ascii_uppercase[:cols]:
            if all(cell!= " " for cell in [row[ord(move) - ord('A')] for row in board]):
                print("Column is full. Please choose another column.")
            else:
                return ord(move) - ord('A')
        else:
            print("Invalid input. Please enter a letter between A and", string.ascii_uppercase[cols-1])

def drop_checker(board, move, player_checker):
    """Drop the checker into the board"""
    for row in reversed(board):
        if row[move] == " ":
            row[move] = player_checker
            break

def check_win(board, player_checker):
    """Check for a win"""
    # Check horizontal
    for row in board:
        for i in range(len(row) - 3):
            if all([cell == player_checker for cell in row[i:i+4]]):
                return True

    # Check vertical
    for col in range(len(board[0])):
        for i in range(len(board) - 3):
            if all([board[row][col] == player_checker for row in range(i, i+4)]):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if all([board[row+i][col+i] == player_checker for i in range(4)]):
                return True

    # Check diagonal (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if all([board[row-i][col+i] == player_checker for i in range(4)]):
                return True

    return False

def check_draw(board):
    """Check for a draw"""
    return all(all(cell!= " " for cell in row) for row in board)

def main():
    num_players = 2
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:num_players]
    current_player = random.choice(players)

    while True:
        os.system('clear')
        print_board(board, BOARD_COLS)
        move = get_valid_move(current_player, board, BOARD_COLS)
        drop_checker(board, move, current_player)
        if check_win(board, current_player):
            os.system('clear')
            print_board(board, BOARD_COLS)
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            os.system('clear')
            print_board(board, BOARD_COLS)
            print("It's a draw!")
            break
        current_player = players[(players.index(current_player) + 1) % num_players]

if __name__ == "__main__":
    main()
