from sys import exit
import pygame
from pygame.locals import *
from state import State
from gamerender import GameRender
from abpruningai import ABPruningAI
import Settings.gamesettings as game_settings
import Settings.aisettings as ai_settings
import Settings.rendersettings as render_settings


if __name__ == "__main__":

    current_match = State()
    render = GameRender(current_match)
    ai = ABPruningAI(current_match)
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(render_settings.FPS)
        pygame.display.update()

        # AI move first
        if(game_settings.FIRST_TURN == game_settings.COM and len(current_match.moves) == 0):
            AI_calulation_time = -pygame.time.get_ticks()
            ai_move = ai.next_move()
            AI_calulation_time += pygame.time.get_ticks()
            print("AI calculation time: ", AI_calulation_time/1000 ," seconds (depth = ", ai_settings.MAX_TREE_DEPTH_LEVEL, ").")
            render.handle_com_move(ai_move, current_match)
            render.render_state(current_match.board, current_match.current_turn, State.game_over(current_match.board))
                
        for event in pygame.event.get():

            #exit
            if event.type == pygame.QUIT:
                running = False
                exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if(render.is_new_game_button_pressed()):
                    current_match = State()
                    ai = ABPruningAI(current_match)
                    render.render_state(current_match.board, game_settings.FIRST_TURN, False)
                    break

                if State.game_over(current_match.board):
                    
                    # Announcement
                    print("Game Over!")

                    continue
                
                # HUMAN turn
                if(current_match.current_turn == game_settings.HUMAN):
                    render.handle_human_move(current_match) 
                    render.render_state(current_match.board, current_match.current_turn, State.game_over(current_match.board))
                    ai.state.board = current_match.board

                if State.game_over(current_match.board):
                    
                    # Announcement
                    print("Game Over!")

                    continue

                # AI turn
                if(current_match.current_turn == game_settings.COM):
                    
                    AI_calulation_time = -pygame.time.get_ticks()

                    # Announcement
                    print("AI is calculating next move...")

                    ai_move = ai.next_move()
                    AI_calulation_time += pygame.time.get_ticks()
                    
                    # Announcement
                    print("AI calculation time: ", AI_calulation_time/1000 ," seconds.")
                    
                    render.handle_com_move(ai_move, current_match)
                    render.render_state(current_match.board, current_match.current_turn, State.game_over(current_match.board))
                
                if State.game_over(current_match.board):
                    
                    # Announcement
                    print("Game Over!")

                    continue

                



