import torch
import torch.nn as nn
import torchvision.models as models
from PIL import Image
from torchvision import transforms

PATH = "./model_Resnet50-Pretrained-12000-Dropout_bs128_lr0_001_epoch5-58-FER.pt"

def preprocess(filepath):
    img = Image.open(filepath).convert("RGB")
    preprocess = transforms.Compose([
        transforms.Resize(48),
        transforms.CenterCrop(48),
        transforms.ToTensor(),
      ])
    img_preprocessed = preprocess(img)
    img_tensor = torch.unsqueeze(img_preprocessed, 0)
    return img_tensor

def predict(tensor):
    resnet50 = models.resnet50(pretrained=True)
    num_ftrs = resnet50.fc.in_features
    # resnet50.fc = nn.Linear(num_ftrs, 7)
    resnet50.fc = nn.Sequential(
        nn.Linear(num_ftrs, 1000),
        nn.ReLU(True),
        nn.Dropout(0.4),
        nn.Linear(1000, 50),
        nn.ReLU(True),
        nn.Dropout(0.4),
        nn.Linear(50, 6)
    )
    resnet50.load_state_dict(torch.load(PATH, map_location='cpu'))
    resnet50.eval()
    out = resnet50(tensor)
    pred = out.max(1, keepdim=True)[1]
    return pred

if __name__ == "__main__":
    tensor = preprocess("./test/test3.png")
    result = predict(tensor)
    print(result)




