import pgzrun
from pgzero.actor import Actor
import random

TITLE = 'Spaceship and Meteors'
WIDTH = 600
HEIGHT = 800

spaceship = Actor('spaceship', (300,740))
missles = []
meteors = []

score = 0
MAX_MET = 5
game_state = "NEW_GAME" 
WIN_SCORE =100

def update():
    global game_state
    
    if game_state == "PLAYING":
        if keyboard.left and spaceship.left > 0:
            spaceship.x -= 5
        if keyboard.right and spaceship.right < WIDTH:
            spaceship.x += 5
        if keyboard.up and spaceship.top > 0:
            spaceship.y -= 5
        if keyboard.down and spaceship.bottom < HEIGHT:
            spaceship.y += 5
        
        for missle in missles:
            missle.y -= 10
            if missle.top < 0:
                missles.remove(missle)
    
        for meteor in meteors:
            meteor.y += 3
            if meteor.top > HEIGHT:
                meteors.remove(meteor)

        if len(meteors) < MAX_MET and random.randint(0, 100) < 2:
            meteor = Actor('spacemeteors')
            meteor.x = random.randint(50, 450)
            meteor.y = 0
            meteors.append(meteor)

        if score >= WIN_SCORE:
            game_state = "WIN"    

        check_collisions()

def draw():
    screen.clear() 
    spaceship.draw()

    for missle in missles:
        missle.draw()

    for meteor in meteors:
        meteor.draw()
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=36, color="white")

    if game_state == "GAME_OVER":
        screen.draw.text("GAME OVER", center=(300, 350), fontsize=72, color="red")
        screen.draw.text("PRESS S TO START A NEW GAME", center=(300,450), fontsize=48, color="white")
    elif game_state == "WIN":
        screen.draw.text("YOU WIN!", center=(300, 350), fontsize=72, color="green")
        screen.draw.text("PRESS S TO START A NEW GAME", center=(300,450), fontsize=48, color="white")
    elif game_state == "PAUSED":
        screen.draw.text("PAUSED", center=(300, 400), fontsize=72, color="yellow")
    elif game_state == "NEW_GAME":
        screen.draw.text("PRESS S TO START", center=(300,400), fontsize=48, color="white")

def check_collisions():
    global score, game_state
    for meteor in meteors:
        if meteor.colliderect(spaceship):
            game_state = "GAME_OVER"
        
        for missle in missles:
            if missle.colliderect(meteor):
                missles.remove(missle)
                meteors.remove(meteor)
                score += 10

def on_key_down(key):
    global game_state

    if game_state == "NEW_GAME" and key == keys.S:
        start_new_game()
    elif game_state == "PLAYING" and key == keys.SPACE:
        missle = Actor('spacemissles', (spaceship.x, spaceship.top))
        missles.append(missle)
    elif game_state == "PLAYING" and key == keys.P:
        game_state = "PAUSED"
    elif game_state == "PAUSED" and key == keys.P:
        game_state = "PLAYING"
    elif game_state == "GAME_OVER" and key == keys.S:
        start_new_game()
    elif game_state == "WIN" and key == keys.S:
        start_new_game()

def start_new_game():
    global game_state, score, missles, meteors
    score = 0
    missles = []
    meteors = []
    game_state = "PLAYING"

pgzrun.go()