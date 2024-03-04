import pygame
import pygame_menu
import numpy as np
import sys, random
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax


class TicTacToeGame:
    def __init__(self, size=(600, 800)):
        # Initialize the game window and other parameters
        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (30,144,255)
        self.GREY = (192, 192, 192)
        self.RELAXING_PURPLE = (149, 107, 169)
        self.DARK_PURPLE = (48, 25, 52)
        self.GOLD = (255, 215, 0)
        self.TROMBONE_YELLOW = (210, 181, 91)
        self.CELADON_GREEN = (172, 225, 175)


        self.GRID_SIZE = 3
        self.MARGIN = 4

        self.WIDTH = self.size[0] / self.GRID_SIZE - self.MARGIN
        self.HEIGHT = self.size[0] / self.GRID_SIZE - self.MARGIN

        self.reset_button_rect = pygame.Rect(self.width - 110, self.height - 60, 100, 50)

        pygame.init()
        self.game_reset()
        self.draw_game()
        self.play_game()

    def draw_game(self):
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.DARK_PURPLE)
        # Draw the grid

        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                # Get the x and y coordinates of the current grid location
                x = col * (self.WIDTH - 2 + self.MARGIN) + self.MARGIN
                y = row * (self.HEIGHT - 2 + self.MARGIN) + self.MARGIN
                # Draw the rectangle for the current grid location
                pygame.draw.rect(self.screen, self.RELAXING_PURPLE, (x, y, self.WIDTH, self.HEIGHT))

        # Draw the reset button above the grid
        self.reset_button_rect = pygame.Rect(self.width - 110, self.height - 60, 100, 50)
        pygame.draw.rect(self.screen, self.TROMBOME_YELLOW, self.reset_button_rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render("Reset", True, self.BLACK)
        text_rect = text.get_rect(center=self.reset_button_rect.center)
        self.screen.blit(text, text_rect)

        pygame.display.update()

    def change_turn(self):
        # Change the turn indicator in the window title
        if self.game_state.turn_0:
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")


    def draw_circle(self, x, y):
        # Get the x and y coordinates of the center of the circle
        cx = (self.WIDTH + self.MARGIN) * (x + 0.5)
        cy = (self.HEIGHT + self.MARGIN) * (y + 0.5)

        # radius, with offset
        radius = min(self.WIDTH, self.HEIGHT) / 3 - self.MARGIN

        # Draw a circle at the specified position
        # 3 is pixel size of width
        pygame.draw.circle(self.screen, self.GOLD, (int(cx), int(cy)), int(radius), 3)
        pygame.display.update()

    def draw_cross(self, x, y):

        # Calculate the coordinates for drawing the cross
        cx1 = x * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH / 4
        cy1 = y * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT / 4
        cx2 = x * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH * 3 / 4
        cy2 = y * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT * 3 / 4

        # Draw the cross
        pygame.draw.line(self.screen, self.CELADON_GREEN, (cx1, cy1), (cx2, cy2), 3)
        pygame.draw.line(self.screen, self.CELADON_GREEN, (cx1, cy2), (cx2, cy1), 3)

        pygame.display.update()


    def is_game_over(self):
        # Check if the game is over
        terminal = self.game_state.is_terminal()

        # If the game is over, return True
        if terminal:
            return True

        # Otherwise, return False
        return False

    def move(self, move):
        # Check if the selected cell is empty
        row, col = move
        if self.game_state.board_state[row][col] == 0:
            # Update game state
            self.game_state.board_state[row][col] = 1 if self.game_state.turn_0 else -1

            # Draw the move on the board
            if self.game_state.turn_0:
                self.draw_circle(col, row)
            else:
                self.draw_cross(col, row)

            # Switch the other player
            self.game_state.turn_0 = not self.game_state.turn_0


    def play_ai(self):
        if self.algorithm_select == "Minimax":
         best_move = minimax(self.game_state, self.player_O)

        elif self.algorithm_select == "Negamax":
         best_move = negamax(self.game_state, self.player_O)

    # Draw the nought (or circle, depending on the symbol chosen for the AI player) at the best move returned by the algorithm
        self.draw_cross(*best_move)
        
        self.change_turn()
        pygame.display.update()
        terminal = self.game_state.is_terminal()
        self.game_state.get_scores(terminal)

    def play_game(self, mode="player_vs_ai"):
        # Main game loop
        done = False
        player_turn = True

        while not done:
            for event in pygame.event.get(): # User did something

                if event.type == pygame.QUIT:
                    done = True

                # mouse button was released and it is the player's turn
                elif event.type == pygame.MOUSEBUTTONUP and player_turn:
                    pos = pygame.mouse.get_pos()

                    # find approximate column from mouse's x coordinate
                    col = pos[0] // (self.WIDTH + self.MARGIN)

                    # make sure approximated column is not outside of largest possible index
                    # self.GRID_SIZE-1 gives largest possible index
                    col = min(col, self.GRID_SIZE - 1)

                    # convert to integer
                    col = int(col)

                    # find approximate row from mouse's y coordinate
                    row = pos[1] // (self.HEIGHT + self.MARGIN)

                    # make sure approximated row is not outside of largest possible index
                    row = min(row, self.GRID_SIZE - 1)

                    # convert to integer
                    row = int(row)

                    # check if the square is empty
                    if self.game_state.board_state[row][col] == 0:
                        # if empty, place move down on board
                        self.move((row, col))

                        # now it is AI's turn
                        player_turn = False

                # check if the reset button was clicked
                elif event.type == pygame.MOUSEBUTTONUP and not player_turn:
                    pos = pygame.mouse.get_pos()
                    if self.reset_button_rect.collidepoint(pos):
                        self.game_reset()
                        player_turn = True

            # if AI's turn
            if not player_turn and not self.is_game_over():
                moves = self.game_state.get_moves()
                move = random.choice(moves)
                self.move(move)
                player_turn = True

            if self.is_game_over():
                winner = "2" if self.game_state.turn_0 else "1 (You)"
                font = pygame.font.SysFont(None, 48)
                text = font.render(f"Player {winner} wins!", True, self.BLACK)
                text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(text, text_rect)
                pygame.display.update()
                pygame.time.wait(2000)
                self.game_reset()
                player_turn = True

            pygame.display.update()

        pygame.quit()


    def game_reset(self):
        # Reset the game state

        # re-initiliaze board
        initial_board_state = np.zeros((self.GRID_SIZE, self.GRID_SIZE))
        self.game_state = GameStatus(initial_board_state, turn_0=True)
        self.draw_game()
        pygame.display.update()

# Start the game
tictactoegame = TicTacToeGame()
tictactoegame.play_game()