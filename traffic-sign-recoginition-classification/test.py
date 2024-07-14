import torch

file_path = 'weights/best.pt'
model_weights = torch.load(file_path)

keys = model_weights.keys()
print(keys)

for key in keys:
    print(f"Key: {key}")
    print(model_weights[key])
    print("\n")