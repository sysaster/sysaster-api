import numpy as np
import cv2

def decode_base64_img(img_data, w, h, c):
    '''
    Decode an RGB image encoded in base64.
    '''
    img_data = base64.b64decode(img_data)
    nparr = np.fromstring(img_data, dtype=np.uint8)
    nparr = nparr.reshape(int(c) * int(h), int(w))
    b = nparr[0:int(h),:]
    g = nparr[int(h):2*int(h),:]
    r = nparr[2*int(h):3*int(h),:]
    img = cv2.merge((b, g, r))
    return img

