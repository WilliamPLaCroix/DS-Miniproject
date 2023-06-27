# checkpoint functions
import torch


def checkpoint(model, filename):
    torch.save(model.state_dict(), filename)


def resume(model, filename):
    model.load_state_dict(torch.load(filename))


def load_model(ModelClass, filename):
    model = ModelClass()
    model.load_state_dict(torch.load(filename))
    return model
