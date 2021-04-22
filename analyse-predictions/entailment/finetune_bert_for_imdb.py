
# 3 epochs trainen = 15 minuten ongeveer op de gpu 

from torch.utils.data import DataLoader
from transformers import DistilBertForSequenceClassification, AdamW, DistilBertTokenizerFast
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pathlib import Path
import pdb

NUM_EPOCHS = 3
DEVICE = torch.DEVICE('cuda') if torch.cuda.is_available() else torch.DEVICE('cpu')

def read_imdb_split(split_dir):
    split_dir = Path(split_dir)
    texts = []
    labels = []
    for label_dir in ["pos", "neg"]:
        for text_file in (split_dir/label_dir).iterdir():
            texts.append(text_file.read_text())
            labels.append(0 if label_dir == "neg" else 1)
    return texts, labels


def compute_accuracy(labels, logits): 
    """
        Predicted: tensor with logits [[], [], []] of shape [batch_size, label_size]
    """
    accuracy = (logits.max(1).indices  == labels).sum().item() / logits.size(0)

    return accuracy

    # accuracy_score 
    # accuracy_score(y_true, ypredicted)



# dict_keys(['input_ids', 'attention_mask', 'labels']) train_dataset[0]
class IMDbDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


# -------------- train model ----------------------------------
def train(model, optim, train_loader, DEVICE, num_epochs=3): 
    epoch_loss = 0 
    epoch_acc = 0 
    for batch in train_loader:
        optim.zero_grad()
        input_ids = batch['input_ids'].to(DEVICE)
        attention_mask = batch['attention_mask'].to(DEVICE)
        labels = batch['labels'].to(DEVICE)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        logits = outputs.logits 
        
        # add the loss to the item. 
        epoch_loss += loss.item()

        # compute the accuracy 
        accuracy_score = compute_accuracy(labels, logits)
        epoch_acc += accuracy_score

        loss.backward()
        optim.step()

    
    print("total loss {0} and accuracy {1}".format(epoch_loss/len(train_loader), epoch_acc/len(train_loader)  ))
    return epoch_loss/len(train_loader), epoch_acc / len(train_loader)
    

def evaluate(model, valid_loader, DEVICE): 

    epoch_loss = 0 
    epoch_acc = 0 

    with torch.no_grad(): 

        for batch in valid_loader: 
            input_ids = batch['input_ids'].to(DEVICE)
            attention_mask = batch['attention_mask'].to(DEVICE)
            labels = batch['labels'].to(DEVICE)
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            logits = outputs.logits 
            
            # add the loss to the item. 
            epoch_loss += loss.item()

            # compute the accuracy 
            accuracy_score = compute_accuracy(labels, logits)
            epoch_acc += accuracy_score
            
    print("total loss {0} and accuracy {1}".format(epoch_loss/len(train_loader), epoch_acc/len(train_loader)  ))
    return epoch_loss/len(train_loader), epoch_acc / len(train_loader)



def main(): 

    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    train_texts, train_labels = read_imdb_split('aclImdb/train')
    test_texts, test_labels = read_imdb_split('aclImdb/test')
    train_texts, val_texts, train_labels, val_labels = train_test_split(train_texts, train_labels, test_size=.2)


    train_encodings = tokenizer(train_texts, truncation=True, padding=True)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True)

    train_dataset = IMDbDataset(train_encodings, train_labels)
    val_dataset = IMDbDataset(val_encodings, val_labels)
    test_dataset = IMDbDataset(test_encodings, test_labels)



    print("------------training --------------------------------------")
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    valid_loader = DataLoader(val_dataset, batch_size = 16, schuffle=True)
    
    model.to(DEVICE)
    model.train()
    optim = AdamW(model.parameters(), lr=5e-5)
    for epoch, _ in enumerate(range(NUM_EPOCHS),1):
        print("------- epoch {0}".format(epoch))
        
        train(model, optim, train_loader, DEVICE)
    print("training is finished")


    print("=============evaluating ========================================")
    model.eval()
    for epoch, _ in enumerate(range(NUM_EPOCHS),1):
         print("------- epoch {0}".format(epoch))
         evaluate(model, valid_loader, DEVICE)


main()