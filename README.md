# Face Swap Image
Face swap image with 1 line of code. 

Takes in a filepath, PIL image, or numpy array and outputs a PIL image of result image. 

Try out the Web Demo: [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/tonyassi/face-swap)

![faceswap1](https://github.com/user-attachments/assets/9fdac61d-78b3-4ba8-848a-4028e3766b60)


## Installation
```bash
pip install -r requirements.txt
```
Requires Python 10+

## Usage

Import module
```python
from SegCloth import segment_clothing
```

Import PIL and open image
```python
from PIL import Image
image = Image.open('image.jpg')
```

![](https://cdn.discordapp.com/attachments/1120417968032063538/1202309847287345253/image-1.jpg?ex=65e8accd&is=65d637cd&hm=f42cd1095001982434a3b05907409ef8d3a380a860a7c7e079ab82f558842697&)
---

### Segment Clothing
- **img** input image of type PIL
```python
result = segment_clothing(img=image)
result.save('segmented.png')
```
![](https://cdn.discordapp.com/attachments/1120417968032063538/1202309847543185499/segmented-1.png?ex=65e8accd&is=65d637cd&hm=eed593adeca5b6d37ae2576499d5e142e4117f9c3f7bbd076d5cb575655e0efc&)

You can also explicitly specify which clothes to segment
- **img** input image of type PIL
- **clothes** (optional) list of strings. by default ["Hat", "Upper-clothes", "Skirt", "Pants", "Dress", "Belt", "Left-shoe", "Right-shoe", "Scarf"]
```python
result = segment_clothing(img=image, clothes= ["Hat", "Upper-clothes", "Skirt", "Pants", "Dress", "Belt", "Left-shoe", "Right-shoe", "Scarf"])
result.save('segmented.png')
```

### Batch Segment Clothing

- **img_dir** image folder
- **out_dir** output folder where the segmented images will go
- **clothes** (optional) list of strings. by default ["Hat", "Upper-clothes", "Skirt", "Pants", "Dress", "Belt", "Left-shoe", "Right-shoe", "Scarf"]
```python
batch_segment_clothing(img_dir="images", out_dir="output", clothes= ["Hat", "Upper-clothes", "Skirt", "Pants", "Dress", "Belt", "Left-shoe", "Right-shoe", "Scarf"])
```
