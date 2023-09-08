import cv2
import numpy as np
import tensorflow as tf
from Model.modules.utils import (draw_bbox_landm, pad_input_image, recover_pad_output,save_image)


def main(file):
    model = tf.keras.models.load_model('./Model/modules/retinaface_model')
    img_path = './media/'+file
    out_path = './media/results'
    print("[*] Processing on single image {}".format(img_path))
    img_raw = cv2.imread(img_path)
    img_height_raw, img_width_raw, _ = img_raw.shape
    img = np.float32(img_raw.copy())
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # pad input image to avoid unmatched shape problem
    img, pad_params = pad_input_image(img, max_steps=max([8, 16, 32]))

    # run model
    outputs = model(img[np.newaxis, ...]).numpy()

    # recover padding effect
    outputs = recover_pad_output(outputs, pad_params)

    # draw and save results
    for prior_index in range(len(outputs)):
        draw_bbox_landm(img_raw, outputs[prior_index], img_height_raw,
                        img_width_raw)
        count = "count :: " + str(len(outputs))
        cv2.putText(img_raw, count , (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255,255))
    save_image(img_raw, out_path, image_format='jpg')
    print("count :: " + str(len(outputs)))
    return img_raw,len(outputs)