import pygame, sys, random, time
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

scorefont = pygame.font.Font("neuropolxrg.ttf", 20)

menu_font = pygame.font.Font("neuropolxrg.ttf", 50)
menu_text = menu_font.render("Press Enter to Start.", True, (0, 0, 0))
menu_textRect = menu_text.get_rect(center = (400, 300))

score = 0
high_score_file = open("highscore.txt", "r")
highscore = int(high_score_file.read())
high_score_file.close()

TIMER = pygame.USEREVENT

def time_up(score, highscore):
    
    time_up_text = menu_font.render("Time's up!", True, (0, 0, 0))
    time_up_textRect = time_up_text.get_rect(center = (400, 100))
    finalscoretext = scorefont.render("You scored: {}".format(score), True, (0, 0, 0))
    finalscoretextRect = finalscoretext.get_rect(center = (400, 200))
    if score == highscore:
        newhighscoretext = scorefont.render("That's a new high score!", True, (0, 0, 0))
        newhighscoretextRect = newhighscoretext.get_rect(center = (400, 300))
        screen.blit(newhighscoretext, newhighscoretextRect)
    game_active = False
    screen.blit(time_up_text, time_up_textRect)
    screen.blit(finalscoretext, finalscoretextRect)
    pygame.display.update()
    time.sleep(2)

def game_loop(score, highscore):

    pygame.time.set_timer(TIMER, 10000)

    x = 375
    y = 275
    score = 0

    game_active = False

    def level_loop(score, highscore, game_active, x, y):

        
        objectivex = random.randint(0, 700)
        objectivey = random.randint(0, 500)


        while True:

            scoretext = scorefont.render("Score: {}".format(score), True, (0, 0, 0))
            scoretextRect = scoretext.get_rect(center = (200, 50))
            highscoretext = scorefont.render("High Score: {}".format(highscore), True, (0, 0, 0))
            highscoretextRect = highscoretext.get_rect(center = (600, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not game_active:
                    game_active = True
                if event.type == TIMER:
                    time_up(score, highscore)
                    game_loop(score, highscore)

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP] and y >= 0 and game_active:
                y -= 10
            if pressed[pygame.K_DOWN] and y <= 550 and game_active:
                y += 10
            if pressed[pygame.K_LEFT] and x >= 0 and game_active:
                x -= 10
            if pressed[pygame.K_RIGHT] and x <= 750 and game_active:
                x += 10

            if int(score) >= int(highscore):
                highscore = score
                high_score_file = open("highscore.txt", "w")
                high_score_file.write(str(highscore))
                high_score_file.close()


            screen.fill((255, 255, 255))


            if game_active:

                objective = pygame.Rect(objectivex, objectivey, 100, 100)
                pygame.draw.rect(screen, (255, 0, 0), objective)

                player = pygame.Rect(x, y, 50, 50)
                pygame.draw.rect(screen, (0, 0, 255), player)

                if player.colliderect(objective):

                    score += 1
                    level_loop(score, highscore, game_active, x, y)

            elif not game_active:
            
                screen.blit(menu_text, menu_textRect)

            screen.blit(scoretext, scoretextRect)
            screen.blit(highscoretext, highscoretextRect)

            pygame.display.update()
            clock.tick(60)
    
    level_loop(score, highscore, game_active, x, y)

game_loop(score, highscore)