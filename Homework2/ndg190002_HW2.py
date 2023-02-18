import sys
import nltk
import random
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


# Create a list of stopwords from the english language
stopwords_en = nltk.corpus.stopwords.words('english')

# Define the game function 
def game():
    score = 5
    moves = 0
    word = random.choice(common_nouns)
    guessed_letters = set()
    while score > 0:
        masked_word = ''.join(['_ ' if letter not in guessed_letters else letter+' ' for letter in word])
        print(masked_word)
        letter = input("Guess a letter: ")
        if letter == '!':
            print("Thanks for playing!")
            return
        if letter in guessed_letters:
            print("You already guessed that letter. Try again.")
            continue
        guessed_letters.add(letter)
        if letter in word:
            moves += 1
            score += 1
            print(f"Correct Letter Guessed. Points: {score}")
            if set(word) == guessed_letters:
                print(f"Congratulations, you guessed the word '{word}' in {moves} moves and won with a score of {score}!")
                return
        else:
            moves += 1
            score -= 1
            print(f"Sorry, guess again. Points: {score}")
    print(f"You ran out of points in {moves} moves. The word was '{word}'. Better luck next time!")

def preprocess(textFile):
    
    # Tokenize the text file to generate list of tokens
    tokens = nltk.word_tokenize(textFile)
    # Create the set to define the unique tokens in the text file
    unq_tokens = set(tokens)
    print("Lexical diversity: %.2f" % (len(unq_tokens) / len(tokens))) # Calculate the lexical diversity of the text
    
    # Process the text to only have words that are above length 5, are words, and are not stopwords
    tokens = [t.lower() for t in tokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
    
    # get the lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    # make unique
    lemmas_unique = set([wnl.lemmatize(token) for token in tokens])

    print("The number of unique lemmas in text: ", len(lemmas_unique))

    # Add POS tags to each lemma 
    tagged_lemmas = pos_tag(list(lemmas_unique))
    # Create a list of nouns from the POS tagged lemmas
    nouns = [lemma for lemma, pos in tagged_lemmas if pos.startswith('N')]
    
    print(f"The number of tokens: {len(tokens)}")
    print(f"The number of nouns: {len(noun)}")
    
    return tokens, nouns

# Handling the anat19.txt file to be entered in as a sys arg.
data = sys.argv[1]
file_content = open(data).read()
tokens, nouns = preprocess(file_content)

# Creating a dict of nouns with the key being the count
noun_list = {}
for noun in nouns:
    count = tokens.count(noun)
    noun_list[noun] = count

# Sorts list from most common to least common noun
noun_list = sorted(noun_list.items(), key=lambda x: x[1], reverse=True)

# Prints the 50 most common noun
print("50 most common nouns:")
common_nouns = []
for i, (noun, count) in enumerate(noun_list[:50]):
    print(f"{i+1}. {noun}: {count}")
    common_nouns.append(noun)

game()

# Handling file not being specified
if len(sys.argv) < 2:
    print("Error: No file specified")
    sys.exit()

def main(args):
    # Run check to see if a file was passed using sys args
    if len(args) < 2:
        print("Error: Please specify a file path.")