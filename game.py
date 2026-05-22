import pygame
import random

pygame.init()

# Screen
WIDTH = 626
HEIGHT = 372

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minecraft Potato Catcher")

clock = pygame.time.Clock()


# Colours
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLACK = (0, 0, 0)

# Pictures

# Background
try:
    background = pygame.image.load("images/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    use_background = True
except:
    use_background = False

# Bucket
try:
    bucket_img = pygame.image.load("images/bucket.png")
    bucket_img = pygame.transform.scale(bucket_img, (60, 60))
    use_bucket_image = True
except:
    use_bucket_image = False

# NORMAL POTATO
try:
    potato_img = pygame.image.load("images/potato.png")
    potato_img = pygame.transform.scale(potato_img, (50, 50))
    use_potato_image = True
except:
    use_potato_image = False

# POISONOUS POTATO
try:
    poison_img = pygame.image.load("images/poison_potato.png")
    poison_img = pygame.transform.scale(poison_img, (50, 50))
    use_poison_image = True
except:
    use_poison_image = False


# Fonts

small_font = pygame.font.Font("fonts/Minecraft.ttf", 24)
font = pygame.font.Font("fonts/Minecraft.ttf", 32)
big_font = pygame.font.Font("fonts/Minecraft.ttf", 50)


# Player - bucket
bucket_width = 60
bucket_height = 60

bucket_x = WIDTH // 2 - bucket_width // 2
bucket_y = HEIGHT - 110

bucket_speed = 15

bucket_rect = pygame.Rect(
    bucket_x,
    bucket_y,
    bucket_width,
    bucket_height
)


# List of falling potatoes

potatoes = []

# how many potatoes at once
for i in range(4):

    potato_type = random.choice([
        "normal",
        "poison",
        "normal",
        "poison"
    ])

    potatoes.append({

        "x": random.randint(50, WIDTH - 50),

        "y": random.randint(-600, -50),

        "speed": random.randint(2, 3),

        "type": potato_type
    })

# Game

score = 0
lives = 6
level = 1

game_over = False
game_started = False

running = True


while running:

    clock.tick(60)

    for event in pygame.event.get():

        # Start the game
        if not game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True

        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                score = 0
                lives = 6
                level = 1

                potatoes.clear()

                for i in range(4):

                    potato_type = random.choice([
                        "normal",
                        "normal",
                        "normal",
                        "normal",
                        "poison"
                    ])

                    potatoes.append({

                        "x": random.randint(50, WIDTH - 50),

                        "y": random.randint(-600, -50),

                        "speed": random.randint(2, 3),

                        "type": potato_type
                    })

                game_over = False


    if game_started and not game_over:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            bucket_x -= bucket_speed

        if keys[pygame.K_RIGHT]:
            bucket_x += bucket_speed

        if bucket_x < 0:
            bucket_x = 0

        if bucket_x > WIDTH - bucket_width:
            bucket_x = WIDTH - bucket_width

        bucket_rect.x = bucket_x

        for potato in potatoes:

            potato["y"] += potato["speed"] + level * 0.3

            potato_rect = pygame.Rect(
                potato["x"],
                potato["y"],
                50,
                50
            )

            if potato_rect.colliderect(bucket_rect):

                if potato["type"] == "normal":
                    score += 1

                if potato["type"] == "poison":
                    lives -= 1


                potato["x"] = random.randint(50, WIDTH - 50)
                potato["y"] = random.randint(-300, -50)

                potato["type"] = random.choice([
                    "normal",
                    "normal",
                    "normal",
                    "normal",
                    "poison"
                ])

            if potato["y"] > HEIGHT:

   
                if potato["type"] == "normal":
                    lives -= 0.5

                potato["x"] = random.randint(50, WIDTH - 50)
                potato["y"] = random.randint(-300, -50)

                potato["type"] = random.choice([
                    "normal",
                    "normal",
                    "normal",
                    "normal",
                    "poison"
                ])

        if score >= 10:
            level = 2

        if score >= 25:
            level = 3

        if score >= 50:
            level = 4

        # GAME OVER
        if lives <= 0:
            game_over = True



    if use_background:
        screen.blit(background, (0, 0))
    else:
        screen.fill((120, 200, 255))


    for potato in potatoes:

        if potato["type"] == "normal":

            if use_potato_image:
                screen.blit(
                    potato_img,
                    (potato["x"], potato["y"])
                )
            else:
                pygame.draw.circle(
                    screen,
                    (160, 120, 60),
                    (potato["x"], potato["y"]),
                    25
                )

        else:

            if use_poison_image:
                screen.blit(
                    poison_img,
                    (potato["x"], potato["y"])
                )
            else:
                pygame.draw.circle(
                    screen,
                    (50, 200, 50),
                    (potato["x"], potato["y"]),
                    25
                )

    if use_bucket_image:
        screen.blit(bucket_img, (bucket_x, bucket_y))
    else:
        pygame.draw.rect(
            screen,
            (150, 150, 150),
            (bucket_x, bucket_y, bucket_width, bucket_height)
        )



    score_text = small_font.render(
        "Score: " + str(score),
        True,
        WHITE
    )

    lives_text = small_font.render(
        "Lives: " + str(lives),
        True,
        RED
    )

    level_text = small_font.render(
        "Level: " + str(level),
        True,
        WHITE
    )

    if game_started is True:

        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 60))
        screen.blit(level_text, (20, 100))

    # GAME OVER
    if game_over:

        over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        restart_text = big_font.render(
            "Press SPACE to restart",
            True,
            BLACK
        )

        screen.blit(over_text, (WIDTH // 2 - 160, HEIGHT // 2 - 40))
        screen.blit(restart_text, (WIDTH // 2 - 275, HEIGHT // 2 + 10))

    
    # START SCREEN
    if not game_started:

        title_text = font.render(
            "MINECRAFT POTATO CATCHER",
            True,
            BLACK
        )

        start_text = font.render(
            "Press SPACE to Start",
            True,
            BLACK
        )

        controls_text = font.render(
            "Move with LEFT and RIGHT arrows",
            True,
            BLACK
        )

        screen.blit(title_text, (WIDTH // 2 - 250, HEIGHT // 2 - 80))
        screen.blit(start_text, (WIDTH // 2 - 160, HEIGHT // 2 - 20))
        screen.blit(controls_text, (WIDTH // 2 - 260, HEIGHT // 2 + 10))

    pygame.display.update()

pygame.quit()