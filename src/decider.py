import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

# Hyperparameters
input_size = 28  # MNIST image size
hidden_size = 128
num_classes = 3
num_epochs = 10
batch_size = 64
learning_rate = 0.001

import random

# Números de dados a gerar
data_size = 1000000

# Número de indicadores a gerar
indicator_size = 28

# Geração do peso dos indicadores
indicator_weight = []

for i in range(0, indicator_size):
    indicator_weight.append(random.randint(1, 20))

# Geração do dataset
dataset = []

for i in range(0, int(data_size / 100)):

    results = []

    entries = []

    for i in range(0, 100):

        entry = []

        soma = 0

        for a in range(0, indicator_size):
            entry.append(random.randint(0, 100) / 100)
            soma += (entry[a] * indicator_weight[a])

            soma = soma / (sum(indicator_weight))

        if soma > random.randint(60, 100) / 100:
            results.append(0)
        elif soma < random.randint(0, 41) / 100:
            results.append(1)
        else:
            results.append(2)

        entries.append(entry)

    dataset.append((torch.FloatTensor(entries), torch.LongTensor(results)))

test = []

for i in range(0, int(data_size / 10000)):

    results = []

    entries = []

    for i in range(0, 100):

        entry = []

        soma = 0

        for a in range(0, indicator_size):
            entry.append(random.randint(0, 100) / 100)
            soma += (entry[a] * indicator_weight[a])

            soma = soma / (sum(indicator_weight))

        if soma > random.randint(60, 100) / 100:
            results.append(0)
        elif soma < random.randint(0, 41) / 100:
            results.append(1)
        else:
            results.append(2)

        entries.append(entry)

    test.append((torch.FloatTensor(entries), torch.LongTensor(results)))

# Define the neural network architecture
class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

model = NeuralNetwork(input_size, hidden_size, num_classes)

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training the model
for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(dataset):
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        if (i+1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(dataset)}], Loss: {loss.item():.4f}')

# Evaluating the model
model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test:
        outputs = model(images)
        print(outputs.data)
        this, predicted = torch.max(outputs.data, 1)
        print(this)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    print(f'Accuracy of the model on the {total} test images: {(correct/total)*100:.2f}%')
