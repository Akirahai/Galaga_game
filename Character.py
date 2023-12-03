import turtle
import random
import time
import winsound



turtle.addshape('char/spaceship.gif')

turtle.addshape('char/minion.gif')

turtle.addshape('char/boss.gif')

turtle.addshape('char/bullet.gif')

turtle.addshape('char/fire.gif')

turtle.addshape('char/explosion.gif')
class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape('char/spaceship.gif')
        self.penup()
        self.goto(0, -250)
            
        self.bullets = []
        self.number_of_bullets = 10
        self.bullets_display = turtle.Turtle()
        self.bullets_display.speed(0)
        self.bullets_display.color("white")
        self.bullets_display.penup()
        self.bullets_display.hideturtle()
        self.bullets_display.goto(290, 260)
        self.bullets_display.clear()
        self.bullets_display.write(f"Bullets: {self.number_of_bullets}", align="right", font=("Arial", 14, "normal"))
        
        self.move_speed = 10  # Adjust the movement speed
        self.move_left = False
        self.move_right = False
        
        # Keyboard bindings
        turtle.listen()
        turtle.onkeypress(self.start_move_left, "Left")
        turtle.onkeypress(self.start_move_right, "Right")
        turtle.onkeyrelease(self.stop_move_left, "Left")
        turtle.onkeyrelease(self.stop_move_right, "Right")
        turtle.onkeypress(self.fire_bullet, "space")
        
        
        # Start continuous movement check
        self.move()
    def shooting_sound(self):
        winsound.PlaySound("sound/shooting.wav", winsound.SND_ASYNC)
        
    def start_move_left(self):
        self.move_left = True

    def stop_move_left(self):
        self.move_left = False

    def start_move_right(self):
        self.move_right = True

    def stop_move_right(self):
        self.move_right = False

    def move(self):
        if self.move_left:
            new_x = self.xcor() - self.move_speed
            if new_x < -280:
                new_x = -280
            self.setx(new_x)
        elif self.move_right:
            new_x = self.xcor() + self.move_speed
            if new_x > 280:
                new_x = 280
            self.setx(new_x)
        
        turtle.ontimer(self.move, 10)
        
    def fire_bullet(self):
        if self.number_of_bullets >= 1:
            bullet = Bullet()
            bullet.goto(self.xcor(), self.ycor())
            bullet.showturtle()
            self.bullets.append(bullet)
            self.number_of_bullets -= 1
            self.bullets_display.clear()
            self.bullets_display.write(f"Bullets: {self.number_of_bullets}", align="right", font=("Arial", 14, "normal"))
        else:
            pen = turtle.Turtle()
            pen.speed(0)
            pen.color("white") 
            pen.penup()
            pen.hideturtle()
            pen.goto(0, -100)
            pen.write("You have no bullet left", align="center", font=("Arial", 10, "normal"))
            turtle.ontimer(lambda: pen.clear(), 2000)  # Clears message after 2000 milliseconds (2 seconds)
            
    def reward_bullet(self, number):
        self.number_of_bullets += number
        self.bullets_display.clear()
        self.bullets_display.write(f"Bullets: {self.number_of_bullets}", align="right", font=("Arial", 14, "normal"))
        
    # def fire_double_bullet(self):
    #     bullet1 = Bullet()
    #     bullet1.goto(self.xcor() - 10, self.ycor())  # Adjust position for the first bullet
    #     bullet1.setheading(90)  # Adjust the angle if needed
    #     bullet1.showturtle()
    #     self.bullets.append(bullet1)

        # bullet2 = Bullet()
        # bullet2.goto(self.xcor() + 10, self.ycor())  # Adjust position for the second bullet
        # bullet2.setheading(90)  # Adjust the angle if needed
        # bullet2.showturtle()
        # self.bullets.append(bullet2)
        
    def is_attacked(self, enemy):
        if self.distance(enemy) < 30:  
            return True
        return False



class Bullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("char/bullet.gif")
        self.penup()
        self.hideturtle()
        
class Fire(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("char/fire.gif")
        self.penup()
        self.hideturtle()

class Explosion(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("char/explosion.gif")
        self.penup()
        self.hideturtle()
        
        
        
        
        
class Enemy(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("char/minion.gif")
        self.penup()
        self.speed = 0.25
        self.goto(random.randint(-290, 290), 280)
        self.explosion = Explosion()
    
    def disappear(self):
        self.hideturtle()
        self.explosion.goto(self.xcor(), self.ycor())
        self.explosion.showturtle()
        turtle.ontimer(lambda: self.explosion.hideturtle(), 500)
        
        
        
class Boss(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("char/boss.gif")
        self.penup()
        self.goto(0, 200)
        self.hp = 100  # Set HP attribute for the boss
        
        self.fire_bullets = []
    

    def fire_player(self, player, number):
        for i in range(number):
            fire = Fire()
            fire.goto(self.xcor(), self.ycor())
            fire.showturtle()
            self.fire_bullets.append(fire)

    def reduce_hp(self):
        self.hp -= 10  # Reduce HP by 10 upon collision with a bullet

    
    def die(self):
        if self.hp <= 0:
            self.hideturtle()
            self.clear()
            print("Boss defeated")
            return True
        else:
            return False

    def check_collision(self, bullet):
        if self.distance(bullet) < 50:  
            self.reduce_hp()
            return True
        return False
