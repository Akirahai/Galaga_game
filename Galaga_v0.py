import turtle
import time
import random

# Set up the screen
wn = turtle.Screen()
wn.title("Galaga")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Player
player = turtle.Turtle()
player.shape("triangle")
player.color("white")

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
  problems = [
      {
          "question": "What is the derivative of x^2?",
          "options": ["2x", "x^2", "2", "x"],
          "answer": "2x"
      },
      {
          "question": "What is the integral of 2x?",
          "options": ["x^2 + C", "2x + C", "x^2", "1"],
          "answer": "x^2 + C"
      },
      {
          "question": "What is the derivative of sin(x)?",
          "options": ["cos(x)", "-sin(x)", "cos(x) + C", "sin(x)"],
          "answer": "cos(x)"
      },
      {
          "question": "What is the integral of cos(x)?",
          "options":
          ["sin(x) + C", "-sin(x) + C", "cos(x) + C", "-cos(x) + C"],
          "answer": "sin(x) + C"
      },
      {
          "question": "What is the derivative of 3x^3?",
          "options": ["9x^2", "6x", "x^3", "3x^2"],
          "answer": "9x^2"
      },
      {
          "question": "What is the integral of 1/x?",
          "options": ["ln|x| + C", "1/x + C", "x + C", "x^2/2 + C"],
          "answer": "ln|x| + C"
      },
      {
          "question": "What is the derivative of e^x?",
          "options": ["e^x", "x*e^x", "1", "e^(x+1)"],
          "answer": "e^x"
      },
      {
          "question": "What is the integral of e^x?",
          "options": ["e^x + C", "x*e^x + C", "1 + C", "e^(x+1) + C"],
          "answer": "e^x + C"
      },
      {
          "question": "What is the derivative of cos(x)?",
          "options": ["-sin(x)", "sin(x)", "-cos(x)", "cos(x)"],
          "answer": "-sin(x)"
      },
      {
          "question": "What is the integral of sin(x)?",
          "options":
          ["-cos(x) + C", "cos(x) + C", "sin(x) + C", "-sin(x) + C"],
          "answer": "-cos(x) + C"
      },
      {
          "question": "What is the integral of 3x^2?",
          "options": ["x^3 + C", "9x + C", "x^3/3 + C", "3x^3 + C"],
          "answer": "x^3 + C"
      },
      {
          "question": "What is the derivative of ln(x)?",
          "options": ["1/x", "ln(x)^2", "x/ln(x)", "1"],
          "answer": "1/x"
      },
      {
          "question": "What is the derivative of tan(x)?",
          "options": ["sec^2(x)", "sin(x)/cos(x)", "cos^2(x)", "1+tan^2(x)"],
          "answer": "sec^2(x)"
      },
      {
          "question":
          "What is the integral of 1/(1+x^2)?",
          "options":
          ["atan(x) + C", "ln|x| + C", "1/2 ln|1+x^2| + C", "x/(1+x^2) + C"],
          "answer":
          "atan(x) + C"
      },
      {
          "question": "What is the derivative of sqrt(x) (x > 0)?",
          "options": ["1/(2sqrt(x))", "sqrt(x)/2", "2sqrt(x)", "1/2x"],
          "answer": "1/(2sqrt(x))"
      },
      {
          "question": "What is the integral of sec(x)tan(x)?",
          "options": ["sec(x) + C", "sin(x) + C", "cos(x) + C", "tan(x) + C"],
          "answer": "sec(x) + C"
      },
      {
          "question": "What is the derivative of 2^x?",
          "options": ["2^x ln(2)", "x 2^(x-1)", "2^x", "ln(2)"],
          "answer": "2^x ln(2)"
      },
      {
          "question": "What is the integral of sec^2(x)?",
          "options": ["tan(x) + C", "sec(x) + C", "sin(x) + C", "cos(x) + C"],
          "answer": "tan(x) + C"
      },
      {
          "question": "What is the limit of (sin(x)/x) as x approaches 0?",
          "options": ["1", "0", "Infinity", "Undefined"],
          "answer": "1"
      },
      {
          "question":
          "What is the derivative of the function f(x) = x^3 - 3x + 2?",
          "options": ["3x^2 - 3", "3x^2 - x", "x^2 - 3", "3x^2"],
          "answer": "3x^2 - 3"
      },
      {
          "question":
          "What is the integral of x * e^x?",
          "options":
          ["e^x (x - 1) + C", "x^2 e^x/2 + C", "e^x (x + 1) + C", "x e^x + C"],
          "answer":
          "e^x (x - 1) + C"
      },
      {
          "question": "What is the limit of (1/x) as x approaches infinity?",
          "options": ["0", "1", "Infinity", "Undefined"],
          "answer": "0"
      },
      {
          "question":
          "What is the integral of 1/cos(x)?",
          "options": [
              "ln|sec(x) + tan(x)| + C", "sec(x) + C", "tan(x) + C",
              "sin(x) + C"
          ],
          "answer":
          "ln|sec(x) + tan(x)| + C"
      },
      {
          "question":
          "What is the derivative of arcsin(x)?",
          "options":
          ["1/sqrt(1-x^2)", "sqrt(1-x^2)", "1/sqrt(1+x^2)", "x/sqrt(1-x^2)"],
          "answer":
          "1/sqrt(1-x^2)"
      },
      {
          "question":
          "What is the limit of (x^2 - 1)/(x - 1) as x approaches 1?",
          "options": ["2", "1", "0", "Undefined"],
          "answer": "2"
      },
      {
          "question": "What is the integral of ln(x)?",
          "options":
          ["x ln(x) - x + C", "x ln(x) + C", "1/x + C", "ln(x)/x + C"],
          "answer": "x ln(x) - x + C"
      },
      {
          "question": "What is the derivative of arctan(x)?",
          "options":
          ["1/(1 + x^2)", "1/(1 - x^2)", "2x/(1 + x^2)", "1/(x^2 - 1)"],
          "answer": "1/(1 + x^2)"
      },
      {
          "question": "What is the limit of (e^x - 1)/x as x approaches 0?",
          "options": ["1", "0", "e", "Infinity"],
          "answer": "1"
      },
      {
          "question":
          "What is the derivative of arccos(x)?",
          "options":
          ["-1/sqrt(1-x^2)", "1/sqrt(1-x^2)", "-sqrt(1-x^2)", "1/sqrt(1+x^2)"],
          "answer":
          "-1/sqrt(1-x^2)"
      },
      {
          "question":
          "What is the integral of 1/(x^2 + 1)?",
          "options": [
              "atan(x) + C", "ln|x| + C", "1/2 ln|x^2 + 1| + C",
              "x/(x^2 + 1) + C"
          ],
          "answer":
          "atan(x) + C"
      },
      {
          "question":
          "What is the limit of (3x^3 - 2x^2 + 4x)/(x^2) as x approaches infinity?",
          "options": ["3", "2", "Infinity", "0"],
          "answer": "Infinity"
      },
      {
          "question": "What is the derivative of a^x (where a > 0, a ≠ 1)?",
          "options": ["a^x ln(a)", "x a^(x-1)", "a^x", "ln(a)"],
          "answer": "a^x ln(a)"
      },
      {
          "question":
          "What is the integral of cos^2(x)?",
          "options": [
              "(1/2)(x + sin(x)cos(x)) + C", "(1/2)(x - sin(x)cos(x)) + C",
              "sin^2(x) + C", "1 - sin^2(x) + C"
          ],
          "answer":
          "(1/2)(x + sin(x)cos(x)) + C"
      },
      {
          "question":
          "What is the limit of (x^2 - 4)/(x - 2) as x approaches 2?",
          "options": ["4", "0", "2", "Undefined"],
          "answer": "4"
      },
  ]

  # Select a random problem
  problem = random.choice(problems)
  return problem


