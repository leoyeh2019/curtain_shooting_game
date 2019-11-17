import random

class color:
  BOLDRED = "\033[1;91m"
  BOLDBLUE = "\033[1;34m"
  NORMAL = "\033[0m"


HANGMAN_PICS = ['''
   +---+
       |
       |
       |
      ===''', """
   +---+
   O   |
       |
       |
      ===""", '''
   +---+
   O   |
   |   |
       |
      ===''', """
   +---+
   O   |
  /|   |
       |
      ===""", '''
   +---+
   O   |
  /|\  |
       |
      ===''', """
   +---+
   O   |
  /|\  |
  /    |
      ===""", '''
   +---+
   O   |
  /|\  |
  / \  |
      ===''']

words = "ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra".split()

def getrandomwords(wordslist):
  wordindex = random.randint(0, len(wordslist) - 1)
  return wordslist[wordindex]


def displayBoard(guesstime, secretword,alreadyguess, correct):
  #print play board
  print (HANGMAN_PICS[guesstime])
  print ("Missed word = ", end = " ")
  for i in blank:
    print (i, end = "")
  print ()

  #check if input is correct
  while True:
    guessingletter = input ("Guess a letter: ").lower()
    if len(guessingletter) > 1:
      print ("Please enter " + color.BOLDRED + "one " +color.NORMAL+"letter.")
      continue
    elif guessingletter not in "abcdefghijklmnopqrstuvwxyz":
      print ("Please enter a " + color.BOLDRED + "letter"+color.NORMAL + ".")
      continue
    elif guessingletter in alreadyguess:
      print ("You have " + color.BOLDRED+ "already guessed" + color.NORMAL + " this letter.")
      continue
    break  
  alreadyguess += guessingletter

  #check if input letter in secretword
  check = 0
  for i in range (0, len(secretword)):  
    if secretword[i] == guessingletter:
      blank[i] = " " + guessingletter + " "
      check +=1
      correct +=1
  if check == 0:
    guesstime += 1
  return guesstime, alreadyguess, correct


#main program
while True:
  print("H A N G M A N")
  secretword = getrandomwords(words)
  blank = []
  for i in range(len(secretword)):
    blank.append(" _ ")
  
  alreadyguess = ""
  guesstime = 0
  correct = 0

  while guesstime < len(HANGMAN_PICS) - 1:
    guesstime, alreadyguess, correct = displayBoard(guesstime, secretword, alreadyguess, correct)
    if correct == len(secretword):
      print(color.BOLDRED+"You win"+color.NORMAL)
      break

  if not correct == len(secretword):
    print (color.BOLDBLUE+"You lose"+color.NORMAL)
    print ("The secret word is:", secretword)
  playagain = input("Do you want to play again? Press 'y' to play again ").lower()
  if playagain == "y":
    continue
  break



