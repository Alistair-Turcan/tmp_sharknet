import streamlit as st
import numpy as np
import os
os.system("pip install matplotlib")
import matplotlib.pyplot as plt
from PIL import Image
import torch
import torchvision.models as models
import torchvision.transforms as transforms


#put in saliencyfunction
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.329, 0.324, 0.325])
#inverse transform to get normalize image back to original form for visualization
inv_normalize = transforms.Normalize(
    mean=[-0.485/0.229, -0.456/0.224, -0.406/0.255],
    std=[1/0.229, 1/0.224, 1/0.255]
)

def saliency(img, model):
    #we don't need gradients w.r.t. weights for a trained model
    for param in model.parameters():
        param.requires_grad = False
    
    #set model in eval mode
    model.eval()
    #transoform input PIL image to torch.Tensor and normalize
    transform = torchvision.transforms.Compose([transforms.ToPILImage(),
                                                       transforms.Resize((128, 128)),
                                                       transforms.ToTensor(),
                                                normalize])

    input = transform(img)
    input.unsqueeze_(0)

    #we want to calculate gradient of higest score w.r.t. input
    #so set requires_grad to True for input 
    input.requires_grad = True
    #forward pass to calculate predictions
    preds = model(input)
    print(preds)
    score, indices = torch.max(preds, 1)
    #backward pass to get gradients of score predicted class w.r.t. input image
    score.backward()
    #get max along channel axis
    slc, _ = torch.max(torch.abs(input.grad[0]), dim=0)
    #normalize to [0..1]
    slc = (slc - slc.min())/(slc.max()-slc.min())

    #apply inverse transform on image
    with torch.no_grad():
      input_img = inv_normalize(input[0])
    #plot image and its saleincy map
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(np.transpose(img.detach().numpy(), (1, 2, 0)))
    plt.xticks([])
    plt.yticks([])
    plt.subplot(1, 2, 2)
    plt.imshow(slc.numpy(), cmap=plt.cm.hot)
    plt.xticks([])
    plt.yticks([])
    plt.savefig('output_thermo.jpg',bbox_inches='tight')
    
st.set_page_config(page_title="Thermograph Processing")
#st.sidebar.header("Thermograph Processing")
st.title("Thermograph Processing")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
st.image(
    uploaded_file, caption=f"Original image", use_column_width=True,
)

#process the image thru the stuff
MODEL_SAVE_PATH = "../sharknet.pt"
model = models.resnet18(num_classes=2)
model.load_state_dict(torch.load(MODEL_SAVE_PATH))
salient_image = torch.from_numpy(np.asarray(Image.open(uploaded_file)).T)



saliency(img, model)

salient_image = "output_thermo.png"

probability = 0
st.write("Probability of tumor presence: " + str(probability) + "%.")
st.write("Processed Image")
st.write("Red dots indicate points of interest.")
st.image(
    salient_image, caption=f"Processed image", use_column_width=True,
)
