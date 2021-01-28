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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WIDTH = 1280
HEIGHT = 720
JUMP_VEL = 10
MAX_JUMPS = 2
PROJECTILE_SPEED = 10
MAX_PROJECTILES = 5
MONEY_GOAL = 25
MONEY_VEL = -5
MONEY_CHANCE = 1000        # chance to spawn money is 10/var
ENEMY_CHANCE = 1250        # chance to spawn enemy is 10/var
ENEMY_VEL = -5
MAX_ENEMIES_PAST = 3           # max number of enemies that can pass the player before losing
TITLE = "SPIDER-POOL"

INTRODUCTION = """WELCOME TO SPIDERPOOL"""
INSTRUCTIONS = """COLLECT MONEY WHILE AVOIDING POLVERINE"""
GOAL = """GATHER 25 MONEY BEFORE POLVERINE GETS YOU"""
GOAL_2 = f"""BE WARNED: IF {MAX_ENEMIES_PAST} POLVERINE GET PAST YOU LOSE"""
BEGIN = """CLICK TO BEGIN"""

WIN = """YOU WIN!!!"""
LOSE = """YOU LOSE"""
LOSE_HIT = """YOU GOT HIT BY POLVERINE"""
LOSE_PASSED = """YOU LET TOO MANY ENEMIES PASS YOU"""
EXIT = """PRESS ESCAPE TO QUIT"""


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
        
        if self.rect.right <= 0:
            self.kill()


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
   
   
def write_text(text, coords, font_size, surface, font_style="arial", bold=False, italic=False):
    """
    Arguments:
        text - string of text to blit
        coords - tuple of x y coordinates
        font_size - size of font
        surface - surface to blit onto
        font_style - text font
        bold - if text is bold, default False
        italic - if text is italic, default False
    """
    font = pygame.font.SysFont(font_style, font_size, bold, italic)
    text_surface = font.render(text, False, WHITE)
    surface.blit(text_surface, coords)
    # print(font.size(text))


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)
    background = pygame.image.load("Images/background.png")

    money_image = pygame.image.load("Images/Money Animation/flyingMoney-1.png")
    money_image = pygame.transform.scale(money_image, (100, 91))
    
    shuriken_image = pygame.image.load("Images/Shuriken Animation/shuriken.png")

    spiderpool_image = pygame.image.load("Images/spider_pool.png")
    spiderpool_image = pygame.transform.scale(spiderpool_image, (120, 196))

    polverine_image = pygame.image.load("Images/polverine.png")

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    money_count = 0
    enemies_past = 0
    introduction = True
    win = False
    lose = False
    lose_type = 0   # 1 = loss to getting hit, 2 = loss to getting passed

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

            # begin on mouse click
            if introduction:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    introduction = False

            # finish on mouse click
            if win or lose:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
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
            win = True
            # print("you win")

        # LOSE condition: too many polverine pass spiderpool
        if enemies_past >= MAX_ENEMIES_PAST:
            lose = True
            lose_type = 2
            # print("you lose (pass)")

        # ----- LOGIC
        if not introduction:
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
                lose = True
                lose_type = 1
                # print("you lose (hit)")

        # player collects money
        money_hit = pygame.sprite.spritecollide(player, money_sprites, True)
        for money in money_hit:
            money_count += 1

        for enemy in enemy_sprites:
            if enemy.rect.right <= 5:
                enemies_past += 1

        # update stats when money is collected
        stats = f"""YOU COLLECTED {money_count}/{MONEY_GOAL} money"""

        # ----- DRAW
        if introduction:        # run the introduction
            screen.fill(SKY_BLUE)

            # Text
            write_text(INTRODUCTION, (218, 100), 75, screen, bold=True)
            write_text(INSTRUCTIONS, (171, 287), 50, screen)
            write_text(GOAL, (126, 395), 50, screen)
            write_text(GOAL_2, (136, 503), 50, screen)
            write_text(BEGIN, (556, 611), 25, screen, italic=True)

            # Characters
            screen.blit(spiderpool_image, (50, 50))
            screen.blit(polverine_image, (WIDTH - (50 + polverine_image.get_width()), 50))

            pygame.display.flip()
            clock.tick(60)

        elif win:
            for sprite in all_sprites:
                sprite.kill()
            screen.fill(GREEN)

            # text
            write_text(WIN, (419, 100), 100, screen, bold=True)
            write_text(stats, (353, 315), 50, screen)
            write_text(EXIT, (512, 473), 25, screen, italic=True)

            # --images
            # left side
            for i in range(3):
                x = random.randrange(0, 253)
                y = random.randrange(0, HEIGHT - 91)
                screen.blit(pygame.transform.flip(money_image, True, False), (x, y))

            # right side
            for i in range(3):
                x = random.randrange(926, WIDTH - 100)
                y = random.randrange(0, HEIGHT - 91)
                screen.blit(money_image, (x, y))

        elif lose:
            for sprite in all_sprites:
                sprite.kill()
            screen.fill(RED)

            # text
            write_text(LOSE, (419, 100), 100, screen, bold=True)
            write_text(stats, (353, 423), 50, screen)
            write_text(EXIT, (512, 581), 25, screen, italic=True)

            if lose_type == 1:
                write_text(LOSE_HIT, (355, 315), 50, screen)

            elif lose_type == 2:
                write_text(LOSE_PASSED, (235, 315), 50, screen)

            # --images
            # left side
            for i in range(3):
                x = random.randrange(0, 92)
                y = random.randrange(0, HEIGHT - 161)
                screen.blit(pygame.transform.flip(polverine_image, True, False), (x, y))

            # right side
            for i in range(3):
                x = random.randrange(1044, WIDTH - 161)
                y = random.randrange(0, HEIGHT - 161)
                screen.blit(polverine_image, (x, y))

        else:
            screen.blit(background, (0, 0))

            write_text(str(money_count), (145, 100), 50, screen)
            screen.blit(money_image, (45, 75))

            write_text(str(6 - len(projectile_sprites)), (600, 40), 50, screen)
            screen.blit(shuriken_image, (550, 50))

            all_sprites.draw(screen)
        
        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
