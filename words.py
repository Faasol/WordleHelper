import math
import operator
from tqdm import tqdm
from tabulate import tabulate
from constant import *

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

def findSolutions(words, guess, pattern):
    result = []
    for word in words:
        if isMatch(word, guess, pattern):
            result.append(word)
    return result

def getProbabilitySolutions(words, guess, pattern):
    result = findSolutions(words, guess, pattern)
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
            possibleSolutions = findSolutions(possibleSolutions, guess, pattern)
            attempt = attempt + 1
            print("\nComputing entropy...")
            entropy = allEntropy(possibleSolutions)
            printTable(entropy)
            
    print("Hai indovinato la parola!")

if __name__ == '__main__':    
    main()