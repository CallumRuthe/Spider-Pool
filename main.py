# main.py
# My final project for programming 2

import pygame
import random
# TODO: Play testing / debugging
# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1280
HEIGHT = 720
JUMP_VEL = 10
MAX_JUMPS = 2
PROJECTILE_SPEED = 10
MAX_PROJECTILES = 5
MONEY_GOAL = 50
MONEY_VEL = -5
MONEY_CHANCE = 1000
ENEMY_CHANCE = 1250
ENEMY_VEL = -5
TITLE = "SPIDER-POOL"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Images/spider_pool.png")
        self.image = pygame.transform.scale(self.image, (120, 196))

        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT

        self.y_vel = 0
        self.num_jumps = 0

    def update(self):
        """ Move the player"""
        self.calc_grav()

        self.rect.y += self.y_vel

        if self.rect.bottom >= HEIGHT:
            self.y_vel = 0
            self.rect.y = HEIGHT - self.rect.height
            self.num_jumps = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.y_vel == 0:
            self.y_vel = 1
        else:
            self.y_vel += .35

    def jump(self):
        """ Called when user hits 'jump' button"""
        if self.num_jumps < MAX_JUMPS:
            self.y_vel -= JUMP_VEL
            self.num_jumps += 1


# randomly spawning enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Images/polverine.png")
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

        self.x_vel = ENEMY_VEL

    def update(self):
        self.rect.x += self.x_vel


# collect money to win
class Money(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.animation = [
            pygame.image.load("Images/Money Animation/flyingMoney-1.png"),
            pygame.image.load("Images/Money Animation/flyingMoney-2.png"),
            pygame.image.load("Images/Money Animation/flyingMoney-3.png"),
            pygame.image.load("Images/Money Animation/flyingMoney-4.png"),
            pygame.image.load("Images/Money Animation/flyingMoney-5.png"),
            pygame.image.load("Images/Money Animation/flyingMoney-6.png"),
            pygame.image.load("Images/Money Animation/flyingMoney-7.png"),
            pygame.image.load("Images/Money Animation/flyingMoney-8.png"),
        ]

        self.animation_frame = 0

        self.image = self.animation[0]
        self.image = pygame.transform.scale(self.image, (100, 91))

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

        self.x_vel = MONEY_VEL

    def update(self):
        self.animate()
        self.rect.x += self.x_vel

        if self.rect.right <= 0:
            self.kill()

    def animate(self):
        if self.animation_frame % 8 == 0:
            self.image = self.animation[0]
            self.image = pygame.transform.scale(self.image, (100, 91))
        elif self.animation_frame % 8 == 1:
            self.image = self.animation[1]
            self.image = pygame.transform.scale(self.image, (100, 91))
        elif self.animation_frame % 8 == 2:
            self.image = self.animation[2]
            self.image = pygame.transform.scale(self.image, (100, 91))
        elif self.animation_frame % 8 == 3:
            self.image = self.animation[3]
            self.image = pygame.transform.scale(self.image, (100, 91))
        elif self.animation_frame % 8 == 4:
            self.image = self.animation[4]
            self.image = pygame.transform.scale(self.image, (100, 91))
        elif self.animation_frame % 8 == 5:
            self.image = self.animation[5]
            self.image = pygame.transform.scale(self.image, (100, 91))
        elif self.animation_frame % 8 == 6:
            self.image = self.animation[6]
            self.image = pygame.transform.scale(self.image, (100, 91))
        elif self.animation_frame % 8 == 7:
            self.image = self.animation[7]
            self.image = pygame.transform.scale(self.image, (100, 91))

        self.animation_frame += 1


# create shuriken projectiles
class Projectile(pygame.sprite.Sprite):
    def __init__(self, coords):
        """
            Arguments:
                coords - tuple of x,y
        """
        super().__init__()

        self.animation = [
            pygame.image.load("Images/Shuriken Animation/shuriken.png"),
            pygame.image.load("Images/Shuriken Animation/shuriken-2.png")
        ]
        self.animation_frame = 0

        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = coords

        self.x_vel = PROJECTILE_SPEED

    def update(self):
        self.rect.x += self.x_vel
        self.animate()

        if self.rect.left >= WIDTH:
            self.kill()

    def animate(self):
        """ create the animation of the projectile"""
        if self.animation_frame % 2 == 0:
            self.image = self.animation[0]
        else:
            self.image = self.animation[1]

        self.animation_frame += 1


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    money_count = 0

    # text = pygame.font.SysFont("arial", True)
    # write = "jbafbjkaf"

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    projectile_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    money_sprites = pygame.sprite.Group()

    # Sprites
    # Player sprite
    player = Player()
    all_sprites.add(player)
    player_sprite.add(player)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Player jump on space bar press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

            # player shoot on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and len(projectile_sprites) <= 5:
                shuriken = Projectile((player.rect.right, player.rect.centery))
                all_sprites.add(shuriken)
                projectile_sprites.add(shuriken)

            # WIN condition: reached coin goal
            if money_count >= MONEY_GOAL:
                done = True
                print("you win")

        # ----- LOGIC
        all_sprites.update()


        # spawn money
        money_spawn_chance = random.randrange(0, MONEY_CHANCE)
        if money_spawn_chance < 10:
            money = Money()
            all_sprites.add(money)
            money_sprites.add(money)

        # spawn enemies
        enemy_spawn_chance = random.randrange(0, ENEMY_CHANCE)
        if enemy_spawn_chance < 10:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemy_sprites.add(enemy)

        # --- Collision
        # bullet hits enemy
        for shuriken in projectile_sprites:
            enemy_hit = pygame.sprite.spritecollide(shuriken, enemy_sprites, True)
            if len(enemy_hit) > 0:
                shuriken.kill()

        # enemy hits player
        for enemy in enemy_sprites:
            player_hit = pygame.sprite.spritecollide(enemy, player_sprite, True)
            if len(player_hit) > 0:
                done = True
                print("you lose")

        # player collects money
        money_hit = pygame.sprite.spritecollide(player, money_sprites, True)
        for money in money_hit:
            money_count += 1

        # TODO: secondary loss option if too many enemies get past player

        # ----- DRAW
        screen.fill(SKY_BLUE)
        all_sprites.draw(screen)

        # img = text.render(write, True, BLACK)
        # screen.blit(img, (100, 100))

        # TODO: counter for money
        # TODO: counter for ammo

        # TODO: Win screen
        # TODO: Lose screen

        # TODO: Title screen (optional)
        # TODO: Background (optional)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
