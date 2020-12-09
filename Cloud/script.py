##Create a list of words from wordlist
wordlist=[]
file = 'wordlist.txt'
with open(file, 'r') as f:
    for line in f:
        line = line.rstrip("\n")    
        wordlist.append(line)

##Print the words to be outputted which will be redirected into a file later
for i in wordlist:
   str=""
   str+=(i+"-")
   print(str)
   for j in wordlist:
       str+=(j+"-")
       str+="s4fet3ch"
       print(str)
       str=(i+"-")
