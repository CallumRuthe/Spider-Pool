# main.py
# My final project for programming 2

import pygame

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
MAX_COINS = 50
TITLE = "SPIDER-POOL"


# TODO: PLayer class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Images/spider_pool.png")
        self.image = pygame.transform.scale(self.image, (120, 196))

        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT

        self.y_vel = 0
        self.num_jumps = 0

    # Movement -> Vertical only
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


# TODO: Enemy class
# randomly spawning enemies

# TODO: pickups classes
# refill ammo
# collect coins to win

# TODO: Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, coords):
        """
            Arguments:
                coords - tuple of x,y
        """
        super().__init__()

        self.image = pygame.image.load("Images/Shuriken Animation/shuriken.png")
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = coords

        self.x_vel = PROJECTILE_SPEED

    def update(self):
        self.rect.x += self.x_vel
        self.animate()

    # TODO: animate shuriken
    def animate(self):
        """ create the animation of the projectile"""
        if self.image == pygame.image.load("Images/Shuriken Animation/shuriken-2.png"):
            self.image = pygame.image.load("Images/Shuriken Animation/shuriken.png")
        elif self.image == pygame.image.load("Images/Shuriken Animation/shuriken.png"):
            self.image = pygame.image.load("Images/Shuriken Animation/shuriken-2.png")


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    projectile_sprites = pygame.sprite.Group()

    # Sprites
    # Player sprite
    player = Player()
    all_sprites.add(player)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # TODO: Keyboard / mouse controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

            if event.type == pygame.MOUSEBUTTONDOWN:
                shuriken = Projectile((player.rect.right, player.rect.centery))
                all_sprites.add(shuriken)
                projectile_sprites.add(shuriken)

        # ----- LOGIC
        all_sprites.update()

        # ----- DRAW
        screen.fill(SKY_BLUE)
        all_sprites.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
