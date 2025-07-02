# train_bilstm_crf.py
# -------------------------------------------------
#  BiLSTM-CRF modeli •EĞİTİR• ve kaydeder
#  (yalnızca dosya doğrudan çalıştırılırsa)
# -------------------------------------------------
import torch, torch.nn as nn, torch.optim as optim
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, random_split
from torchcrf import CRF
from dataset_bilstm import NERDataset, LABEL2ID

# ---- sabitler ----
JSON_PATH  = r"D:\Code\Bitirme\py\json_data\all_data_clean_son.json"
MODEL_OUT  = r"D:\Code\Bitirme\py\my_ner_model\bilstm_crf.pt"
EMB_DIM, HID_DIM = 100, 256
EPOCHS, TRAIN_RATE, SEED = 40, 0.85, 777
# -------------------

# -------- Dataset + vocab --------
ds = NERDataset(JSON_PATH)
train_len = int(TRAIN_RATE * len(ds))
torch.manual_seed(SEED)
train_ds, dev_ds = random_split(ds, [train_len, len(ds) - train_len])

vocab = {"<PAD>": 0, "<UNK>": 1}
for sent, _ in train_ds:
    for w in sent:
        vocab.setdefault(w.lower(), len(vocab))
# ---------------------------------

def collate(batch):
    sents, tags = zip(*batch)
    ids  = [[vocab.get(w.lower(), 1) for w in s] for s in sents]
    ids  = [torch.tensor(x, dtype=torch.long) for x in ids]
    tags = [torch.tensor(t, dtype=torch.long)  for t in tags]

    pad_ids = pad_sequence(ids,  batch_first=True)
    pad_tgs = pad_sequence(tags, batch_first=True, padding_value=-1)

    mask = pad_tgs != -1
    pad_tgs[~mask] = 0

    # ilk token gerçek olmalı (CRF kuralı)
    if not mask[:, 0].all():
        keep = mask[:, 0]
        pad_ids, pad_tgs, mask = pad_ids[keep], pad_tgs[keep], mask[keep]

    return pad_ids, pad_tgs, mask

train_ld = DataLoader(train_ds, batch_size=16, shuffle=True,  collate_fn=collate)
dev_ld   = DataLoader(dev_ds,   batch_size=16, shuffle=False, collate_fn=collate)

# -------- Model tanımı --------
class BiLSTM_CRF(nn.Module):
    def __init__(self, vocab_size, tagset_size):
        super().__init__()
        self.emb  = nn.Embedding(vocab_size, EMB_DIM, padding_idx=0)
        self.lstm = nn.LSTM(EMB_DIM, HID_DIM // 2, bidirectional=True, batch_first=True)
        self.fc   = nn.Linear(HID_DIM, tagset_size)
        self.crf  = CRF(tagset_size, batch_first=True)

    def _feats(self, x):
        out, _ = self.lstm(self.emb(x))
        return self.fc(out)

    def loss(self, x, y, mask):
        return -self.crf(self._feats(x), y, mask=mask)

    def decode(self, x, mask):
        return self.crf.decode(self._feats(x), mask=mask)
# --------------------------------

# ------- Eğitim yalnızca doğrudan çağrılırken ----------------------------
if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model  = BiLSTM_CRF(len(vocab), len(LABEL2ID)).to(device)
    opt    = optim.Adam(model.parameters(), lr=0.005)

    for epoch in range(1, EPOCHS + 1):
        model.train(); tot = 0
        for x, y, m in train_ld:
            x, y, m = x.to(device).long(), y.to(device).long(), m.to(device)
            loss = model.loss(x, y, m)
            opt.zero_grad(); loss.backward(); opt.step()
            tot += loss.item()
        print(f"[{epoch}/{EPOCHS}] train loss: {tot/len(train_ld):.4f}")

    # basit doğruluk
    model.eval(); correct = total = 0
    with torch.no_grad():
        for x, y, m in dev_ld:
            preds = model.decode(x.to(device), m.to(device))
            for p_seq, y_seq, m_seq in zip(preds, y, m):
                for p, y_true, mask in zip(p_seq, y_seq, m_seq):
                    if not mask: break
                    total += 1
                    if p == y_true: correct += 1
    print("Doğruluk:", correct / total)
    torch.save(model.state_dict(), MODEL_OUT)
    print("✅ Model kaydedildi:", MODEL_OUT)
# ------------------------------------------------------------------------
