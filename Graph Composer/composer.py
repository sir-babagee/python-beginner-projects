import random
import string
from graph import Graph, Vertex


def get_words_from_text(text_path):
    with open(text_path, 'r') as f:
        text = f.read()

        # this is saying turn whitespaces into a space
        text = ' '.join(text.split())
        text = text.lower()

        text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split()
    return words


def make_graph(words):
    g = Graph()
    previous_word = None

    for word in words:
        word_vortex = g.get_vertex(word)

        if previous_word:
            previous_word.increment_edge(word_vortex)

        previous_word = word_vortex

    g.generate_probability_mappings()
    return g


def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition


def main():
    words = get_words_from_text(
        r"C:\Users\hp\Documents\P. Languages and G. Development\Python\Work\Beginner Python Projects\Graph Composer\texts\dummy.txt")

    g = make_graph(words)

    composition = compose(g, words, 100)

    # returns a string, where all words are seperated by a space!
    return ' '.join(composition)


if __name__ == '__main__':
    print(main())
