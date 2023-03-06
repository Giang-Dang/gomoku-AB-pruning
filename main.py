from sys import exit
import pygame
from pygame.locals import *
from state import State
from gamerender import GameRender
from abpruningai import ABPruningAI
import Settings.gamesettings as game_settings


if __name__ == "__main__":

    current_match = State()
    render = GameRender(current_match)
    ai = ABPruningAI(current_match)
    running = True

    while running:
        for event in pygame.event.get():

            #exit
            if event.type == pygame.QUIT:
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if(current_match.is_win()):
                    continue
                # HUMAN turn
                if render.handle_human_action(current_match, current_match.is_win()):
                    ai = ABPruningAI(current_match)

                # AI turn
                ai_move = ai.next_move()
                render.update_com_move(ai_move, current_match, current_match.is_win())

                



