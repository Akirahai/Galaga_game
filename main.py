import turtle
import time
import random
import json

from Character import *
from Question import Text, generate_calculus_problem, exploding_sound, bgm


class Game:
    global A
    
    def __init__(self):
        A = True
        self.wn = turtle.Screen()
        # self.wn.title("Galaga")
        self.wn.bgcolor("black")
        self.wn.setup(width=600, height=600)
        self.wn.tracer(0)
        self.wn.frames = 0

        self.player = Player()
        self.mess = Text()

        
        self.score = 0
        self.score_display = turtle.Turtle()
        self.score_display.speed(0)
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(-290, 260)
        self.score_display.write(f"Score: {self.score}", align="left", font=("Arial", 14, "normal"))
        
        self.velocity = 1
        self.number_of_enemies = 5
        

        self.enemies = []
        
        self.boss_appeared = False
        # self.wn.listen()
        # self.wn.onkeypress(self.player.move_left, "Left")
        # self.wn.onkeypress(self.player.move_right, "Right")
        # self.wn.onkeypress(self.player.fire_bullet, "space")

        self.game_running = False
    
        
    def create_enemy(self, n):
        for i in range(n):
            enemy = Enemy()
            self.enemies.append(enemy)
        
        
        
    def handle_choice(self, choice, answer, pen):
        for i in range (4):
            turtle.onkeypress(None, str(i + 1))
        if choice == answer:
            time.sleep(2)
            pen.clear()
            pen.write(f"Correct with your answer as {choice}. Game continue ", align="center", font=("Arial", 16, "normal"))
            time.sleep(2)
            pen.clear()
            self.continue_game()
        else:
            time.sleep(2)
            pen.clear()
            pen.write(f"Wrong with your answer as {choice}. Game Over", align="center", font=("Arial", 16, "normal"))
            time.sleep(2)
            pen.clear()
            self.end_game()
    
    
    def display_question(self, problem, wn):
        pen = Text()
        pen.write(problem['question'], align="center", font=("Arial", 16, "normal"))

        start_y = 30
        for i, option in enumerate(problem["options"], 1):
            pen.goto(0, start_y - 30*i)
            pen.write(f"{i}. {option}", align="center", font=("Arial", 14, "normal"))

        # Here, implement logic to capture user's choice and check the answer
        for i in range(4):
            turtle.onkeypress(lambda i=i: self.handle_choice(problem["options"][i], problem["answer"], pen), str(i + 1))

        turtle.listen()  # Listen for key presses
        turtle.mainloop()
    
    
    
    
    # def restart_game(self):
    #     self.mess.clear()
        
    #     turtle.onkeypress(None, "r")
        
    #     self.player.hideturtle()
    #     self.player.clear()
        
    #     self.player = Player()
        
    #     if self.boss_appeared:
    #         self.boss.hideturtle()
    #         self.boss.clear()
    #         self.boss_appeared = False
            
    #     self.enemies.clear()
    #     self.player.bullets.clear()
        
    #     self.enemies = []
    #     self.player.bullets = []
        
    #     self.velocity = 1
    #     self.number_of_enemies = 5
        
    #     self.score = 0
    #     self.score_display.clear()
    #     self.score_display.write(f"Score: {self.score}", align="left", font=("Arial", 14, "normal"))
        
    #     self.game_loop()
    
            
    def continue_game(self):
        self.player.goto(0, -250)
        self.player.showturtle()
        self.player.reward_bullet(3)
        
        self.velocity = 1
        

        if self.boss_appeared:
            self.boss.hideturtle()
            self.boss.clear()
            for bullet in self.boss.fire_bullets:
                bullet.hideturtle()
                bullet.clear()  
            self.boss_appeared = False
        
        for enemy in self.enemies:
            enemy.hideturtle()
            enemy.clear()
        
        for bullet in self.player.bullets:
            bullet.hideturtle()
            bullet.clear()
        
        self.enemies = []
        self.player.bullets = []
        
        self.number_of_enemies = 5
        print("Game Continued")
        self.game_loop()
        
    
    
        
    def menu(self):
        self.mess.write("Press S to start the game", align="center", font=("Arial", 16, "normal"))
        bgm()
        turtle.onkeypress(self.start_game, "s")
    
    
    def start_game(self):
        self.game_running = True
        self.mess.clear()
        self.game_loop()
        turtle.onkeypress(None, "s")
    
    def game_loop(self):
        try:
                
            if self.game_running:
                self.wn.update()

                
                if self.score > 0 and self.score % 100 == 0 and not self.boss_appeared:
                    self.boss = Boss()
                    self.velocity += 2
                    self.number_of_enemies+= 3
                    self.boss_appeared = True
                    print(self.velocity)

                # Boss logic
                if self.boss_appeared:
                    if len(self.boss.fire_bullets) == 0 or self.wn.frames % 400 == 0:
                        self.boss.fire_player(self.player, 2)
                    
                    for bullet in self.player.bullets:
                        if bullet.isvisible() and bullet.distance(self.boss) < 40:
                            bullet.hideturtle()
                            self.boss.reduce_hp()
                            if bullet in self.player.bullets:
                                self.player.bullets.remove(bullet)
                            print("Boss HP:", self.boss.hp)
                            self.boss_appeared = not self.boss.die()
                            
                    for fire in self.boss.fire_bullets:
                        if fire.isvisible():
                            y = fire.ycor()
                            y -= 5  # Adjust enemy speed
                            fire.sety(y)
                        if fire.ycor() < -300:
                            fire.hideturtle()
                            fire.clear()
                            if fire in self.boss.fire_bullets:
                                self.boss.fire_bullets.remove(fire)
                        if fire.distance(self.player) < 20:
                            fire.hideturtle()
                            fire.clear()
                            if fire in self.boss.fire_bullets:
                                self.boss.fire_bullets.remove(fire)
                            print("Game Over - Enemy reached the player")
                            pen = Text()
                            pen.write("Game Over - Answer this question", align="center", font=("Arial", 16, "normal"))
                            time.sleep(1)
                            pen.clear()
                            for e in self.enemies:
                                e.hideturtle()
                                e.clear()
                            time.sleep(1)
                            self.display_question(generate_calculus_problem(), self.wn)
                            
                    if self.boss.die():
                        # self.boss.hideturtle()
                        # self.boss.clear()
                        self.score += 50
                        self.score_display.clear()
                        self.score_display.write(f"Score: {self.score}", align="left", font=("Arial", 14, "normal"))
                        self.player.reward_bullet(10)
                        for fire in self.boss.fire_bullets:
                            fire.hideturtle()
                            fire.clear()
                        # time.sleep(1)
                        # pen = Text()
                        # pen.write("Game Over - Answer this question", align="center", font=("Arial", 16, "normal"))
                        # time.sleep(1)
                        # pen.clear()
                        # self.display_question(generate_calculus_problem(), self.wn)

                # Move enemies
                for enemy in self.enemies:
                    y = enemy.ycor()
                    y -= self.velocity  # Adjust enemy speed
                    x = enemy.xcor()
                    x += random.randint(1,2)
                    if x > 290:
                        x = -290
                    enemy.setx(x)
                    enemy.sety(y)

                    if self.player.is_attacked(enemy):
                        print("Game Over - Enemy reached the player")
                        pen = Text()
                        pen.write("Game Over - Answer this question", align="center", font=("Arial", 16, "normal"))
                        time.sleep(1)
                        pen.clear()
                        for e in self.enemies:
                            e.hideturtle()
                            e.clear()
                        time.sleep(1)
                        self.display_question(generate_calculus_problem(), self.wn)

                    for bullet in self.player.bullets:
                        if bullet.isvisible() and bullet.distance(enemy) < 20:
                            # exploding_sound()
                            bullet.hideturtle()
                            enemy.disappear()
                            
                            if enemy in self.enemies:
                                self.enemies.remove(enemy)
                            if bullet in self.player.bullets:
                                self.player.bullets.remove(bullet)
                            self.player.reward_bullet(3)
                            self.score += 10
                            self.score_display.clear()
                            self.score_display.write(f"Score: {self.score}", align="left", font=("Arial", 14, "normal"))
                            print("Enemy Destroyed")
                            
                        if bullet.ycor() > 300:
                            if bullet in self.player.bullets:
                                self.player.bullets.remove(bullet)
                    if y < -300:
                        enemy.hideturtle()
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)

                # Move bullets
                for bullet in self.player.bullets:
                    if bullet.isvisible():
                        y = bullet.ycor()
                        y += 20  # bullet speed
                        bullet.sety(y)

                    if bullet.ycor() > 290:
                        if bullet in self.player.bullets:
                            bullet.hideturtle()
                            bullet.clear()
                            self.player.bullets.remove(bullet)
                
                # Create a new enemy every 5 seconds
                if len(self.enemies) == 0 or self.wn.frames % 300 == 0:
                    self.create_enemy(self.number_of_enemies)

                # if self.wn.frames % 100 == 0:
                #     boss.fire_enemy(self.player)
                    
                if self.player.isvisible():
                    self.wn.ontimer(self.game_loop, 10)
                    self.wn.frames += 1

        except turtle.Terminator:
            pass

    def end_game(self):
        self.mess.write("Game Over. Press r to restart game", align="center", font=("Arial", 16, "normal"))
        turtle.onkeypress(self.restart_game(), "r")

# Rest of the code remains the same

# Usage


A = False

# game = 0
# while True:
#     if A == False:
#         game = Game()
#         game.menu()
#         turtle.mainloop()
    
   
game = Game()
game.menu()
turtle.mainloop()
# game = Game()

# game.menu()

# # Listen for the keypress to start the game
# turtle.listen()


