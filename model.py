import torch
import torch.nn as nn
import torchvision.models as models
from PIL import Image
from torchvision import transforms

PATH = "./model_Resnet50_bs128_lr0_001_epoch5.pt"

def preprocess(filepath):
    img = Image.open(filepath).convert("RGB")
    preprocess = transforms.Compose([
        transforms.Resize(48),
        transforms.CenterCrop(48),
        transforms.ToTensor(),
        transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])
    img_preprocessed = preprocess(img)
    img_tensor = torch.unsqueeze(img_preprocessed, 0)
    return img_tensor

def predict(tensor):
    resnet50 = models.resnet50(pretrained=True)
    num_ftrs = resnet50.fc.in_features
    resnet50.fc = nn.Linear(num_ftrs, 7)
    resnet50.load_state_dict(torch.load(PATH, map_location='cpu'))
    resnet50.eval()
    out = resnet50(tensor)
    _, index = torch.max(out, 1)
    # percentage = nn.functional.softmax(out, dim=1)[0] * 100
    return index[0]

if __name__ == "__main__":
    tensor = preprocess("./test/test.jpg")
    result = predict(tensor)
    print(result)




