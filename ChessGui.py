import pygame
import chess
from math import floor

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class ChessGui:
    def __init__(self):
        self.__x = 800
        self.__y = 800
        self.__screen = None

        self.__board = chess.Board()

        self.__clock = pygame.time.Clock()
        self.__fps = 30

        self.__piece_images = None

    @staticmethod
    def init():
        pygame.init()

    @staticmethod
    def quit():
        pygame.quit()

    def frame(self):
        for i in range(64):
            piece = self.__board.piece_at(i)

            if piece == None:
                black_surface = pygame.Surface((100, 100))
                black_surface.fill((0, 0, 0))  # Fill the surface with black

                # Blit the black rectangle onto the screen at the specified coordinates
                self.__screen.blit(black_surface, ((i % 8) * 100, 700 - (i // 8) * 100))
            else:
                self.__screen.blit(self.__piece_images[str(piece)], ((i % 8) * 100, 700 - (i // 8) * 100))

        for i in range(7):
            i = i + 1
            pygame.draw.line(self.__screen, WHITE, (0, i * 100), (800, i * 100))
            pygame.draw.line(self.__screen, WHITE, (i * 100, 0), (i * 100, 800))

        pygame.display.flip()

    def __handle_mouse_click(self, pos, source_square, possible_destinations):
        # find which square was clicked and index of it
        coordinates = (floor(pos[0] / 100), floor(pos[1] / 100))
        clicked_square = (7 - coordinates[1]) * 8 + (coordinates[0])

        if source_square is not None and clicked_square in possible_destinations:
            move = chess.Move(source_square, clicked_square)
            self.__board.push(move)
            source_square = None
            possible_destinations.clear()
            return source_square, possible_destinations

        piece_selected = self.__board.piece_at(clicked_square)

        if piece_selected is not None:
            for move in self.__board.legal_moves:
                if move.from_square == clicked_square:
                    possible_destinations.add(move.to_square)
        else:
            possible_destinations.clear()

        return clicked_square

    def run(self, white_agent, black_agent):
        self.__screen = pygame.display.set_mode((self.__x, self.__y))

        self.__piece_images = {
            'p': pygame.image.load('assets/b_pawn.png').convert(),
            'n': pygame.image.load('assets/b_knight.png').convert(),
            'b': pygame.image.load('assets/b_bishop.png').convert(),
            'r': pygame.image.load('assets/b_rook.png').convert(),
            'q': pygame.image.load('assets/b_queen.png').convert(),
            'k': pygame.image.load('assets/b_king.png').convert(),
            'P': pygame.image.load('assets/w_pawn.png').convert(),
            'N': pygame.image.load('assets/w_knight.png').convert(),
            'B': pygame.image.load('assets/w_bishop.png').convert(),
            'R': pygame.image.load('assets/w_rook.png').convert(),
            'Q': pygame.image.load('assets/w_queen.png').convert(),
            'K': pygame.image.load('assets/w_king.png').convert(),
        }

        self.__screen.fill(BLACK)

        quit = False
        source_square = None
        possible_destinations = set()
        last_turn = self.__board.turn
        while not quit:
            self.show_loading_screen()
            human_turn = self.__board.turn == chess.WHITE and white_agent is None or self.__board.turn == chess.BLACK and black_agent is None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN and human_turn:
                    source_square = self.__handle_mouse_click(pygame.mouse.get_pos(), source_square, possible_destinations)

            if not self.__board.is_game_over():
                if self.__board.turn == chess.WHITE and white_agent is not None:
                    move = white_agent.get_move(self.__board.copy())
                    self.__board.push(move)
                elif self.__board.turn == chess.BLACK and black_agent is not None:
                    move = black_agent.get_move(self.__board.copy())
                    self.__board.push(move)

            if last_turn != self.__board.turn:
                print(self.__board.fen())
                last_turn = self.__board.turn

            self.frame()
            self.__clock.tick(self.__fps)

    def show_loading_screen(self):
        font = pygame.font.Font(None, 36)
        loading_text = font.render("Loading...", True, (255, 255, 255))
        text_rect = loading_text.get_rect(center=(400, 300))
        self.__screen.blit(loading_text, text_rect)
        pygame.display.flip()
