import random
#random.seed(10)

genone_number = int(input("number of genone: "))
genone_length = int(input("genone_length of genone: "))

print("\n")

#### Random generating and writing
random_genome_list_write = open("random_genome_list.txt", "w")

number = 0
for i in range(genone_number):
  number += 1
  sex = random.choice("FM")
  genone = random.choice("ATCG")
  for j in range(genone_length - 1):
    genone += random.choice("ATCG")
  random_genome_list_write.write("{0},{1},{2}".format(number, sex, genone) + "\n")

random_genome_list_write.close()

#### Reading
random_genome_list_read = open("random_genome_list.txt", "r")

genone_list_row = random_genome_list_read.readlines()

genone_list = []

for i in range(genone_number):
  genone_list.append(genone_list_row[i].strip("\n").split(","))

#### Output
maxIndexLength = max(len(str(i[0])) for i in genone_list)

defaultColor  = "\033[0m"
mapSexColor   = {"M": "\033[34m", "F": "\033[31m"}
def showColoredSex(sex):
  sexColor = mapSexColor[sex] if sex in mapSexColor else defaultColor
  return sexColor + sex + defaultColor

matchColor  = "\033[1;93m"
matchString = "A??T"
matchDelimiter = "  "

matchNumber = 0
def showColoredMatch(genoneStr, match, index = 0, acc = []):
  if index > len(genoneStr) - len(match): return acc

  reqMatch = genoneStr[index:len(match) + index]
  resMatch = all(map(lambda i, j: i == j if i != '?' else True, match, reqMatch))
  parseResult = [genoneStr[:index] + matchColor + reqMatch + defaultColor + genoneStr[len(match) + index:]] if resMatch else []
  return showColoredMatch(genoneStr, match, index + 1, acc + parseResult)

for i in genone_list:
  print(f"{i[0]:>{maxIndexLength}}", end = " ")
  print(f"{showColoredSex(i[1])}", end = " ")
  print(f"{i[2]}", end = "  ")
  matchList    = showColoredMatch(i[2], matchString)
  matchNumber += len(matchList)
  print(f"{matchDelimiter.join(matchList)}")

print ("\n")
print (f"{matchString} number: {matchNumber}")