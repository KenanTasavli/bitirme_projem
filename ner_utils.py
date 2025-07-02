# ner_utils.py   (D:\py\ner_utils.py)
import re, torch, pathlib
from dataset_bilstm import LABEL2ID
from train_bilstm_crf import BiLSTM_CRF, vocab       # bu dosyalar da D:\py içinde

# ------- dosya yolları -------
ROOT       = pathlib.Path(__file__).resolve().parent        # = D:\py
MODEL_PT   = ROOT / "my_ner_model" / "bilstm_crf2.pt"       # tam yol
# --------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"
id2lab = {v: k for k, v in LABEL2ID.items()}

_model = BiLSTM_CRF(len(vocab), len(LABEL2ID)).to(device)
_model.load_state_dict(torch.load(MODEL_PT, map_location=device))
_model.eval()

def predict_address(text: str) -> list[str]:
    """Tweet metninden LOC span listesi döndürür."""
    tokens = re.findall(r"\S+", text)
    ids    = torch.tensor([[vocab.get(w.lower(), 1) for w in tokens]],
                          dtype=torch.long, device=device)
    mask   = torch.ones_like(ids, dtype=torch.bool, device=device)
    with torch.no_grad():
        pred = _model.decode(ids, mask)[0]

    spans, cur = [], []
    for w, lab_id in zip(tokens, pred):
        lab = id2lab[lab_id]
        if lab == "B-LOC":
            if cur: spans.append(" ".join(cur)); cur = []
            cur.append(w)
        elif lab == "I-LOC" and cur:
            cur.append(w)
        else:
            if cur: spans.append(" ".join(cur)); cur = []
    if cur: spans.append(" ".join(cur))
    return spans
