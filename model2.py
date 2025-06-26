import json, pandas as pd, itertools
with open("py\all_data.json", "r") as f:
    data = json.load(f)

# Her tweet → (token, tag) listesi
sentences   = [" ".join(item["word"] for item in row["labels"])   for row in data]
tags_nested = [[item["label"] for item in row["labels"]]          for row in data]

df = pd.DataFrame({"sentence": sentences, "tags": tags_nested})

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
import numpy as np

# 1) Tokenleri ve tagleri benzersiz ID’lere çevir
vocab   = {"<PAD>": 0, "<UNK>": 1}
tag2id  = {"O": 0, "B-LOC": 1, "I-LOC": 2}

def tokenize(sent, tag_seq):
    ids, t_ids = [], []
    for tok, tag in zip(sent.split(), tag_seq):
        if tok not in vocab:
            vocab[tok] = len(vocab)
        ids.append(vocab[tok])
        t_ids.append(tag2id["O" if tag=="0" else tag])
    return ids, t_ids

pairs = [tokenize(s, t) for s, t in zip(df["sentence"], df["tags"])]

X, y = zip(*pairs)

# 2) Sabit uzunluğa pad et
MAX_LEN = 100
X = pad_sequences(X, maxlen=MAX_LEN, padding="post", value=vocab["<PAD>"])
y = pad_sequences(y, maxlen=MAX_LEN, padding="post", value=tag2id["O"])

# 3) y’yi (num_tokens, num_tags) one-hot’a çevir
y = [to_categorical(seq, num_classes=len(tag2id)) for seq in y]

X_train, X_val, y_train, y_val = train_test_split(
    np.array(X), np.array(y), test_size=0.1, random_state=42
)

from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, TimeDistributed, Dense
from tensorflow.keras.models import Model

EMB_DIM  = 100
HIDDEN   = 256

inp = Input(shape=(MAX_LEN,))
emb = Embedding(len(vocab), EMB_DIM, mask_zero=True)(inp)
bi  = Bidirectional(LSTM(HIDDEN//2, return_sequences=True))(emb)
out = TimeDistributed(Dense(len(tag2id), activation="softmax"))(bi)

model = Model(inp, out)
model.compile(optimizer="adam",
              loss="categorical_crossentropy",
              metrics=["accuracy"])
model.summary()

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
]

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    batch_size=32,
    epochs=15,
    callbacks=callbacks
)

from seqeval.metrics import classification_report

def predict_tags(model, X_batch):
    pred = model.predict(X_batch)
    pred_id = pred.argmax(-1)
    true_id = y_val.argmax(-1)
    id2tag = {v:k for k,v in tag2id.items()}

    y_true = [[id2tag[i] for i in seq] for seq in true_id]
    y_pred = [[id2tag[i] for i in seq] for seq in pred_id]
    return y_true, y_pred

y_true, y_pred = predict_tags(model, X_val)
print(classification_report(y_true, y_pred, digits=4))

def ner_predict(sentence):
    tokens = sentence.split()
    ids = [vocab.get(t, vocab["<UNK>"]) for t in tokens]
    ids = pad_sequences([ids], MAX_LEN, padding="post", value=vocab["<PAD>"])
    pred = model.predict(ids).argmax(-1)[0][:len(tokens)]
    id2tag = {v:k for k,v in tag2id.items()}
    return list(zip(tokens, [id2tag[i] for i in pred]))

