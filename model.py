import torch
from torch import nn

class StockPriceModel(nn.Module):
    def __init__(self, input_size=4, hidden_size=8):
        super().__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.GRU(4, hidden_size)
        self.output = nn.Linear(hidden_size+1, 1)
    
    def forward(self, tweet_data, open):
        initial_hidden = torch.zeros(1, 1, self.hidden_size)
        tweet_data = tweet_data[:1]
        print(tweet_data, initial_hidden)
        _, final_hidden = self.rnn(tweet_data.unsqueeze(1), initial_hidden)
        encoded_tweet_data = final_hidden.view(-1)
        encoded_input = torch.cat((encoded_tweet_data, open.view(1)), 0)
        print(encoded_input)
        close_pred = self.output(encoded_input)
        #print(close_pred.item())
        return close_pred.view(())
