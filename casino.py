import random  
# import of the __package__ inside the python 
import sys
from threading import Timer # Timer is a class from Python’s standard library   under the Module: threading
#   this is to get the counter running for the response time 
import json
import os
# constant variables using snake case 
nb_python=None
nb_user=None
user_name=None
user_money= 10
nb_attempts=1
user_bet= 0
response=None
level=1
max_level=10  # Out bound of the number in the level. 
max_attempts=3

# def is used to declare the function  here its without parameters 
# here the indentation is important in python
def welcome():
    global user_name
    print("Welcome to the Casino!")
    user_name = input("Please enter your name: ")  # saisi au clavier 
    check_user()
    
   


def check_user():
    if os.path.exists("log_history.json"):
        with open("log_history.json", "r") as file:
            try:
                data = json.load(file)  # load existing JSON
            except json.JSONDecodeError:
                print("No valid data found.")
                return

        # Initialize
        best_level = -1
        best_attempts = []
        if user_name in data:
        # Iterate only through the current user's attempts
            for attempt in data[user_name]:
                if attempt["level"] > best_level:
                    best_level = attempt["level"]
                    best_attempts = [attempt]  # reset list with new max
                elif attempt["level"] == best_level:
                    best_attempts.append(attempt)  # add to list

            # Print best attempts for this user
            print(f"🔥 Best level achieved for {user_name}: {best_level}\n")
            for attempt in best_attempts:
                print(f"Attempts: {attempt['attempts']}")
                print(f"Level: {attempt['level']}")
                print(f"User Bet: {attempt['user_bet']}")
                print(f"User Money: {attempt['user_money']}")
                print("-----------------------")
        else : 
            return


def time_out(): # this is not a pre defined method, this function is called exactly 20 second after the timer.start() function is called. 
    print("\n⏰ 20 seconds passed. Sorry, better luck next time.")
    sys.exit() # getting out of the system from this point if the time excceds  and this function runs in background thread

def python_number():
    global nb_python, max_level,user_bet, user_money
     # here the f is used for the formatted string literals    
    print(f"Hello, {user_name}! You have ${user_money} to start with.")
    user_bet= int(input(f"{user_name}, you have ${user_money}. How much would you like to bet? "))
    nb_python = random.randint(1, max_level)
    # randint is used to generate random integer between the two values 
    # here 1 and 100 inclusive 
    # print(nb_python) # for testing purposes only


def user_number():
    # here this function allows the user to input a number between 1 and 10 and count the number of attempts
    global nb_user, nb_attempts, user_money, user_bet, response, max_attempts, level, max_level
    while True:
        try:
            if nb_attempts <=max_attempts:  # is the user always have the number of attempts left. 
              
                if user_bet > user_money:
                    print(f"You cannot bet more than you have, {user_name}. Please enter a valid bet.")
                    continue
                print(f"Attempt {nb_attempts} of {max_attempts}.")
                if(nb_user == nb_python):
                    if(nb_attempts>3):
                        
                        new_bet= user_bet/2
                        user_money= user_money-user_bet
                        user_money= user_money+new_bet
                
                   
                    response= input(f"You have already guessed the correct number! you have {user_money} so do u want to move to next level ? y/n: ")
                    write_log()
                    print(f"ur choice is {response}")
                    if(response == 'y' or response == 'Y'):
                        level += 1
                        print(f"your level is {level}")
                        max_level += 10 
                        nb_attempts=1
                        python_number()
                        max_attempts=max_attempts+2  # number of attempts for level 1 is 3 and level 2 is 5 and for level 3 its 7 number of attempts. thats why its added with 2 
                        print(f"The Python has chosen its number between 1 and {max_level}.")
                        user_number()
                        if(nb_attempts== max_attempts):  
                            print(f"Thank you for playing with us see you next time ")
                            write_log()
                            return
                        elif(nb_attempts>max_attempts):  
                            print(f"Welcome to level {level}. The Python has chosen a new number between 1 and {max_level}.")
                    elif(response == 'n' or response == 'N'):
                        print(f"Thank you for playing, {user_name}! Your final account balance is ${user_money}.") 
                        write_log()
                        break

                timer = Timer(20, time_out)  
                timer.start() #Here i m starting the timer for the 20 seconds countdown 
                nb_user = int(input(f"{user_name}, please choose a number between 1 and {max_level}: "))
                             
                timer.cancel()
                if 0 <= nb_user <= max_level:
                        compare_numbers()
                                 
                else:
                    print(f"Number must be between 1 and {max_level}. Try again.")
            else :
                    user_money=user_money - user_bet                  
                    print(f"Sorry {user_name}, you've exceeded the maximum number of attempts. The correct number was {nb_python} and now your account is {user_money}.")
                    write_log()
                    return
          
        except ValueError:
            print(f"Invalid input. Please enter an integer between 1 and {max_level}.")

def write_log():
    new_attempt_dict = {
        "attempts": nb_attempts,
        "level": level,
        "user_bet": user_bet,
        "user_money": user_money
    }

    # Step 1: Load existing data if the file exists
    if os.path.exists("log_history.json"):
        with open("log_history.json", "r") as file:
            try:
                data = json.load(file)  # load existing JSON
            except json.JSONDecodeError:
                # If file is empty or corrupted, start fresh
                data = {}
    else:
        data = {}

    # Step 2: Append new attempt for the user
    if user_name in data:
        data[user_name].append(new_attempt_dict)
    else:
        data[user_name] = [new_attempt_dict]

    # Step 3: Write updated data back to file
    with open("log_history.json", "w") as file:
        json.dump(data, file, indent=4)

def compare_numbers():
    global user_bet, nb_attempts, user_money
    new_money=0
    if nb_python == nb_user:
       if(nb_attempts == 1):
            new_money = user_bet * 2
            user_money=user_money-user_bet
            user_money=new_money+user_money
            print(f"Congratulations {user_name}! You guessed the correct number. You win  {user_money}.")
            write_log()
       elif(nb_attempts == 2):
            new_money = user_bet
            user_money=user_money-user_bet
            user_money=new_money+user_money
            print(f"Well done {user_bet}! You guessed the correct number. You win {user_money}.")
            write_log()
       elif(nb_attempts == 3):
            new_money = user_bet / 2
            user_money=user_money-user_bet
            user_money=new_money+user_money
            print(f"Good job {user_name}! You guessed the correct number. You win {user_money}.")
            write_log()
       elif(nb_attempts > max_attempts):
            input(f"Thank you for your participation Do u want to move to the next level. Type y for Yes or N for no: ")
            write_log()
    else:
        if(nb_user<nb_python):
            print(f"Your number is too low. Try again.  ")
            nb_attempts+=1
        elif(nb_user>nb_python):
            print(f"Your number is too high. Try again. ")
            nb_attempts+=1
       
# Main program execution
welcome()
python_number()
print(f"The Python has chosen its number between 1 and {max_level}.")
user_number()

