import array
import numpy as np
import tensorflow as tf
from collections import defaultdict

def load_vocab(filename):
    vocab = None
    with open(filename) as f:
        vocab = f.read().splitlines()
    dct = defaultdict(int)
    for idx, word in enumerate(vocab):
        dct[word] = idx
    return [vocab, dct]

def load_glove_vectors(filename, vocab):
  """
  Load glove vectors from a .txt file.
  Optionally limit the vocabulary to save memory. `vocab` should be a set.
  """
  dct = {}
  vectors = array.array('d')
  current_idx = 0
  with open(filename, "r") as f:
    f.readline()
    for _, line in enumerate(f):
        tokens = line.split(" ")
        word = tokens[0]
        entries = tokens[1:]
        if not vocab or word in vocab:
            dct[word] = current_idx
            vectors.extend(float(x) for x in entries)
            current_idx += 1
    word_dim = len(entries)
    num_vectors = len(dct)
    tf.logging.info("Found {} out of {} vectors in {}".format(num_vectors, len(vocab), filename))
    return [np.array(vectors).reshape(num_vectors, word_dim), dct]


def build_initial_embedding_matrix(vocab_dict, glove_dict, glove_vectors, embedding_dim):
    np.random.seed(11)
    initial_embeddings = np.random.normal(0.0, 0.01, size=(len(vocab_dict), embedding_dim), ).astype("float32")
    initial_embeddings[0] = np.zeros(shape=[embedding_dim], dtype='float32')  # <unk> vector is 0
    # initial_embeddings[1] = np.ones(shape=[embedding_dim],dtype='float32') # <\s> vector is 1
    for word, glove_word_idx in glove_dict.items():
        word_idx = vocab_dict.get(word)
        initial_embeddings[word_idx, :] = glove_vectors[glove_word_idx]
    return initial_embeddings

# vocab, vocab_dict = load_vocab('data/vocabulary.txt')
# glove_vectors,glove_dict = load_glove_vectors('data/test.txt',vocab)
# build_initial_embedding_matrix(vocab_dict,glove_dict,glove_vectors,300)
