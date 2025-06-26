import pygame as pygame
from constants import *
import sys
import webbrowser

r"""
             /$$     /$$ /$$          
            | $$    |__/| $$          
 /$$   /$$ /$$$$$$   /$$| $$  /$$$$$$$
| $$  | $$|_  $$_/  | $$| $$ /$$_____/
| $$  | $$  | $$    | $$| $$|  $$$$$$ 
| $$  | $$  | $$ /$$| $$| $$ \____  $$
|  $$$$$$/  |  $$$$/| $$| $$ /$$$$$$$/
 \______/    \___/  |__/|__/|_______/ 
                                                  
"""

from util.components.button import Button
from util.components.card import Card
from util.cards import *

icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Black Jack")

screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()

        self.gameStateManager = GameStateManager('start')
        self.start = Start(screen, self.gameStateManager)
        self.level = Level(screen, self.gameStateManager)
        self.game = RunningGame(screen, self.gameStateManager)

        self.states = {'start': self.start, 'level': self.level, 'game': self.game}

    def run(self):
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.gameStateManager.set_state('start')
                    if event.key == pygame.K_2:
                        self.gameStateManager.set_state('level')

            self.states[self.gameStateManager.get_state()].run(events)

            pygame.display.update()
            clock.tick(60)

def draw_text(text: str, font, text_col, x, y):
    text = font.render(text, True, text_col)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self, events):
        self.display.fill('red')

class RunningGame:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        button_w, button_h = 150, 45
        center_x = display_width // 2

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.calc_hand()

        self.hit_button = Button(
            (center_x - button_w//2) - 80, display_height - 50, button_w, button_h,
            "Hit", option_font, 'black', 'white', 'black', 5,
            action=lambda: self.player_hand.add_card(self.deck.deal()),
            hover_effect=True
        )

        self.stay_button = Button(
            (center_x - button_w//2) + 80, display_height - 50, button_w, button_h,
            "Stand", option_font, 'black', 'white', 'black', 5,
            action=lambda: self.gameStateManager.set_state('game'),
            hover_effect=True
        )

    def run(self, events):
        self.display.fill(background_color)

        self.card_sprites = []
        for i, card in enumerate(self.player_hand.cards):
            card_img = pygame.image.load(f"./assets/Cards/{card.name}.png")
            self.card_sprites.append(
                Card(
                    (display_width//4) + i*110, display_height//1.5, 96, 128,
                    card.name, 'white', card_img
                )
            )

        self.hit_button.draw(self.display)
        self.stay_button.draw(self.display)
        for card in self.card_sprites:
            card.draw(self.display)

        draw_text(f"{self.player_hand.calc_hand()}", option_font, 'white', display_width-50, display_height-50)

        # mouse click listener
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = event.pos
                if self.hit_button.is_clicked(mouse_pos):
                    self.hit_button.action()
                if self.stay_button.is_clicked(mouse_pos):
                    self.stay_button.action()


class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        github_img = pygame.image.load("./assets/githublogo2.png")

        button_w, button_h = 200, 60
        center_x = display_width // 2

        self.play_button = Button(
            center_x - button_w//2, 300, button_w, button_h,
            "Play", button_font, 'black', 'white', 'black', 5,
            action=lambda: self.gameStateManager.set_state('game'),
            hover_effect=True
        )

        self.github_button = Button(
            display_width - 50, display_height - 50, 40, 40, 
            '', font, (0,0,0), None, None, 0, image=github_img,
            action=lambda: webbrowser.open("https://github.com/illy-dev/BlackJack", new=2, autoraise=True),
            hover_effect=False
        )

        self.quit_button = Button(
            center_x - button_w//2, 380, button_w, button_h,
            "Quit", button_font, 'black', 'white', 'black', 5,
            action=lambda: sys.exit(),
            hover_effect=True
        )

    def run(self, events):
        self.display.fill(background_color)
        draw_text("Black Jack", game_title, 'black', (display_width//2), (display_height//8))
        draw_text("Black Jack", game_title, 'white', (display_width//2.03), (display_height//8))

        self.play_button.draw(self.display)
        self.quit_button.draw(self.display)
        self.github_button.draw(self.display)

        # mouse click listener
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = event.pos
                if self.play_button.is_clicked(mouse_pos):
                    self.play_button.action()
                if self.quit_button.is_clicked(mouse_pos):
                    self.quit_button.action()
                if self.github_button.is_clicked(mouse_pos):
                    self.github_button.action()
        

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState
    
    def set_state(self, state):
        self.currentState = state

if __name__ == '__main__':
    game = Game()
    game.run()