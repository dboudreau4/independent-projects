"""
I made this game to get better used to object oriented programming in Python.
In this game, enemy circles fall from the top of the screen and the player
(a rectangle) must fire a bullet at them to stop them. The player is moved
left and right at the bottom of the screen with the arrow keys, and the bullet
is fired with the space bar. The player starts with a score of 20, and each
enemy that reaches the bottom of the screen will cause the score to drop by 2.
If the player shoots an enemy, 10 points are earned at the enemy respawns at
the top. Additionally, if the player fails to dodge an enemy, 5 points of health
will be deducted. If the health or score fall to 0, the game ends and the window
automatically closes.

To run this file, you must have pygame installed on your computer, which requires
a quick one line cmd/powershell command.

I acknowledge this game is not as crisp, advanced, or efficient as it could be,
but I'm proud of the time I spent on it. If you have any suggestions, please feel
free to send them my way.
"""
import random
import pygame
pygame.font.init()

#game window-----------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

#colors----------------------
TEAL = (0, 255, 255)
GRAPE_FRUIT = (255, 102, 102)
RED = (255, 0, 0)
BLUE = (0, 255, 255)
GREEN = (0, 255, 0)

colors = [(TEAL), (GRAPE_FRUIT), (RED), (BLUE), (GREEN)]

class Enemy(object):
    """Constructor for the Enemy object, which is a circle
    with random color, radius, and speed. The position and
    color are passed by the user to the constructor, but the
    enemies end up being randomly generated depending on the
    number of enemies wanted by the user.
    """
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.radius = random.randint(10, 35)
        self.color = color
        self.speed = random.randint(5, 10)

class Player(object):
    """Constructor for the Player object, which is a rectangle
    with width, height, and position given by the user.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Bullet(object):
    """Constructor for the Bullet, which is a circle of fixed
    radius 5 and which stays with the Player object unless fired.
    The fired property is what is used to determine if the bullet
    should start moving.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fired = False
        self.radius = 5

    def hit(self, enemy):
        """Function to determine if the bullet has hit an enemy.
        Collision detection is similar to the checkCollision function
        used between the enemy and player, but this is between two circles,
        so the math is a little different.
        Returns:
            boolean: Returns true if a collision is detected
        """
        self_left = self.x - self.radius
        self_right = self.x + self.radius
        self_top = self.y - self.radius
        self_bottom = self.y + self.radius
        enemy_left = enemy.x - enemy.radius
        enemy_right = enemy.x + enemy.radius
        enemy_top = enemy.y - enemy.radius
        enemy_bottom = enemy.y + enemy.radius

        if self_right >= enemy_left and self_right < enemy_right or self_left >= enemy_left and self_left < enemy_right:
            if self_bottom >= enemy_top and self_bottom < enemy_bottom or self_top >= enemy_top and self_top < enemy_bottom:
                return True

def enemy_spawn(num):
    """Function to generate a user defined number of enemies and
    place them into a list.
    Returns:
        List: Returns a list of enemies with random colors
    """
    enemies = []
    for i in range(num):
        color = random.choice(colors)
        _x = Enemy(random.randint(0, WINDOW_WIDTH), 0, color)
        enemies.append(_x)

    return enemies

def create_player():
    """Function to construct a player with set dimensions
    Returns:
        Player object: Returns a player starting at the middle of
        the screen.
    """
    return Player(400, 500, 125, 75)

def check_collision(enemy, player):
    """Function to check if an enemy has collided with the player.
    Returns:
        boolean: Returns true if a collision has happened
    """
    p_right = player.x + player.width
    p_bottom = player.y + player.height
    e_left = enemy.x - enemy.radius
    e_right = enemy.x + enemy.radius
    e_top = enemy.y - enemy.radius
    e_bottom = enemy.y + enemy.radius

    if e_right >= player.x and e_right < p_right or e_left >= player.x and e_left < p_right:
        if e_bottom >= player.y and e_bottom < p_bottom or e_top >= player.y and e_top < p_bottom:
            return True

def main(win):
    """Main function where the game loop and all functions listed above
    are used. This function is called in the last line of this file to
    execute the code and it takes a game window object with a set width
    and height as input. To change the game window, modify the window width
    and height global variables at the top of the file.
    """
    #player, five enemies, and bullet created
    player = create_player()
    enemy = enemy_spawn(5)
    bullet = Bullet((player.x + int(player.width/2)), player.y)

    #game stats------------------
    score = 20 #score starts at 20 because enemies reaching the bottom deducts points
    health = 100

    clock = pygame.time.Clock()
    game_over = False

    #game loop------------------
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.display.quit()

        #player movement--------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.x += 15
            if event.key == pygame.K_LEFT:
                player.x -= 15
            if event.key == pygame.K_SPACE:
                #once fired, the bullet's free to move
                bullet.fired = True

        #enemy movement----------------
        for i in range(len(enemy)):
            #all enemies in the list move at their set speeds
            enemy[i].y += enemy[i].speed

            #if they reach the bottom, 2 points are lost
            #and the enemy restarts at the top of the screen
            if enemy[i].y >= WINDOW_HEIGHT:
                enemy[i].x = random.randint(0, WINDOW_WIDTH)
                enemy[i].y = 0
                score -= 2

            #if an enemy hits the player, the player's health
            #goes down by 5 and the enemy restarts at the top
            if check_collision(enemy[i], player):
                enemy[i].x = random.randint(0, WINDOW_WIDTH)
                enemy[i].y = 0
                health -= 5

            #if the bullet hits an enemy, the bullet goes back
            #to a not fired state to stop it from moving and goes
            # back to the player, the enemy restarts at the top,
            #10 points are earned
            if bullet.hit(enemy[i]):
                bullet.fired = False
                enemy[i].x = random.randint(0, WINDOW_WIDTH)
                enemy[i].y = 0
                bullet.x = player.x + int(player.width/2)
                bullet.y = player.y
                score += 10

        #if fired, the bullet starts moving up and if not, the
        #bullet moves with the player
        if bullet.fired:
            bullet.y -= 30
        else:
            bullet.x = player.x + int(player.width/2)
            bullet.y = player.y

        #if the bullet reaches the top of the screen, it's reset
        #to not fired and returns to the player
        if bullet.y <= 0:
            bullet.fired = False
            bullet.x = player.x + int(player.width/2)
            bullet.y = player.y

        if health <= 0 or score <= 0:
            game_over = True

        #background color
        win.fill((0, 0, 0))

        #display health and score
        health_font = pygame.font.SysFont("calibri", 30)
        health_display = health_font.render("Health: " + str(health), 1, BLUE)
        win.blit(health_display, (30, 30))
        score_font = pygame.font.SysFont("calibri", 30)
        score_display = score_font.render("Score: " + str(score), 1, GREEN)
        win.blit(score_display, (30, 60))

        #draw player---------------
        pygame.draw.rect(win, (TEAL), (player.x, player.y, player.width, player.height))

        #draw enemy-----------------

        for i in range(len(enemy)):
            pygame.draw.circle(win, enemy[i].color, (enemy[i].x, enemy[i].y), enemy[i].radius)

        #draw bullet------------------
        pygame.draw.circle(win, (TEAL), (bullet.x, bullet.y), bullet.radius)

        #frame rate
        clock.tick(30)
        #update display
        pygame.display.update()


#game setup------------------
GAME_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Beat the Meteors')

main(GAME_WINDOW)
