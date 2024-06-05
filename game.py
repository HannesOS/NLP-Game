from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import euclidean, cosine
import numpy as np
from tqdm import tqdm
import time
import warnings; warnings.filterwarnings("ignore")
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.pipeline import Pipeline


class WordGuessingGame:
    def __init__(self):
        # Initialize the model and game variables
        self.model_name = "mixedbread-ai/mxbai-embed-large-v1"
        self.model = SentenceTransformer(self.model_name, trust_remote_code=True)
        self.distance_measure = euclidean
        self.vocabulary = np.loadtxt('vocabulary.txt', dtype=str, comments='.')
        self.embedding_list = self.get_embedding_list()
        self.lower_dim_embed = self.create_lower_dim_embed()
        self.reset_game()

    def get_embedding_list(self, create_embedding_list=True):
        # Load or create embedding list for the vocabulary
        if create_embedding_list:
            embedding_list = []
            print("Embedding words...")
            time.sleep(0.1)
            for word in tqdm(self.vocabulary):
                embedding_word = self.model.encode([word])[0]
                embedding_list.append(embedding_word)
            np.savetxt("embedding_list.txt", embedding_list)
        else:
            print("Loading embeddings")
            embedding_list = np.loadtxt("embedding_list.txt")
        return embedding_list

    def create_lower_dim_embed(self):
        # Reduce the dimensionality of embeddings for visualization
        n_dimensions = 3
        pipeline = Pipeline([('pca', PCA(n_components=n_dimensions)), ('normalize', Normalizer())])
        lower_dim_embed = pipeline.fit_transform(self.embedding_list)
        return lower_dim_embed

    def get_word_to_guess(self):
        # Select a random word from the vocabulary with length greater than 3
        word_to_guess = ""
        while len(word_to_guess) <= 3:
            random_number = np.random.randint(200, 10000)
            word_to_guess = self.vocabulary[random_number]
        embedding_word_to_guess = self.model.encode([word_to_guess])[0]
        return word_to_guess, embedding_word_to_guess

    def reset_game(self):
        # Reset game variables for a new round
        self.word_to_guess, self.embedding_word_to_guess = self.get_word_to_guess()
        self.sorted_words, self.sorted_similarities = self.get_word_similarities()
        self.embed_projection_word_to_guess = self.lower_dim_embed[np.argwhere(self.vocabulary == self.word_to_guess)][0][0]
        self.best_word = None
        self.best_word_rank = len(self.vocabulary) - 1
        self.best_similarity = 0
        self.number_of_guesses = 0
        self.current_word_rank = None
        self.game_won = False

    def get_word_similarities(self):
        # Calculate similarities of all vocabulary words to the word to guess
        similarities = {}
        for i, embedding_word in enumerate(self.embedding_list):
            distance = self.distance_measure(self.embedding_word_to_guess, embedding_word)
            similarities[self.vocabulary[i]] = distance
        sorted_ = np.array(sorted(similarities.items(), key=lambda x: x[1]))
        sorted_words = sorted_[:, 0]
        sorted_similarities = sorted_[:, 1].astype(float)
        return sorted_words, sorted_similarities

    def handle_guess(self, input_word):
        # Handle a guess and provide feedback
        self.number_of_guesses += 1
        if input_word == self.word_to_guess:
            self.game_won = True
            return f"Word '{input_word}'. Word found!!! Number of guesses: {self.number_of_guesses}\nPress reset to reset the game with a new word."
        else:
            rank = np.argwhere(self.sorted_words == input_word)
            if len(rank) == 0:
                self.current_word_rank = -1
                return f"Word '{input_word}' not found in vocabulary"
            rank = rank[0][0]
            self.current_word_rank = rank
            similarity = np.round(1 - self.sorted_similarities[rank] / np.max(self.sorted_similarities), 2)
            if rank < self.best_word_rank:
                self.best_word = input_word
                self.best_word_rank = rank
                self.best_similarity = similarity
            return (f"Word '{input_word}'. Rank: {rank}. Best word so far: '{self.best_word}' at rank "
                    f"{self.best_word_rank}. Guesses so far: {self.number_of_guesses}")