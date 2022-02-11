# -*- coding: utf-8 -*-
""" Author: Ahmad Alzeitoun, The University of Bonn
    Date created: 07/2021
    Status: Production
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import transformers
from transformers import AutoModel, BertTokenizerFast

import time

# specify GPU
device = torch.device("cuda")

"""# Import BERT Model and BERT Tokenizer"""

# import BERT-base pretrained model
bert = AutoModel.from_pretrained('bert-base-uncased')

# Load the BERT tokenizer
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

"""# Freeze BERT Parameters"""

# freeze all the parameters
for param in bert.parameters():
    param.requires_grad = False

"""# Define Model Architecture"""

class BERT_Arch(nn.Module):

    def __init__(self, bert):

      super(BERT_Arch, self).__init__()

      self.bert = bert

      # dropout layer
      self.dropout = nn.Dropout(0.1)

      # relu activation function
      self.relu =  nn.ReLU()

      # dense layer 1
      self.fc1 = nn.Linear(768,512)

      # dense layer 2 (Output layer)
      self.fc2 = nn.Linear(512,2)

      #softmax activation function
      self.softmax = nn.LogSoftmax(dim=1)

    #define the forward pass
    def forward(self, sent_id, mask):

      #pass the inputs to the model
    #   _, cls_hs = self.bert(sent_id, attention_mask=mask)
      cls_hs = self.bert(sent_id, attention_mask=mask)[1]

      x = self.fc1(cls_hs)

      x = self.relu(x)

      x = self.dropout(x)

      # output layer
      x = self.fc2(x)

      # apply softmax activation
      x = self.softmax(x)

      return x

# pass the pre-trained BERT to our define architecture
model = BERT_Arch(bert)

# push the model to GPU
model = model.to(device)

# optimizer from hugging face transformers
from transformers import AdamW

# define the optimizer
optimizer = AdamW(model.parameters(), lr = 1e-3)

"""# Find Class Weights"""

from sklearn.utils.class_weight import compute_class_weight
from transformers import AdamW
optimizer = AdamW(model.parameters(), lr = 1e-3)



#######################
#### Prediction types:
# 0: Select
# 1: ASK
#######################
def pred_questionType(nlQuestion):
    """# Load Saved Model"""
    #load weights of best model
    path = 'model/saved_weights_intentTag.pt'
    model.load_state_dict(torch.load(path))

    """# Get Predictions for given question"""
    # question text
    #question_text = ["Where Eistein was born?"]
    question_text = [nlQuestion]
    # encode the question
    question_tokens = tokenizer.batch_encode_plus(question_text, padding=True)
    # covert to tensors
    question_seq = torch.tensor(question_tokens['input_ids'])
    question_mask = torch.tensor(question_tokens['attention_mask'])

    # get predictions for the question
    with torch.no_grad():
        preds = model(question_seq.to(device), question_mask.to(device))
        preds = preds.detach().cpu().numpy()

    preds = np.argmax(preds, axis = 1)
    #print("prediction", preds)
    #print(preds[0])
    return preds[0]


# q = "Where Eistein was born?"
# pred_questionType(q)
