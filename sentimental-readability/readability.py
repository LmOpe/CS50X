# TODO
import math


def main():
    # Get text from user
    text = input("Text: ")
    # Store the average number of letters per 100 words
    l = round(l_value(text) * 100) / 100
    # Store average number of sentences per 100 words
    s = round(s_value(text) * 100) / 100
    # Calculate the Coleman-Liau index and stores it in a variable
    index = round(((0.0588 * l) - (0.296 * s)) - 15.8)

    # Check for grade and output appropriately
    # For grade above 16
    if (index > 16):
        print("Grade 16+")
    # Fof grade less than 1
    elif (index < 1):
        print("Before Grade 1")
    # For grade 1-16
    else:
        print(f"Grade {index}")


# Counts the number of letters and returns the number as output
def count_letters(text):
    letter_length = 0
    for char in text:
        if (char.isalpha()):
            letter_length += 1
    return letter_length


# Count the number of words and return the number as output
def count_words(text):
    word_length = 0
    for char in text:
        if (char == ' '):
            word_length += 1
    return word_length + 1


# Counts the number of sentences and returns the number as output
def count_sentences(text):
    sentence_length = 0
    for char in text:
        if (char == '.' or char == '!' or char == '?'):
            sentence_length += 1
    return sentence_length


# Finds the average number of letters per 100 words and returns it as output
def l_value(text):
    l = float((count_letters(text) / count_words(text)) * 100)
    return l


# Finds the average number of sentences per 100 words and returns it as output
def s_value(text):
    s = float((count_sentences(text) / count_words(text)) * 100)
    return s


main()