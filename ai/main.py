import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import json


commit_messages = [
]  # List of commit messages
git_emojis = [
]  # List of corresponding git emojis
model = tf.keras.models.load_model('my_model.keras')

with open('data.json') as json_data:
    fastapi_commits = json.load(json_data)
    json_data.close()


for commit in fastapi_commits:
    commit_messages.append(commit["message"])
    git_emojis.append(commit["emoji"])

tokenizer = Tokenizer()
tokenizer.fit_on_texts(commit_messages)


sequences = tokenizer.texts_to_sequences(commit_messages)
max_sequence_length = max(len(seq) for seq in sequences)

def predict_git_emoji(commit_message):
    sequence = tokenizer.texts_to_sequences([commit_message])
    padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length)
    predicted_label = model.predict(padded_sequence)[0]
    predicted_emoji = git_emojis[np.argmax(predicted_label)]
    return predicted_emoji

# Example usage

commit_message = "Refactor, fix and update code"
commit_message = "Fixed a bug in the login feature"
predicted_emoji = predict_git_emoji(commit_message)
print(f"Predicted Git Emoji: {predicted_emoji}")