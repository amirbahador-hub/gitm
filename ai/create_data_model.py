import numpy as np
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Step 1: Data Collection
commit_messages = [
    # "Update release notes",
    # "Add Traditional Chinese translation",
    # "Fix relative path of dist on frontend",
    # "Comment out ci bug",
    # "Include HTTP 205 in status codes with no body",
]  # List of commit messages
git_emojis = [
    # ":memo:",
    # ":globe_with_meridians:",
    # ":bug:",
    # ":bug:",
    # ":sparkles:",
]  # List of corresponding git emojis

with open('data.json') as json_data:
    fastapi_commits = json.load(json_data)
    json_data.close()

for commit in fastapi_commits:
    commit_messages.append(commit["message"])
    git_emojis.append(commit["emoji"])

print(len(commit_messages))
print(len(git_emojis))
# Step 2: Data Preprocessing
tokenizer = Tokenizer()
tokenizer.fit_on_texts(commit_messages)
vocab_size = len(tokenizer.word_index) + 1

sequences = tokenizer.texts_to_sequences(commit_messages)
max_sequence_length = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

# Convert git emojis to numerical labels
emoji_labels = np.array([git_emojis.index(emoji) for emoji in git_emojis])

# Step 3: Model Architecture
embedding_dim = 100  # Define the dimensionality of the word embeddings
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_sequence_length),
    tf.keras.layers.LSTM(units=128),
    tf.keras.layers.Dense(len(git_emojis), activation='softmax')
])

# Step 4: Training
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(padded_sequences, emoji_labels, epochs=10, validation_split=0.2)
model.save('my_model.keras')
# Step 5: Evaluation (Optional)
# Evaluate the model on a separate test set if available

# Step 6: Inference
# def predict_git_emoji(commit_message):
#     sequence = tokenizer.texts_to_sequences([commit_message])
#     padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length)
#     predicted_label = model.predict(padded_sequence)[0]
#     predicted_emoji = git_emojis[np.argmax(predicted_label)]
#     return predicted_emoji

# Example usage
# commit_message = "Fixed a bug in the login feature"
# predicted_emoji = predict_git_emoji(commit_message)
# print(f"Predicted Git Emoji: {predicted_emoji}")