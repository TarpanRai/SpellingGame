import random


def main():
    words_list = []
    num_words = int(input("Enter the number of words: "))

    for _ in range(num_words):
        word = input("Enter a word: ").lower()  # Convert to lowercase
        words_list.append(word)  # Store words as strings

    # Replace a random letter in each word with '_'
    modified_words = []
    original_words = words_list.copy()

    for word in words_list:
        if word:  # Ensure the word is not empty
            index = random.randint(0, len(word) - 1)  # Pick a random index
            modified_word = list(word)
            modified_word[index] = '_'  # Replace with '_'
            modified_words.append(''.join(modified_word))

    # Display the modified words
    print("\nHere are your words with missing letters:")
    for word in modified_words:
        print(word)

    # Ask the user to fill in the missing words
    for i, word in enumerate(modified_words):
        user_guess = input(f"Enter the full word for: {word}: ").lower()  # Convert input to lowercase
        if user_guess == original_words[i]:
            print("Correct!")
        else:
            print(f"Wrong! The correct word was '{original_words[i]}'")


if __name__ == "__main__":
    main()
