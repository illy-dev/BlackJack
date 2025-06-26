import pygame

display_width = 1280
display_height = 720

background_color = (36,85,64)
grey = (220,220,220)
black = (0,0,0)
green = (0, 200, 0)
red = (255,0,0)
light_slat = (119,136,153)
dark_slat = (47, 79, 79)
dark_red = (255, 0, 0)
pygame.init()
font = pygame.font.SysFont("Arial", 20)
textfont = pygame.font.SysFont('Arial', 35)
game_end = pygame.font.SysFont('dejavusans', 100)
blackjack = pygame.font.SysFont('roboto', 70)
game_title = pygame.font.Font('assets/fonts/Daydream.ttf', 80)
button_font = pygame.font.Font('assets/fonts/Daydream.ttf', 32)
card_font = pygame.font.Font('assets/fonts/Daydream.ttf', 16)
option_font = pygame.font.Font('assets/fonts/Daydream.ttf', 24)


SUITS = ['KR', 'P', 'H', 'K']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

CARD_SIZE = (48, 64)
CARD_CENTER = (24, 32)
CARD_BACK_SIZE = (48, 64)
CARD_BACK_CENTER = (24, 32)