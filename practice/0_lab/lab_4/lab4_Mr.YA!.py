import random
#random.seed(10)

genone_number = int(input("number of genone: "))
lenth = int(input("lenth of genone: "))
print("\n")

random_genome_list_write = open("random_genome_list.txt", "w")

number = 0
for i in range(genone_number):
  number += 1
  sex = random.choice("FM")
  genone = random.choice("ATCG")
  for j in range(lenth - 1):
    genone += random.choice("ATCG")
  random_genome_list_write.write("{0},{1},{2}".format(number, sex, genone) + "\n")

random_genome_list_write.close()


random_genome_list_read = open("random_genome_list.txt", "r")

genone_list_row = random_genome_list_read.readlines()

genone_list = []

for i in range(genone_number):
  genone_list.append(genone_list_row[i].strip("\n").split(","))


AXXT_number = 0

for i in genone_list:
  # print(("{0:>" + str(len(str(genone_number))) + "}").format(i[0]), end = " ")
  print(f"{(i[0]):>{len(str(genone_number))}}", end = " ")
  if i[1] == "M":
    print("\033[34m" + i[1] + "\033[0m", end = " ")
  else:
    print("\033[31m" + i[1] + "\033[0m", end = " ")
  print(i[2], end = "   ")
    
  for j in range(len(i[2])-3):
    if (i[2][j] == "A") and (i[2][j+3] == "T"):
      AXXT_number += 1
      print (i[2][0:j] + "\033[1;93m" + i[2][j:j+4] + "\033[0m" + i[2][j+4:lenth+1], end = "   ")
  print()

print ("\n")
print ("AXXT number: ", AXXT_number)