# What happen after answer chosen
def handle_choice(choice, correct_answer, pen):
  if choice == correct_answer:
    time.sleep(2)
    pen.hideturtle()
    pen.clear()
    pen.write("Correct! You survive.",
              align="center",
              font=("Arial", 14, "bold"))
    time.sleep(2)
    pen.hideturtle()
    pen.clear()
    continue_game()

  else:
    pen.hideturtle()
    pen.clear()
    pen.write("Wrong answer. You died.",
              align="center",
              font=("Arial", 14, "bold"))


def display_question(problem):
  # Clear the screen or reset the drawing for display question
  wn.bgcolor("black")

  pen = turtle.Turtle()
  pen.hideturtle()
  pen.penup()
  pen.color("white")
  pen.goto(0, 50)
  pen.write(problem["question"], align="center", font=("Arial", 16, "normal"))

  start_y = 30
  for i, option in enumerate(problem["options"], 1):
    pen.goto(0, start_y - 30 * i)
    pen.write(f"{i}. {option}", align="center", font=("Arial", 14, "normal"))

  # Here, implement logic to capture user's choice and check the answer
  for i in range(4):
    wn.onkey(lambda i=i: handle_choice(problem["options"][i], problem["answer"
                                                                      ], pen),
             str(i + 1))

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
  score = score
  score_display.clear()
  score_display.write("Score: {}".format(score),
                      align="center",
                      font=("Courier", 16, "normal"))

  for enemy in enemies:
    enemy.hideturtle()
  enemies.clear()

  print("Game Continued")
  pass  # Restart the game loop
  game_loop()


# Keyboard bindings
wn.listen()
wn.onkey(lambda: player.setx(player.xcor() - player_speed), "Left")
wn.onkey(lambda: player.setx(player.xcor() + player_speed), "Right")
wn.onkey(lambda: fire_bullet(), "space")
wn.onkey(restart_game, "r")  # Press 'r' to restart the game
wn.onkey(continue_game, "q")


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
        display_question(generate_calculus_problem())
        print("Game Over - Enemy reached the bottom")
        for e in enemies:
          e.hideturtle()
        time.sleep(1)
        # Stops the game loop

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
      wn.ontimer(game_loop, 1000)
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
