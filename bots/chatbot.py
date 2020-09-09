from bots import model_talking
import re
import tensorflow as tf
import pickle
import numpy as np

class ChatBot:

    def __init__(self):
        NUM_LAYERS = 2
        D_MODEL = 256
        NUM_HEADS = 8
        UNITS = 512
        DROPOUT = 0.1

        self.MAX_LENGTH = 40

        with open('bots/files_for_models/tokenizer_talking.pickle', 'rb') as f:
            self.tokenizer = pickle.load(f)

        self.START_TOKEN, self.END_TOKEN = [self.tokenizer.vocab_size], [self.tokenizer.vocab_size + 1]

        self.VOCAB_SIZE = self.tokenizer.vocab_size + 2

        self.answer_model = model_talking.transformer(
            vocab_size=self.VOCAB_SIZE,
            num_layers=NUM_LAYERS,
            units=UNITS,
            d_model=D_MODEL,
            num_heads=NUM_HEADS,
            dropout=DROPOUT)

        self.answer_model.load_weights('bots/files_for_models/model_weights_talking.h5')

    @staticmethod
    def preprocess_sentence(sentence):
        sentence = sentence.lower().strip()
        # creating a space between a word and the punctuation following it
        # eg: "he is a boy." => "he is a boy ."
        sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
        sentence = re.sub(r'[" "]+', " ", sentence)
        # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
        sentence = re.sub(r"[^a-zA-Z?.!,]+", " ", sentence)
        sentence = sentence.strip()
        # adding a start and an end token to the sentence
        return sentence

    def evaluate(self, sentence):
        sentence = self.preprocess_sentence(sentence)

        sentence = tf.expand_dims(
            self.START_TOKEN + self.tokenizer.encode(sentence) + self.END_TOKEN, axis=0)

        output = tf.expand_dims(self.START_TOKEN, 0)

        for i in range(self.MAX_LENGTH):
            predictions = self.answer_model(inputs=[sentence, output], training=False)

            # select the last word from the seq_len dimension
            predictions = predictions[:, -1:, :]
            predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

            # return the result if the predicted_id is equal to the end token
            if tf.equal(predicted_id, self.END_TOKEN[0]):
                break

            # concatenated the predicted_id to the output which is given to the decoder
            # as its input.
            output = tf.concat([output, predicted_id], axis=-1)

        return tf.squeeze(output, axis=0)

    def predict(self, sentence):
        prediction = self.evaluate(sentence)

        predicted_sentence = self.tokenizer.decode(
             [i for i in prediction if i < self.tokenizer.vocab_size])
            #
            # print('Input: {}'.format(sentence))
            # print('Output: {}'.format(predicted_sentence))
        return predicted_sentence
