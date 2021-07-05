from transformers import BertTokenizer, BertForSequenceClassification
import torch
import pdb 

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
outputs = model(**inputs, labels=labels)
loss = outputs.loss
print(loss)
print(loss.item())
logits = outputs.logits
print(logits)
print(labels)
pdb.set_trace()
pred = logits.max(1).indices
print(pred)