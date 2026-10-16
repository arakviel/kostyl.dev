import os
import shutil
import torch
import torch.nn.functional as F
from torchviz import make_dot
from PIL import Image

TARGET_DIR = "public/images/ai-python/pytorch-intro/tensors-and-autograd"
os.makedirs(TARGET_DIR, exist_ok=True)

# 1. Step: Reorganize existing images so numbers don't clash
# 08.png -> 11.png (3D loss surface)
# 06.png -> 07.png (Matmul vs elementwise)
# 05.png -> 06.png (Broadcasting)
# We use temporary names to avoid overwriting

shutil.copyfile(os.path.join(TARGET_DIR, "08.png"), os.path.join(TARGET_DIR, "11.png"))
shutil.copyfile(os.path.join(TARGET_DIR, "06.png"), os.path.join(TARGET_DIR, "07.png"))
shutil.copyfile(os.path.join(TARGET_DIR, "05.png"), os.path.join(TARGET_DIR, "06.png"))
print("Moved existing images to 06, 07, 11")

def style_and_save(dot, out_path):
    dot.attr(dpi='300', bgcolor='#FFFFFF', rankdir='TB', nodesep='0.5', ranksep='0.6')
    dot.attr('node', fontname='Helvetica, Arial, sans-serif', fontsize='12', shape='box', style='filled,rounded', penwidth='1.5')
    dot.attr('edge', color='#64748B', penwidth='1.2', arrowsize='0.8')
    
    # render without adding .png to dot name
    base_name = out_path.replace(".png", "")
    dot.render(base_name, format="png", cleanup=True)
    print(f"Generated: {out_path}")

# Graph 1 -> 05.png: clone() graph
w = torch.tensor([2.0, 4.0], requires_grad=True)
w_cloned = w.clone()
loss1 = (w_cloned * 3).sum()
dot1 = make_dot(loss1, params={"w (оригінал)": w})
style_and_save(dot1, os.path.join(TARGET_DIR, "05.png"))

# Graph 2 -> 08.png: Polynomial f(x, y) = x^2 + 3xy + y^2
x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)
z = x**2 + 3*x*y + y**2
dot2 = make_dot(z, params={"x (скаляр)": x, "y (скаляр)": y})
style_and_save(dot2, os.path.join(TARGET_DIR, "08.png"))

# Graph 3 -> 09.png: Linear model MSE loss L = (wx + b - y)^2
w_lin = torch.tensor(0.5, requires_grad=True)
b_lin = torch.tensor(0.2, requires_grad=True)
x_lin = torch.tensor(3.0)
y_lin_true = torch.tensor(2.0)
y_pred = w_lin * x_lin + b_lin
loss_lin = (y_pred - y_lin_true) ** 2
dot3 = make_dot(loss_lin, params={"w (вага)": w_lin, "b (зміщення)": b_lin})
style_and_save(dot3, os.path.join(TARGET_DIR, "09.png"))

# Graph 4 -> 10.png: detach() edge severance
x_det = torch.tensor(2.0, requires_grad=True)
y_det = x_det ** 3
y_detached = y_det.detach()
loss_det = y_detached * 5 + x_det
dot4 = make_dot(loss_det, params={"x": x_det, "y_detached (відокремлено)": y_detached})
style_and_save(dot4, os.path.join(TARGET_DIR, "10.png"))

# Graph 5 -> 12.png: Linear regression with MmBackward0 and MseLossBackward0
torch.manual_seed(42)
X = torch.randn(100, 1)
y_true = 3 * X + 2 + torch.randn(100, 1) * 0.3
w_reg = torch.randn(1, 1, requires_grad=True)
b_reg = torch.randn(1, requires_grad=True)
y_reg_pred = X @ w_reg + b_reg
loss_reg = F.mse_loss(y_reg_pred, y_true)
dot5 = make_dot(loss_reg, params={"w (матриця 1x1)": w_reg, "b (вектор 1)": b_reg})
style_and_save(dot5, os.path.join(TARGET_DIR, "12.png"))

print("All 12 images ready in directory!")
