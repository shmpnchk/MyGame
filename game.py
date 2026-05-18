import pygame
import random

pygame.init()

# экран
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ну, погоди! - PRO")

clock = pygame.time.Clock()

# фон
try:
    background = pygame.image.load("images/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    use_bg = True
except:
    use_bg = False

# звуки (если есть)
try:
    catch_sound = pygame.mixer.Sound("sounds/catch.wav")
    miss_sound = pygame.mixer.Sound("sounds/miss.wav")
except:
    catch_sound = None
    miss_sound = None

# дорожки (4 лотка)
lanes_x = [180, 300, 420, 540]

# волк (анимация)
wolf_imgs = []
try:
    wolf_imgs.append(pygame.image.load("images/wolf1.png"))
    wolf_imgs.append(pygame.image.load("images/wolf2.png"))
    wolf_imgs = [pygame.transform.scale(img, (100, 100)) for img in wolf_imgs]
    wolf_use_img = True
except:
    wolf_use_img = False

wolf_lane = 3
wolf_rect = pygame.Rect(lanes_x[wolf_lane], 480, 100, 100)
wolf_anim = 0

# яйца (несколько)
eggs = []

for i in range(3):
    eggs.append({
        "lane": random.randint(0, 3),
        "y": random.randint(-300, 0),
        "speed": random.randint(4, 7)
    })

egg_img = None
try:
    egg_img = pygame.image.load("images/egg.png")
    egg_img = pygame.transform.scale(egg_img, (40, 50))
except:
    pass

# игра
score = 0
lives = 3
font = pygame.font.SysFont("Arial", 28)

game_over = False

# уровни сложности
level = 1

running = True

while running:

    clock.tick(60)

    # события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            score = 0
            lives = 3
            level = 1
            game_over = False
            eggs.clear()
            for i in range(3):
                eggs.append({
                    "lane": random.randint(0, 3),
                    "y": random.randint(-300, 0),
                    "speed": random.randint(4, 7)
                })

    if not game_over:

        keys = pygame.key.get_pressed()

        # управление по 4 лоткам
        if keys[pygame.K_LEFT]:
            wolf_lane -= 1
            if wolf_lane < 0:
                wolf_lane = 0

        if keys[pygame.K_RIGHT]:
            wolf_lane += 1
            if wolf_lane > 3:
                wolf_lane = 3

        wolf_rect.x = lanes_x[wolf_lane]

        # анимация волка
        wolf_anim += 0.1

        # движение яиц
        for egg in eggs:

            egg["y"] += egg["speed"] + level * 0.2

            egg_rect = pygame.Rect(lanes_x[egg["lane"]], egg["y"], 40, 50)

            # поймал
            if egg_rect.colliderect(wolf_rect):

                score += 1

                if catch_sound:
                    catch_sound.play()

                egg["y"] = random.randint(-200, 0)
                egg["lane"] = random.randint(0, 3)

            # упало
            if egg["y"] > HEIGHT:

                lives -= 1

                if miss_sound:
                    miss_sound.play()

                egg["y"] = random.randint(-200, 0)
                egg["lane"] = random.randint(0, 3)

        # уровень сложности
        if score > 10:
            level = 2
        if score > 25:
            level = 3

        # game over
        if lives <= 0:
            game_over = True

    # фон
    if use_bg:
        screen.blit(background, (0, 0))
    else:
        screen.fill((120, 200, 255))

    # яйца
    for egg in eggs:
        if egg_img:
            screen.blit(egg_img, (lanes_x[egg["lane"]], egg["y"]))
        else:
            pygame.draw.ellipse(screen, (255, 255, 0),
                                (lanes_x[egg["lane"]], egg["y"], 40, 50))

    # волк
    if wolf_use_img:
        screen.blit(wolf_imgs[int(wolf_anim) % 2], wolf_rect)
    else:
        pygame.draw.rect(screen, (255, 255, 255), wolf_rect)

    # UI
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, (255, 80, 80)), (10, 40))
    screen.blit(font.render(f"Level: {level}", True, (255, 255, 0)), (10, 70))

    # game over экран
    if game_over:
        text = font.render("GAME OVER - press any key", True, (255, 255, 255))
        screen.blit(text, (200, 300))

    pygame.display.update()

pygame.quit()