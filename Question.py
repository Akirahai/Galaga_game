import json
import turtle
import random
import time

class Text(turtle.Turtle):
    
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.goto(0, 50)
        

def generate_calculus_problem():
    # Load problems from a JSON file
    with open('data/question.json') as f:
        question = json.load(f)
    
    problems = question["data"]
    # Select a random problem
    problem = random.choice(problems)
    return problem

