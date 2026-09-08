import os
import copy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models

# 裝置設定
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'使用裝置: {device}')

# 資料路徑
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, 'cats_and_dogs_small')
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')
test_dir = os.path.join(base_dir, 'test')

# 資料擴增與預處理
imagenet_mean = [0.485, 0.456, 0.406]
imagenet_std = [0.229, 0.224, 0.225]

train_transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.RandomRotation(40),
    transforms.RandomHorizontalFlip(),
    transforms.RandomAffine(degrees=0, translate=(0.2, 0.2), shear=20),
    transforms.ColorJitter(brightness=0.2),
    transforms.ToTensor(),
    transforms.Normalize(imagenet_mean, imagenet_std),
])

val_test_transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),
    transforms.Normalize(imagenet_mean, imagenet_std),
])

train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
val_dataset = datasets.ImageFolder(validation_dir, transform=val_test_transform)
test_dataset = datasets.ImageFolder(test_dir, transform=val_test_transform)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=20, shuffle=True, num_workers=4)
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=20, shuffle=False, num_workers=4)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=20, shuffle=False, num_workers=4)

print(f'訓練集: {len(train_dataset)} 張, 驗證集: {len(val_dataset)} 張, 測試集: {len(test_dataset)} 張')

# 建立 VGG16 模型
vgg16 = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)

# 換成二元分類器
vgg16.classifier = nn.Sequential(
    nn.Linear(512 * 7 * 7, 256),  # VGG16 avgpool 輸出為 7x7x512 = 25088
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(256, 1),
    nn.Sigmoid(),
)

# 凍結卷積基底
for param in vgg16.features.parameters():
    param.requires_grad = False

trainable_params = sum(p.numel() for p in vgg16.parameters() if p.requires_grad)
print(f'凍結卷積基底後，可訓練參數量: {trainable_params:,}')

vgg16 = vgg16.to(device)


# 訓練函式
def train_model(model, train_loader, val_loader, optimizer, criterion, epochs):
    history = {'acc': [], 'val_acc': [], 'loss': [], 'val_loss': []}

    for epoch in range(epochs):
        # --- 訓練 ---
        model.train()
        running_loss = 0.0
        running_corrects = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.float().to(device)
            optimizer.zero_grad()
            outputs = model(inputs).squeeze()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            preds = (outputs > 0.5).float()
            running_loss += loss.item() * inputs.size(0)
            running_corrects += (preds == labels).sum().item()
            total += inputs.size(0)

        epoch_loss = running_loss / total
        epoch_acc = running_corrects / total

        # --- 驗證 ---
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        val_total = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.float().to(device)
                outputs = model(inputs).squeeze()
                loss = criterion(outputs, labels)
                preds = (outputs > 0.5).float()
                val_loss += loss.item() * inputs.size(0)
                val_corrects += (preds == labels).sum().item()
                val_total += inputs.size(0)

        val_epoch_loss = val_loss / val_total
        val_epoch_acc = val_corrects / val_total

        history['acc'].append(epoch_acc)
        history['val_acc'].append(val_epoch_acc)
        history['loss'].append(epoch_loss)
        history['val_loss'].append(val_epoch_loss)

        print(f'Epoch {epoch+1}/{epochs} - '
              f'loss: {epoch_loss:.4f} - acc: {epoch_acc:.4f} - '
              f'val_loss: {val_epoch_loss:.4f} - val_acc: {val_epoch_acc:.4f}')

    return history


criterion = nn.BCELoss()

# 第一階段：只訓練分類器（30 epochs）
print('\n--- 第一階段：訓練分類器（凍結卷積基底） ---')
optimizer = optim.RMSprop(filter(lambda p: p.requires_grad, vgg16.parameters()), lr=2e-5)
history1 = train_model(vgg16, train_loader, val_loader, optimizer, criterion, epochs=30)

# 微調：解凍 block5（最後 3 個卷積層）
# block5 從 index 24 開始
print('\n--- 第二階段：微調 block5 ---')
for i, layer in enumerate(vgg16.features):
    if i >= 24:  # block5_conv1 開始
        for param in layer.parameters():
            param.requires_grad = True
    else:
        for param in layer.parameters():
            param.requires_grad = False

trainable_params = sum(p.numel() for p in vgg16.parameters() if p.requires_grad)
print(f'解凍 block5 後，可訓練參數量: {trainable_params:,}')

# 用更低的 lr 微調
optimizer = optim.RMSprop(filter(lambda p: p.requires_grad, vgg16.parameters()), lr=1e-5)
history2 = train_model(vgg16, train_loader, val_loader, optimizer, criterion, epochs=100)

# 繪製趨勢圖
acc = history2['acc']
val_acc = history2['val_acc']
loss = history2['loss']
val_loss = history2['val_loss']

epochs_range = range(1, len(acc) + 1)

# 原始曲線
plt.figure()
plt.plot(epochs_range, acc, 'bo', label='Training acc')
plt.plot(epochs_range, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.savefig(os.path.join(script_dir, 'accuracy.png'), dpi=150)

plt.figure()
plt.plot(epochs_range, loss, 'bo', label='Training loss')
plt.plot(epochs_range, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.savefig(os.path.join(script_dir, 'loss.png'), dpi=150)


# 平滑曲線（指數移動平均）
def smooth_curve(points, factor=0.8):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points


plt.figure()
plt.plot(epochs_range, smooth_curve(acc), 'bo', label='Smoothed training acc')
plt.plot(epochs_range, smooth_curve(val_acc), 'b', label='Smoothed validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.savefig(os.path.join(script_dir, 'accuracy_smoothed.png'), dpi=150)

plt.figure()
plt.plot(epochs_range, smooth_curve(loss), 'bo', label='Smoothed training loss')
plt.plot(epochs_range, smooth_curve(val_loss), 'b', label='Smoothed validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.savefig(os.path.join(script_dir, 'loss_smoothed.png'), dpi=150)

print(f'\n趨勢圖已儲存至 {script_dir}')

# 測試集評估
vgg16.eval()
test_corrects = 0
test_total = 0

with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.float().to(device)
        outputs = vgg16(inputs).squeeze()
        preds = (outputs > 0.5).float()
        test_corrects += (preds == labels).sum().item()
        test_total += inputs.size(0)

print(f'Test accuracy: {test_corrects / test_total:.4f}')
