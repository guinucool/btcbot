# Importação dos módulos de aprendizagem necessários para a construção do modelo
import torch.nn as nn
import torch.optim as optim
import torch

# Classe que define um modelo de redes neurais
class LinearModel(nn.Module):

    # Construtor do modelo pretendido
    def __init__(self, input_layer: int, result_layer: int, activation = None, loss = None, optimizer: optim.Optimizer = None, hidden_layers: list = None):

        # Inicialização do super construtor
        super(LinearModel, self).__init__()

        # Verificação de validade dos conteúdo das hidden_layers
        for elem in hidden_layers:
            if elem is not int:
                raise ValueError('Given hidden layers are invalid!')

        # Criação da lista de layers inicial
        layers = [ input_layer ] + hidden_layers + [ result_layer ]

        # Criação do conteúdo inicial do modelo
        self.__layers = []

        # Criação das várias camadas da estrutura do modelo
        for i in range(0,len(layers)):
            self.__layers.append(nn.Linear(layers[i], layers[i+1]))

        # Armazenamento do tamanho pretendido para entrada
        self.__entry_size = input_layer

        # Caso não tenha sido definido uma função de ativação
        if activation is None:
            activation = nn.ReLU()
        
        # Criação da função de ativação
        self.__activation = activation

        # Caso não tenha sido definida uma função de perda
        if loss is None:
            loss = nn.CrossEntropyLoss()

        # Caso não tenha sido definida uma função de otimização
        if optimizer is None:
            optimizer = optim.Adam

        # Associação das propriedades de treino
        self.__criterion = loss
        self.__optimizer = optimizer

    # Definição da execução de informação no modelo
    def forward(self, x):

        # Verificação do tamanho das entradas
        if x.size(0) != self.__entry_size:
            raise ValueError('Entry values for model are invalid!')
        
        # Transformação dos valores de entrada numa entrada vertical
        x = x.view(x.size(0), -1)

        # Aplicação da entrado pelas layers do modelo
        for index, layer in enumerate(self.__layers):

            # Aplicação da entrada sobre a camada
            x = layer(x)

            # Aplicação da entrada sobre a função de ativação
            if index != (len(self.__layers) - 1):
                x = self.__activation(x)

        # Devolução das entradas após a aplicação do modelo
        return x
    
    # Função de treino do modelo
    def train(self, train_data: list, epochs: int, info: bool):

        # Troca para o modo de treino
        super().train()

        # Execução das várias épocas de treino
        for epoch in range(epochs):

            # Execução das batches de treino
            for i, (entry_data, expected_data) in enumerate(train_data):

                # Restauro da matriz de otimização para o novo batch
                self.__optimizer.zero_grad()

                # Criação das previsões de treino do modelo
                outputs = self(entry_data)

                # Cálculo da perda do treino e retroceço para melhoria
                loss = self.__criterion(outputs, expected_data)
                loss.backward()

                # Atualização dos pesos do modelo
                self.__optimizer.step()

                # Impressão de informação relativa ao progresso do treino
                if (i+1) % 100 == 0 and info:
                    print(f'Epoch [{epoch+1}/{epochs}], Step [{i+1}/{len(train_data)}], Loss: {loss.item():.4f}')

    # Função que avalia o modelo treinado
    def evaluate(self, eval_data: list) -> float:

        # Troca para o modo de avaliação
        super().eval()

        # Criação de um contexto sem cálculo de gradientes
        with torch.no_grad():

            # Variáveis armazenadoras de resultados
            correct = 0
            total = 0

            # Avalia todos os conteúdos presentes na lista de testes
            for entry_data, expected_data in eval_data:

                # Criação de resultados do modelo
                outputs = self(entry_data)

                # Criação de previsões do modelo
                _, predicted = torch.max(outputs.data, 1)
                
                # Contagem dos resultados obtidos
                total += expected_data.size(0)
                correct += (predicted == expected_data).sum().item()

            # Devolução da pontuação obtida
            return correct / total
        
    # Função que faz uma previsão dado um conjunto de valores
    def predict(self, data: torch.Tensor) -> dict:
        
        # Troca para o modo de avaliação
        super().eval()

        # Criação de um contexto sem cálculo de gradientes
        with torch.no_grad():

            # Criação de resultados do modelo
            outputs = self(data)

            # Criação de previsões do modelo
            multiplier, predicted = torch.max(outputs.data, 1)

            # Devolução da pontuação obtida
            return predicted, multiplier