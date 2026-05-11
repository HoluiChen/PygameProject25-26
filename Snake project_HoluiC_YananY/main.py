from gamelib import *
from SnakeClass import *

game = Game(700, 500, "Hardcore Snake", 30)
snake_head = Animation("images/snake_head.png", 3, game, 43, 44,15) 
snake_body = Snake("images/snake_body.png", 5, 30, game)
apple = Image("images/apple.png", game)
apple.resizeTo(25, 25)
bk = Image("images/bk.jpg", game)
bullet = Animation("./images/plasmaball1.png", 11, game, 32,  32)
bullet.resizeBy(-50)
explosion = Animation("./images/explosion4.png",18,game,640 / 5, 512 / 4,5)
explosion.visible = False
logo = Animation("images/snakelogo.png",33,game,1700/5,2380/7)
logo.resizeBy(-70)
logo.y = 250
logo.x = 450
#function
def moveApple():
    while True:
        apple.moveTo(randint(50, 650), randint(50, 450))
        
        collision = False
        
        for segment in snake_body.snake:
            if apple.collidedWith(segment):
                collision = True
        
        for obstacle in obstacles:
            if apple.collidedWith(obstacle):
                collision = True
        
        if not collision:
            break

# list
obstacles = []
for i in range(5):
    obstacle = Image("images/obstacle.jpg", game) 
    obstacle.resizeTo(40, 40)
    
    # Keep moving obstacle until it's not colliding with snake
    while True:
        obstacle.moveTo(randint(50, 650), randint(50, 450))
        if not obstacle.collidedWith(snake_head):
            break
    
    obstacles.append(obstacle)

snake2 = []
for i in range(5):
    s = Animation("images/snake2.png", 20, game, 1700/5, 386/4)
    s.resizeBy(-70)
    snake2.append(s)


#sound
eat = Sound("sounds/eatapple.wav",0)
move = Sound("sounds/snakesound.mp3",1)
die = Sound("sounds/die.wav",2)
die2 = Sound("sounds/die2.wav",3)
winner = Sound("sounds/win.mp3",4)
loser = Sound("sounds/lose.wav",5)
#bar
progressbar = Shape("bar",game, 120, 10, magenta)
progressbar.moveTo(3 , 25)

#start direction and where the snake start move
start_x, start_y = 350, 250
snake_head.moveTo(start_x, start_y)
locations = []
for i in range(len(snake_body.snake) + 1): 
    locations.append((start_x - i * 30, start_y))
for i in range(len(snake_body.snake)):
    snake_body.snake[i].moveTo(locations[i+1][0], locations[i+1][1])
    
direction = "RIGHT"
snake_head.moveTo(350, 250)
snake_head.speed = 5

#game over screen images
gameover = Image("./images/gameover.png",game)
gameover.resizeBy(-50)
gameover.moveTo(350,100)

lose = Image("./images/youlose.png",game)
lose.resizeBy(-85)
lose.y = 300

win = Image("./images/youwin.png",game)
win.resizeBy(-50)
win.y = 300

#game start screen images
title = Image("images/title.png",game)
title.resizeBy(-30)
title.y = 100

story = Image("images/story.png",game)
story.resizeBy(-20)
story.y = 375
story.x = 200

storyText = Image("images/storytext.png",game)
storyText.resizeBy(-10)
storyText.visible = False

howto = Image("images/howtoplay.png",game)
howto.resizeBy(-70)
howto.y = 375

howtoText = Image("Images/howtoplaytext.png",game)
howtoText.visible = False

play = Image("images/play.png",game)
play.resizeBy(-60)
play.y = 375
play.x = 500

#Start screen
mouse.visible = False
game.setMusic("sounds/start.mp3")
game.playMusic()
while not game.over:
    game.processInput()

    bk.draw()
    bullet.visible = True
    bullet.moveTo(mouse.x, mouse.y)
    title.draw()
    logo.draw()
    apple.moveTo(250,250)
    apple.draw()
    story.draw()
    howto.draw()
    play.draw()
    howtoText.draw()
    storyText.draw()

    #Display Story Text
    if bullet.collidedWith(story,"rectangle") and mouse.LeftClick:
        storyText.visible = True
    #Display How to play text
    if bullet.collidedWith(howto,"rectangle") and mouse.LeftClick:
        howtoText.visible = True
    #close how to play text & return to Start menu
    if keys.Pressed[K_SPACE]:
        storyText.visible = False
        howtoText.visible = False
    #Start game
    if bullet.collidedWith(play,"rectangle") and mouse.LeftClick:
        game.over = True

    game.update(30)

