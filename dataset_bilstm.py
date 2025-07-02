# dataset_bilstm.py  –  JSON dosyasını PyTorch Dataset'ine dönüştürür
import json, torch
from torch.utils.data import Dataset

class NERDataset(Dataset):
    def __init__(self, path):
        data = json.load(open(path, encoding="utf8"))
        self.sents, self.tags = [], []
        for tw in data:
            words = [p["word"] for p in tw["labels"]]
            labels= [LABEL2ID[p["label"].replace("0","O")] for p in tw["labels"]]
            if words:                      # <-- boş tweetleri at
                self.sents.append(words)
                self.tags.append(labels)

LABEL2ID = {"O":0, "B-LOC":1, "I-LOC":2}

class NERDataset(Dataset):
    def __init__(self, path):
        data = json.load(open(path, encoding="utf8"))
        self.sents = [[p["word"] for p in tw["labels"]] for tw in data]
        self.tags  = [[LABEL2ID[p["label"].replace("0","O")] for p in tw["labels"]] for tw in data]

    def __len__(self): return len(self.sents)
    def __getitem__(self, idx): return self.sents[idx], self.tags[idx]
