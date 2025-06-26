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
                    #if event.key == pygame.K_2:
                        #self.gameStateManager.set_state('level')

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
        self.display.fill(background_color)

class RunningGame:

    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

        button_w, button_h = 150, 45
        center_x = display_width // 2

        self.outcome = ""
        self.game_over = False

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.deck = Deck(num_decks=6)
        self.deck.shuffle()

        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.calc_hand()

        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.calc_hand()

        if self.player_hand.calc_hand() == 21:
            if self.dealer_hand.calc_hand() == 21:
                self.outcome = "Push (Both have Blackjack)"
            else:
                self.outcome = "Blackjack! You Win!"
            self.game_over = True
        elif self.dealer_hand.calc_hand() == 21:
            self.outcome = "Dealer Wins!"
            self.game_over = True


        self.hit_button = Button(
            (center_x - button_w//2) - 80, display_height - 50, button_w, button_h,
            "Hit", option_font, 'black', 'white', 'black', 5,
            action=self.hit,
            hover_effect=True
        )

        self.stay_button = Button(
            (center_x - button_w//2) + 80, display_height - 50, button_w, button_h,
            "Stand", option_font, 'black', 'white', 'black', 5,
            action=self.stand,
            hover_effect=True
        )

        self.play_again_button = Button(
            (center_x - 120), display_height//2 + 50, 240, 56,
            "Play Again", option_font, 'black', 'white', 'black', 5,
            action=self.reset_game,
            hover_effect=True
        )

    def dealer_turn(self):
        while self.dealer_hand.calc_hand() < 17:
            self.dealer_hand.add_card(self.deck.deal())
        self.outcome = self.determine_outcome()

    def determine_outcome(self):
        player_total = self.player_hand.calc_hand()
        dealer_total = self.dealer_hand.calc_hand()

        if player_total > 21:
            return "You Busted! Dealer Wins!"
        elif dealer_total > 21:
            return "Dealer Busted! You Win!"
        elif player_total > dealer_total:
            return "You Win!"
        elif dealer_total > player_total:
            return "Dealer Wins!"
        else:
            return "Push (Draw)"


    def reset_game(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        if len(self.deck.cards) < 15:
            self.deck = Deck(num_decks=6)
            self.deck.shuffle()

        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.calc_hand()

        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.dealer_hand.calc_hand()

        self.outcome = ""
        self.game_over = False


    def hit(self):
        if not self.game_over:
            self.player_hand.add_card(self.deck.deal())
            if self.player_hand.calc_hand() > 21:
                self.outcome = "You Busted! Dealer Wins!"
                self.game_over = True

    def stand(self):
        if not self.game_over:
            while self.dealer_hand.calc_hand() < 17:
                self.dealer_hand.add_card(self.deck.deal())

            self.outcome = self.determine_outcome()
            self.game_over = True

    def run(self, events):
        self.display.fill(background_color)

        self.dealer_card_sprites = []
        for i, card in enumerate(self.dealer_hand.cards):
            dealer_card_img = pygame.image.load(f"./assets/Cards/{card.name}.png")
            self.dealer_card_sprites.append(
                Card(
                    (display_width//4) + i*110, display_height//4, 96, 128,
                    card.name, 'white', dealer_card_img
                )
            )

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
        for card in self.dealer_card_sprites:
            card.draw(self.display)

        draw_text(f"{self.player_hand.calc_hand()}", option_font, 'white', display_width-50, display_height-50)
        draw_text(f"{self.dealer_hand.calc_hand()}", option_font, 'white', display_width-50, 50)

        if self.outcome:
            draw_text(self.outcome, option_font, 'yellow', display_width // 2, display_height // 2)

        if self.game_over:
            self.play_again_button.draw(self.display)

        # mouse click listener
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left Click
                mouse_pos = event.pos
                if not self.game_over:
                    if self.hit_button.is_clicked(mouse_pos):
                        self.hit_button.action()
                    if self.stay_button.is_clicked(mouse_pos):
                        self.stay_button.action()
                else:
                    if self.play_again_button.is_clicked(mouse_pos):
                        self.play_again_button.action()


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