#game level 1    
game.over = False
game.setMusic("sounds/snakesound.mp3")
game.playMusic()
while not game.over:
    game.processInput()
    bk.draw()
    progressbar.draw()
    progressbar.width = 120 - game.score * 4
    apple.draw()
    
    for i in range(len(obstacles)):
        obstacles[i].draw()
        if snake_head.collidedWith(obstacles[i]):
           game.score -= 2
           explosion.visible = True
           explosion.moveTo(obstacles[i].x, obstacles[i].y )
           explosion.draw(False)
           obstacles[i].visible = False
           obstacles[i].moveTo(randint(50, 650), randint(50, 450))
           obstacles[i].visible = True
        if apple.collidedWith(obstacles[i]):
            moveApple()
            

    # CHALLENGE: Increasing Speed, as the score goes up, the speed increases
    if game.score > 10:
        snake_head.speed = 5 + game.score * 0.2

    if keys.Pressed[K_LEFT] and direction != "RIGHT":
        direction = "LEFT"
    if keys.Pressed[K_RIGHT] and direction != "LEFT":
        direction = "RIGHT"
    if keys.Pressed[K_UP] and direction != "DOWN":
        direction = "UP"
    if keys.Pressed[K_DOWN] and direction != "UP":
        direction = "DOWN"

    if direction == "LEFT":
        snake_head.x -= snake_head.speed
    elif direction == "RIGHT":
        snake_head.x += snake_head.speed
    elif direction == "UP":
        snake_head.y -= snake_head.speed
    elif direction == "DOWN":
        snake_head.y += snake_head.speed

    # record head position
    locations.insert(0, (snake_head.x, snake_head.y))

    # keep length safe
    if len(locations) > len(snake_body.snake):
        locations.pop()

    # move body
    for i in range(len(snake_body.snake)):
        snake_body.snake[i].moveTo(locations[i][0], locations[i][1])


    # CHALLENGE: Self-Collision
    for i in range(4,len(snake_body.snake)):
        x = snake_head.x - snake_body.snake[i].x
        y = snake_head.y - snake_body.snake[i].y
        distance = (x**2 + y**2)**0.5
        if distance < 12:
            die2.play()
            game.over = True
    #If the snake leaves the screen, the game ends
    if snake_head.x < 0 or snake_head.x > game.width or snake_head.y < 0 or snake_head.y > game.height:
        die.play()
        game.over = True

    if game.score >= 30:
        game.over = True

    if snake_head.collidedWith(apple):
        snake_body.addTail()
        moveApple()
        eat.play()
        game.score += 1

    snake_head.draw()
    game.displayScore(0, 0)
    game.drawText("level 1",5,45)
    game.update(30)

#game level 2 
game.over = False
game.setMusic("sounds/snakesound.mp3")
game.playMusic()
# Reset snake position for the new level
direction = "RIGHT"

# Reset snake position
snake_head.moveTo(350, 250)

# Reset body spacing
locations = []
for i in range(len(snake_body.snake) + 1):
    locations.append((350 - i * 30, 250))

# Move body properly
for i in range(len(snake_body.snake)):
    snake_body.snake[i].moveTo(locations[i+1][0], locations[i+1][1])

# Set initial positions for enemy snakes
for s in snake2:
    s.moveTo(randint(0, 700), randint(0, 500))
    s.speed = randint(2, 5)

while not game.over and game.score >25:
    game.processInput()
    bk.draw()
    
    # Draw and Move Enemy Snakes
    for s in snake2:
        s.x += s.speed
        s.y += randint(-2, 2)
        # Wrap enemies around the screen
        if s.x < 0 or s.x > game.width or s.y < 0 or s.y > game.height:
            s.moveTo(randint(0, 700), randint(0, 500))
        s.draw()
        
        # Collision with enemies
        if snake_head.collidedWith(s):
            game.score -= 1
            s.visible = False
            s.moveTo(randint(0, 700), randint(0, 500))
            s.visible = True
            

    # Progress Bar 
    progressbar.draw()
    progressbar.width = 200 - game.score * 4
    
    apple.draw()
    
    # Movement Logic (Keeping Level 1 speed scaling)
    current_speed = 7 + (game.score * 0.1)
    if keys.Pressed[K_LEFT] and direction != "RIGHT": direction = "LEFT"
    if keys.Pressed[K_RIGHT] and direction != "LEFT": direction = "RIGHT"
    if keys.Pressed[K_UP] and direction != "DOWN": direction = "UP"
    if keys.Pressed[K_DOWN] and direction != "UP": direction = "DOWN"

    if direction == "LEFT": snake_head.x -= current_speed
    elif direction == "RIGHT": snake_head.x += current_speed
    elif direction == "UP": snake_head.y -= current_speed
    elif direction == "DOWN": snake_head.y += current_speed

    # Update Body
    locations.insert(0, (snake_head.x, snake_head.y))
    if len(locations) > len(snake_body.snake) + 1:
        locations.pop()
    for i in range(len(snake_body.snake)):
        snake_body.snake[i].moveTo(locations[i+1][0], locations[i+1][1])

    # Apple Collision
    if snake_head.collidedWith(apple):
        eat.play()
        snake_body.addTail()
        moveApple()
        game.score += 2

    #Challenge
    for i in range(4,len(snake_body.snake)):
        x = snake_head.x - snake_body.snake[i].x
        y = snake_head.y - snake_body.snake[i].y
        distance = (x**2 + y**2)**0.5
        if distance < 15:
            die2.play()
            game.over = True

    # Win condition for Level 2
    if game.score >= 50:
        game.over = True

    # Boundary Check
    if snake_head.x < 0 or snake_head.x > game.width or snake_head.y < 0 or snake_head.y > game.height:
        die.play()
        game.over = True

    snake_head.draw()
    game.displayScore(0, 0)
    game.drawText("level 2",5,45)
    game.update(30)

#End screen
game.over = False
#font
f = Font(green,45,black,"Comic Sans MS")
f1 = Font(cyan, 40, black, "Chiller")
while not game.over:
    game.processInput()
    bk.draw()

    gameover.draw()

    if game.score >= 50:
        win.draw()
        winner.play()
    else:
        lose.draw()
        loser.play()

    #show instruction to end game
    game.drawText("You get score:" + str(game.score),250,350, f1)
    game.drawText("Press [Q] to quit",175,game.height - 80,f)

    #Press Q key to Quit game
    if keys.Pressed[K_q]:
        game.over = True

    game.update(30)
game.quit()
