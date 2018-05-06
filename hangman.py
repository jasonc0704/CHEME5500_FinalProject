import time

name = raw_input("What is your name? ")

print "Hello, " + name
time.sleep(0.5)

print "This is HANGMAN!"

time.sleep(1)

print "Start guessing..."
time.sleep(0.5)

word = "dolphin"
guesses = []

turns = 10

while turns > 0:         

    space = 0             
  
    for char in word:

        if char in guesses:    
            print char,    

        else:
            print "_",     
            space += 1    


    if space == 0:        
        print "You Won!"  
        break

    print              

    guess = raw_input("guess a character:") 

    guesses += guess                    

    if guess not in word:  
        turns -= 1        
        print "Wrong"
        print "You have", + turns, 'more guesses' 
 

    if turns == 0:           
        print "You Lose!"