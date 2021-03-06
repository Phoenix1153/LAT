import torch 
import torch.nn as nn
from torch.autograd import Variable
import torchvision
import torchvision.transforms as transforms
from torchvision.utils import save_image  
from pathlib import Path
import matplotlib.pyplot as plt
import numpy
import pickle

toImg = transforms.ToPILImage()

# Device configuration
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Hyper parameters
num_epochs = 5
num_classes = 10
batch_size = 100
learning_rate = 0.01
eps = 0.3
output_dir = './img/'
# MNIST dataset
train_dataset = torchvision.datasets.MNIST(root='./data/',
                                           train=True, 
                                           transform=transforms.ToTensor(),
                                           download=False)

test_dataset = torchvision.datasets.MNIST(root='./data/',
                                          train=False, 
                                          transform=transforms.ToTensor())

# Data loader
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size, 
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size, 
                                          shuffle=False)

# Convolutional neural network (two convolutional layers)
class LeNet(nn.Module):
    def __init__(self, num_classes=10):
        super(LeNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = nn.Linear(7*7*32, num_classes)
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out

model = LeNet(num_classes).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
def train():
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):
            images = images.to(device)
            labels = labels.to(device)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if (i+1) % 200 == 0:
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                       .format(epoch+1, num_epochs, i+1, total_step, loss.item()))
    # Save the model checkpoint
    torch.save(model.state_dict(), 'model.pth')


# Test the model
def test():
    model.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
    with torch.no_grad(): # cut off gradient
        correct = 0
        total = 0
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        print('Test Accuracy of the model on the 10000 test images: {} %'.format(100 * correct / total))
    # Save the model checkpoint
    torch.save(model.state_dict(), 'model.pth')
    
    model.train()

'''# this function still has bugs

def fgsm_generate():
    correct = 0
    total = 0
    correct_adv = 0
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)
        images.requires_grad_()
        outputs = model(images)
        loss = criterion(outputs,labels)
        
        #loss.backward()
        _,prediction = torch.max(outputs,1)

        #FGSM
        images_grad = torch.sign(images.grad)
        images_adv = torch.clamp(images.detach() + eps*images_grad, 0, 1)
        outputs_adv = model(images)
        _,prediction_adv = torch.max(outputs_adv.data,1)
        total += labels.size(0)
        correct_adv += (prediction_adv == labels).sum().item()
        correct += (prediction == labels).sum().item()


    print('Before FGSM Test Accuracy on the 10000 test images: {} %'.format(100 * correct / total))
    print('After FGSM Test Accuracy on the 10000 test images : {} %'.format(100 * correct_adv / total))
            
'''

def fgsm():
    model.eval()

    images_all = list()
    adv_all = list()
    correct = 0
    correct_cln = 0
    correct_adv = 0
    total=0
    for images,labels in test_loader:
        x = Variable(images, requires_grad = True).to(device)
        y_true = Variable(labels, requires_grad = False).to(device)

        h = model(x)
        _, predictions = torch.max(h,1)
        correct_cln += (predictions == y_true).sum()
        loss = criterion(h, y_true)
        model.zero_grad()
        if x.grad is not None:
            x.grad.data.fill_(0)
        loss.backward()
        
        #FGSM
        #x.grad.sign_()   # change the grad with sign ?
        x_adv = x.detach() + eps * torch.sign(x.grad)
        x_adv = torch.clamp(x_adv,0,1)
        
        h_adv = model(x_adv)
        _, predictions_adv = torch.max(h_adv,1)
        correct_adv += (predictions_adv == labels).sum()

        images_all.append([x.data.view(-1,28,28).detach().cpu(), labels])
        adv_all.append([x_adv.data.view(-1,28,28).cpu(), predictions_adv])

        correct += (predictions == predictions_adv).sum()
        total += len(predictions)
    
    model.train()
    error_rate = float(total-correct)*100/total
    print("Error Rate is ",float(total-correct)*100/total)
    print("Before FGSM the accuracy is",float(100*correct_cln)/total)
    print("After FGSM the accuracy is",float(100*correct_adv)/total)

    return images_all, adv_all, error_rate

def save(images_all, adv_all):
    #save adversarial examples
    image, label = images_all[0]
    image_adv, label_adv = adv_all[0]
    tot = len(image)
    for i in range(0, tot):
        im = toImg(image[i].unsqueeze(0))
        im.save(Path('img/eps_{}/{}_clean.jpg'.format(eps,i)))
        im = toImg(image_adv[i].unsqueeze(0))
        im.save(Path('img/eps_{}/{}_adver.jpg'.format(eps,i)))

def display(images_all, adv_all):
    # display a batch adv
    curr, label = images_all[0]
    curr_adv, label_adv = adv_all[0]
    disp_batch = 10
    for a in range(disp_batch):
        plt.figure()
        plt.subplot(121)
        plt.title('Original Label: {}'.format(label[a].cpu().numpy()),loc ='left')
        plt.imshow(curr[a].numpy(),cmap='gray')
        plt.subplot(122)
        plt.title('Adv Label : {}'.format(label_adv[a].cpu().numpy()),loc ='left')
        plt.imshow(curr_adv[a].numpy(),cmap='gray')
        plt.show()
    total=batch_size
    correct=(label==label_adv).sum()
    print("Batch Error rate ",float(total-correct)*100/total)

def draw(error_rate = error_rate, ):


#train()
model.load_state_dict(torch.load('model.pth'))
#test()
images_all, adv_all, error_rate = fgsm()
save(images_all, adv_all)
#display(images_all, adv_all)


with open('clean.p','wb') as f:
	pickle.dump(images_all[0], f, pickle.HIGHEST_PROTOCOL)

with open('eps_{}.p'.format(eps),'wb') as f:
	pickle.dump(adv_all[0], f, pickle.HIGHEST_PROTOCOL)
