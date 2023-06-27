from torch import nn


# define the Network
class MyNetwork(nn.Module):
    def __init__(self, lr=0.0001):
        super(MyNetwork, self).__init__()
        self.learning_rate = lr

        self.network = nn.Sequential(
            nn.Linear(10, 100),
            nn.ReLU(),
            nn.Linear(100, 500),
            nn.ReLU(),
            nn.Linear(500, 100),
            nn.ReLU(),
            nn.Linear(100, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)
