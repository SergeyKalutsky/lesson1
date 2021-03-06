import torch
from torchvision import datasets, transforms
from tqdm import tqdm
import torch.nn.functional as F


def train(model, device, train_loader, optimizer, epoch):
    model.train()
    for data, target in tqdm(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()


def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in tqdm(test_loader):
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    all_data = len(test_loader.dataset)
    percent_correct = 100. * correct / len(test_loader.dataset)
    print(f'\nСредняя точность: {correct}/{all_data} ({percent_correct}%)')
    print(f'\nСреднее значение функции потерь: {test_loss}')


def get_data_loaders():
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])

    train_data = datasets.MNIST('./', train=True, download=False, transform=transform)
    test_data = datasets.MNIST('./', train=False, transform=transform)

    train_loader = torch.utils.data.DataLoader(train_data, batch_size=64)
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=64)
    return train_loader, test_loader