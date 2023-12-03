import turtle
import time
import random
import json

# Set up the screen
wn = turtle.Screen()
wn.title("Galaga")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Player
player = turtle.Turtle()

turtle.addshape('char/spaceship.gif')
player.shape('char/spaceship.gif')

player.shapesize(stretch_wid=1, stretch_len=2)
player.penup()
player.goto(0, -250)
player_speed = 20

# Player bullet
bullet = turtle.Turtle()
bullet.shape("triangle")
bullet.color("yellow")
bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)
bullet.penup()
bullet.hideturtle()
bullet_speed = 20

# Score
score = 0

# Score display
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Score: {}".format(score),
                    align="center",
                    font=("Courier", 16, "normal"))

# Enemies
enemies = []


def generate_calculus_problem():
  #problems
  with open('data/question.json') as f:
    question = json.load(f)
    
  problems = question["data"]
  # Select a random problem
  problem = random.choice(problems)
  return problem


# What happen after answer chosen
def handle_choice(choice, correct_answer, pen):
  if choice == correct_answer:
      time.sleep(2)
      pen.hideturtle()
      pen.clear()
      pen.write("Correct! You survive.", align="center", font=("Arial", 14, "bold"))
      time.sleep(2)
      pen.hideturtle()
      pen.clear()
      continue_game()
        
  else:
      pen.hideturtle()
      pen.clear()
      pen.write("Wrong answer. You died.", align="center", font=("Arial", 14, "bold"))       
        
def display_question(problem):
    

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.penup()
    pen.color("white")
    pen.goto(0, 50)
    pen.write(problem["question"], align="center", font=("Arial", 16, "normal"))

    start_y = 30
    for i, option in enumerate(problem["options"], 1):
        pen.goto(0, start_y - 30*i)
        pen.write(f"{i}. {option}", align="center", font=("Arial", 14, "normal"))

    # Here, implement logic to capture user's choice and check the answer
    for i in range(4):
      wn.onkey(lambda i=i: handle_choice(problem["options"][i], problem["answer"], pen), str(i + 1))

    wn.listen()  # Listen for key presses
    wn.mainloop()


def create_enemy():
  enemy = turtle.Turtle()
  enemy.shape("circle")
  enemy.color("red")
  enemy.penup()
  x = random.randint(-290, 290)
  y = random.randint(100, 250)
  enemy.goto(x, y)
  enemies.append(enemy)


def restart_game():
  global score

  # Reset the game
  player.goto(0, -250)
  player.showturtle()
  score = 0
  score_display.clear()
  score_display.write("Score: {}".format(score),
                      align="center",
                      font=("Courier", 16, "normal"))

  for enemy in enemies:
    enemy.hideturtle()
  enemies.clear()

  print("Game Restarted")
  game_loop()  # Restart the game loop

def continue_game():
  global score
  # Reset the game
  player.goto(0, -250)
  player.showturtle()

  for enemy in enemies:
    enemy.hideturtle()
  enemies.clear()

  print("Game Continued")# Restart the game loopq
  game_loop()

# Keyboard bindings
wn.listen()
wn.onkey(lambda: player.setx(player.xcor() - player_speed), "Left")
wn.onkey(lambda: player.setx(player.xcor() + player_speed), "Right")
wn.onkey(lambda: fire_bullet(), "space")
wn.onkey(restart_game, "r")  # Press 'r' to restart the game
wn.onkey(continue_game,"q")

# Main game loop
def game_loop():
  global score

  try:
    wn.update()

    # Move the enemies
    # Move the enemies
    for enemy in enemies:
      y = enemy.ycor()
      y -= 2
      enemy.sety(y)

      # Check if any enemy reaches the bottom
      if y < -240:  # Adjust this value as needed
        print("Game Over - Enemy reached the bottom")
        for e in enemies:
          e.hideturtle()
        time.sleep(1)
        display_question(generate_calculus_problem())# Stops the game loop
    
        

      if is_collision(bullet, enemy):
        bullet.hideturtle()
        enemy.hideturtle()
        enemies.remove(enemy)
        score += 10
        score_display.clear()
        score_display.write("Score: {}".format(score),
                            align="center",
                            font=("Courier", 16, "normal"))
        print("Enemy Destroyed")

    # Move the bullet
    if bullet.isvisible():
      y = bullet.ycor()
      y += bullet_speed
      bullet.sety(y)

      if bullet.ycor() > 290:
        bullet.hideturtle()

    # Create a new enemy every 5 seconds
    if len(enemies) == 0 or wn.frames % 300 == 0:
      create_enemy()

    if player.isvisible():
      wn.ontimer(game_loop, 10)
      wn.frames += 1

  except turtle.Terminator:
    pass


def fire_bullet():
  if not bullet.isvisible():
    x = player.xcor()
    y = player.ycor()
    bullet.goto(x, y)
    bullet.showturtle()


def is_collision(t1, t2):
  distance = t1.distance(t2)
  if distance < 15:
    return True
  return False


# Start the game loop
wn.frames = 0
game_loop()

# Start the turtle main loop
turtle.mainloop()
