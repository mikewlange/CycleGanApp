import torch
import torchvision.transforms as transforms


class CycleData():
    def __init__(self, discr_x, discr_y, gen_xy, gen_yx, batch_x, batch_y):
        self.batch_x = batch_x
        self.batch_y = batch_y
        self.synthesis_x = gen_yx(batch_y)
        self.synthesis_y = gen_xy(batch_x)
        self.batch_x_predictions = discr_x(self.batch_x)
        self.batch_y_predictions = discr_y(self.batch_y)
        self.synthesis_x_predictions = discr_x(self.synthesis_x)
        self.synthesis_y_predictions = discr_y(self.synthesis_y)
        self.id_x_approximations = gen_yx(self.synthesis_y)
        self.id_y_approximations = gen_xy(self.synthesis_x)


def get_transform(image_size):
    return transforms.Compose([
        transforms.Resize(image_size),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


def get_batch_data(data_x_loader, data_y_loader, discr_x, discr_y, gen_xy,
                   gen_yx, device):
    batch_x, _ = next(iter(data_x_loader))
    batch_x = batch_x.to(device)
    batch_y, _ = next(iter(data_y_loader))
    batch_y = batch_y.to(device)
    cycle_data = CycleData(discr_x, discr_y, gen_xy, gen_yx, batch_x, batch_y)
    return cycle_data


def init_weights_gaussian(model):
    classname = model.__class__.__name__
    if classname.find('Conv') != -1:
        model.weight.data.normal_(0.0, 0.02)


def get_target(real, inverted, shape, device):
    if (real and not inverted) or (not real and inverted):
        return torch.zeros(shape).to(device)
    return torch.ones(shape).to(device)


def log_loss(loss):
    with open('log_loss.csv', 'a') as log_file:
        log_file.write(str(loss) + '\n')