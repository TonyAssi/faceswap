# Face Swap Image
Face swap image with 1 line of code. 

Takes in a filepath, PIL image, or numpy array and outputs a PIL image of result image. 

Try out the Web Demo: [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/tonyassi/face-swap)

![faceswap1](https://github.com/user-attachments/assets/9fdac61d-78b3-4ba8-848a-4028e3766b60)

## Download
Download the .zip file or use the command line
```bash

```

## Installation
```bash
pip install -r requirements.txt
```
Requires Python 3.10+

## Usage

Import module
```python
from face_swap import swap_faces
```


- **src_img** source face *(filepath, PIL image, numpy array)*
- **dest_img** target image *(filepath, PIL image, numpy array)*
```python
out = swap_faces(src_img="src.jpg", dest_img="dest.jpg")
out.save("output.jpg")
```
The output is a PIL image
