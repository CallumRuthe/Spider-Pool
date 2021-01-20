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
TITLE = "<You're title here>"       # Decide on a title


# TODO: PLayer class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./Images/spider-pool.png")
        self.image = pygame.transform.scale(self.image, (90, 150))

        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - self.image.get_height()
        self.y_vel = 0

    # Movement -> Vertical only
    def update(self):
        pass
        # single and double jump

    def gravity(self):
        pass

    def jump(self):
        pass


# TODO: Enemy class


# TODO: Pickups class


# TODO: Projectile class


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

        # ----- LOGIC

        # ----- DRAW
        screen.fill(SKY_BLUE)
        all_sprites.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
