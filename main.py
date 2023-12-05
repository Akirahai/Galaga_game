import turtle
import time
import random
import string

from Character import *

pen = Text()
class Game:
    def __init__(self):
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
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}", align="left", font=("Arial", 14, "normal"))
        
        self.number_of_enemies = 5
        

        self.enemies = []
        self.letters = []
        self.stupids = []
        
        self.boss_appeared = False
        self.type_boss = False
        self.type_fight = False

        self.game_running = False
        
        self.number_of_words = 10
        
        self.boss_attack_speed = 5
    
        
    def create_enemy(self, n):
        for i in range(n):
            enemy = Enemy()
            self.enemies.append(enemy)
        
    
    
    
    
    def restart_game(self):
        self.player.clear()
        self.tboss.clear()
        self.wn.clear()
        self.__init__()
        self.menu()
    
            
    def continue_game(self):
        self.player.goto(0, -250)
        self.player.showturtle()
        self.player.reward_bullet(3)
        
        Enemy.speed = 1
        self.number_of_enemies = 5

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
        
        print("Game Continued")
        self.game_loop()
        
        
    def menu(self):
        Game.A = False
        self.mess.write("Press S to start the game", align="center", font=("Arial", 16, "normal"))
        bgm()
        turtle.onkeypress(self.start_game, "s")
    
    
    def start_game(self):
        self.game_running = True
        self.mess.clear()
        self.game_loop()
        turtle.onkeypress(None, "s")

    def create_letter(self, n):
        alph = list(string.ascii_lowercase)
        for i in range(n):
            char = random.choice(alph)
            l = Letter(char)
            alph.remove(char)
            self.letters.append(l)
    
    def game_loop(self):
        try:
                
            if self.game_running:
                self.wn.update()

                # Move bullets
                for bullet in self.player.bullets:
                    y = bullet.ycor()
                    y += 20  # bullet speed
                    bullet.sety(y)

                    if bullet.ycor() > 290 and bullet in self.player.bullets:
                            bullet.hideturtle()
                            bullet.clear()
                            self.player.bullets.remove(bullet)


                if self.type_fight:

                    if self.type_boss == False:
                        self.tboss = Boss()
                        self.create_letter(self.number_of_words)
                        pen.color('red')
                        
                        time.sleep(1)
                        pen.write("TYPE OR DIE!!!!", align="center", font=("Bakery", 20, "normal"))
                        
                    
                    self.type_boss = True
                    for enemy in self.enemies:
                        enemy.hideturtle()
                        enemy.clear()
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                    
                    if self.boss_appeared:
                        for fire in self.boss.fire_bullets:
                            fire.hideturtle()
                            fire.clear()
                            if fire in self.boss.fire_bullets:
                                self.boss.fire_bullets.remove(fire)

                    if len(self.letters) == 0:
                        self.tboss.hideturtle()
                        self.letters.clear()
                        self.player.reward_bullet(3)
                        Letter.speed += 1
                        self.number_of_words += 1
                        pen.clear()
                        self.type_fight = False
                        self.type_boss = False

                    for letter in self.letters:
                        if letter.alive:
                            letter.clear()
                            y = letter.ycor()
                            y -= Letter.speed
                            letter.sety(y)
                            letter.write(letter.string, align='center', 
                                        font=('Arial', 20, 'bold'))
                            
                            if y < -300:
                                pen.clear()
                                pen.color("red")
                                for l in self.letters:
                                    l.hideturtle()
                                    l.clear()
                                if l in self.letters:
                                    self.letters.remove(l)
                                pen.write(f"GAME OVER. You got {self.score}. Amazing, good job", align='center', font=('Impact', 14, 'normal'))
                                time.sleep(2)
                                self.restart_game()
                                break
                        else:
                            letter.clear()
                            self.letters.remove(letter)

                else:

                    # Create a new enemy every 5 seconds
                    if len(self.enemies) == 0 or self.wn.frames % 300 == 0:
                        self.create_enemy(self.number_of_enemies)

                    
                    if self.score > 0 and self.score % 100 == 0 and not self.boss_appeared:
                        self.boss = Boss()
                        Enemy.speed += 2
                        self.number_of_enemies+= 3
                        self.boss_appeared = True
                        print(Enemy.speed)

                    # Boss fight logic
                    if self.boss_appeared:
                        if len(self.boss.fire_bullets) == 0 or self.wn.frames % 200 == 0:
                            self.boss.fire_player(self.player, 4)
                        
                        for bullet in self.player.bullets:
                            if bullet.isvisible() and bullet.distance(self.boss) < 40:
                                bullet.hideturtle()
                                self.boss.reduce_hp()
                                if bullet in self.player.bullets:
                                    self.player.bullets.remove(bullet)
                                print("Boss HP:", self.boss.hp)
                                self.boss_appeared = not self.boss.die()
                                
                        for fire in self.boss.fire_bullets:
                            y = fire.ycor()
                            y -= self.boss_attack_speed  # Adjust enemy speed
                            fire.sety(y)
                            
                            if self.player.is_attacked(fire):
                                self.type_fight = True
                            if fire.ycor() < -300:
                                fire.hideturtle()
                                if fire in self.boss.fire_bullets:
                                    self.boss.fire_bullets.remove(fire)

                                
                        if self.boss.die():
                            # self.boss.hideturtle()
                            # self.boss.clear()
                            self.score += 50
                            self.boss_attack_speed += 2
                            self.score_display.clear()
                            self.score_display.write(f"Score: {self.score}", align="left", font=("Arial", 14, "normal"))
                            self.player.reward_bullet(10)
                            for fire in self.boss.fire_bullets:
                                fire.hideturtle()
                                fire.clear()

                    
                    # Move stupid

                    if self.wn.frames % 100 == 0:
                        s = Stupid('char/literallyme.gif')
                        self.stupids.append(s)

                    for stupid in self.stupids:
                        y = stupid.ycor()
                        y -= Stupid.speed
                        x = stupid.xcor()
                        x += random.randint(1,2)
                        if x > 290:
                            x = -290
                        stupid.setx(x)
                        stupid.sety(y)
                        if y < -300:
                            stupid.hideturtle()
                            if stupid in self.stupids:
                                self.stupids.remove(stupid)  
                    
                    
                    # Move enemies
                    for enemy in self.enemies:
                        y = enemy.ycor()
                        y -= Enemy.speed
                        x = enemy.xcor()
                        x += random.randint(1,2)
                        if x > 290:
                            x = -290
                        enemy.setx(x)
                        enemy.sety(y)

                        if self.player.is_attacked(enemy):
                            self.type_fight = True
                            
                        if y < -300:
                            enemy.hideturtle()
                            if enemy in self.enemies:
                                self.enemies.remove(enemy)   

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

                
                if self.player.isvisible():  ## Check if the player character is visible on the screen
                    # Schedule the game_loop method to be called again after 10 milliseconds
                    self.wn.ontimer(self.game_loop, 10)
                    # Increment the frames attribute to keep track of the number of iterations
                    self.wn.frames += 1    

        except turtle.Terminator:
            pass



game = Game()
game.menu()
turtle.mainloop()



