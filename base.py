import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Flappy Bird Chines')

clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

try:
    bird_image = pygame.image.load('bird.png')
    bird_image = pygame.transform.scale(bird_image, (50, 50))
    bird_rect = bird_image.get_rect()
    bird_rect.topleft = (100, 300)
    print("Imagem do pássaro carregada com sucesso")
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    sys.exit()

try:
    background_image = pygame.image.load('masqueico.jpg')
    background_image = pygame.transform.scale(background_image, (800, 600))
    print("Funfo")
except pygame.error as e:
    print(f"Erro")
    pygame.quit()
    sys.exit()

bird_velocity = 0
gravity = 0.02
jump_height = -2.2
max_fall_speed = 0.5

obstacle_width = 70
obstacle_height = random.randint(150, 400)
obstacle_x = 800
obstacle_gap = 200
obstacle_speed = 0.5
obstacle_passed = False

score = 0
font = pygame.font.Font(None, 36)

game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_height
            if event.key == pygame.K_r and game_over:
                # Reseta o jogo
                bird_rect.topleft = (100, 300)
                bird_velocity = 0
                obstacle_height = random.randint(150, 400)
                obstacle_x = 800
                obstacle_passed = False
                score = 0
                game_over = False

    if not game_over:
        bird_velocity += gravity
        if bird_velocity > max_fall_speed:
            bird_velocity = max_fall_speed

        bird_rect.y += bird_velocity

        if bird_rect.y < 0:
            bird_rect.y = 0
        elif bird_rect.y > 550:
            bird_rect.y = 550

        obstacle_x -= obstacle_speed
        if obstacle_x < -obstacle_width:
            obstacle_x = 800
            obstacle_height = random.randint(150, 400)
            obstacle_passed = False

        
        if (bird_rect.colliderect(pygame.Rect(obstacle_x, 0, obstacle_width, obstacle_height)) or
            bird_rect.colliderect(pygame.Rect(obstacle_x, obstacle_height + obstacle_gap, obstacle_width, 600 - obstacle_height - obstacle_gap))):
            game_over = True

        
        if not obstacle_passed and obstacle_x + obstacle_width < bird_rect.x:
            score += 1
            obstacle_passed = True


    screen.blit(background_image, (0,0))
    screen.blit(bird_image, bird_rect.topleft)
    pygame.draw.rect(screen, GREEN, pygame.Rect(obstacle_x, 0, obstacle_width, obstacle_height))
    pygame.draw.rect(screen, GREEN, pygame.Rect(obstacle_x, obstacle_height + obstacle_gap, obstacle_width, 600 - obstacle_height - obstacle_gap))

    
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        
        game_over_text = font.render(f"Game Over! Pontuação: {score}", True, BLACK)
        screen.blit(game_over_text, (200, 250))
        restart_text = font.render("Pressione 'R' para reiniciar", True, BLACK)
        screen.blit(restart_text, (200, 300))

        pygame.display.flip()

        
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                       
                        bird_rect.topleft = (100, 300)
                        bird_velocity = 0
                        obstacle_height = random.randint(150, 400)
                        obstacle_x = 800
                        obstacle_passed = False
                        score = 0
                        game_over = False
                        paused = False

    
    pygame.display.flip()
    clock.tick(400)

    print("Posição do pássaro:", bird_rect.topleft, "Posição do obstáculo:", obstacle_x, "Pontuação:", score)
