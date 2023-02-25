import math
import operator
from tqdm import tqdm
from tabulate import tabulate
from constant import *

def isMatchMultipleLetters(word, guess, pattern, index):
    for i in range(len(pattern)):
        if pattern[i] == 'b' and i not in index:
            if guess[i] in word:
                return False
        else:
            if pattern[i] == 'g' and i not in index:
                if guess[i] != word[i]:
                    return False
            else:
                if (guess[i] not in word or guess[i] == word[i]) and i not in index:
                    return False
    return True

def getIndex(guess, char):
    index = []
    for i in range(len(guess)):
        if guess[i] == char:
            index.append(i)
    return index

def checkMultipleLetters(guess, pattern):
    aux = ""
    for char in guess:
        if deleteWords(guess, char):
            aux = char 
    index = getIndex(guess, aux)
    if index != []:
        if (pattern[index[0]] == 'b' and pattern[index[1]] != 'b') or (pattern[index[1]] == 'b' and pattern[index[0]] != 'b'):
            return aux
        return ""    
    return ""     
    
def deleteWords(word, char):
    return word.count(char) > 1   

def isMatch(word, guess, pattern):            
    for i in range(len(pattern)):
        if pattern[i] == 'b':
            if guess[i] in word:
                return False
        else:
            if pattern[i] == 'g':
                if guess[i] != word[i]:
                    return False
            else:
                if guess[i] not in word or guess[i] == word[i]:
                    return False
    return True

def findSolutions(words, guess, pattern, flag):
    if flag:
        char = checkMultipleLetters(guess, pattern)  
    result = []
    for word in words:
        if flag:
            if char == "":
                if isMatch(word, guess, pattern):
                    result.append(word)
            else:
                if not deleteWords(word, char):
                    index = getIndex(guess, char)
                    if isMatchMultipleLetters(word, guess, pattern, index):
                        result.append(word)
        else:
            if isMatch(word, guess, pattern):
                result.append(word)
    return result

def getProbabilitySolutions(words, guess, pattern):
    result = findSolutions(words, guess, pattern, False)
    if result == []:
        return 0
    return len(result)/len(words)

def getEntropy(words, guess, pattern):
    result = getProbabilitySolutions(words, guess, pattern) 
    if result == 0:
        return 0.0
    e = -result * math.log2(result)
    return e
    
def allEntropy(words):
    result = []
    for word in tqdm(words):
        total = 0.0
        for pattern in PATTERNS:
            total = total + getEntropy(words, word, pattern)
        result.append({"word" : word, "entropy" : total})
    return result

def printTable(entropy):
    entropy.sort(key=operator.itemgetter('entropy'),reverse=True)
    header = entropy[0].keys()
    rows =  []
    for i in range(10):
        if i < len(entropy):
            rows.append([entropy[i]["word"], entropy[i]["entropy"]])
    print("\n")
    print(tabulate(rows, header, tablefmt='grid'))
    print("\n")

def main():
    pattern = ""
    possibleSolutions = list(WORDS)
    entropy = []
    attempt = 0
    while pattern != "ggggg" and attempt < MAX_ATTEMPT:
        guess = input("Insert guess: ")
        guess = guess.lower()
        while guess not in ALLOWED_WORDS:
            guess = input("ERROR: guess not allowed.\nInsert guess: ")
            guess = guess.lower()
        pattern = input("Insert pattern: ")
        pattern = pattern.lower()
        while pattern not in PATTERNS:
            pattern = input("ERROR: pattern not allowed.\nInsert pattern: ")
            pattern = pattern.lower()
        if pattern != "ggggg":
            possibleSolutions = findSolutions(possibleSolutions, guess, pattern, True)
            attempt = attempt + 1
            print("\nComputing entropy...")
            entropy = allEntropy(possibleSolutions)
            printTable(entropy)
            
    print("Hai indovinato la parola!")

if __name__ == '__main__':    
    main()