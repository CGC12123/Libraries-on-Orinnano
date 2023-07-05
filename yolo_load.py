import torch

def yolo_load(path1, path2):
    model = torch.hub.load(path1, 'custom', path2, source='local', device = 0)
    return model