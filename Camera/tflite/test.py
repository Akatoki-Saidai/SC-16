#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import time
import argparse
import numpy as np
import cv2

from yolox.yolox_tflite import YoloxTFLite




def main():
    # パラメータ #################################################################
    cap_device = 0
    cap_width = 640
    cap_height = 480

    model_path = "yolox_nano_int8_quantize.tflite"
    input_shape = (416,416)
    score_th = 0.7
    nms_th = 0.7
    nms_score_th = 0.5

    fmt = cv2.VideoWriter_fourcc('m','p','4','v')
    fps = 30
    size = (cap_width, cap_height)
    write = cv2.VideoWriter('Cam.mp4', fmt, fps, size)

    # カメラ準備 ###############################################################

    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード #############################################################
    yolox = YoloxTFLite(
        model_path=model_path,
        input_shape=input_shape,
        class_score_th=score_th,
        nms_th=nms_th,
        nms_score_th=nms_score_th,
    )

    # COCOクラスリスト読み込み
    with open('coco_classes.txt', 'rt') as f:
        coco_classes = f.read().rstrip('\n').split('\n')

    while True:
        start_time = time.time()

        # カメラキャプチャ ################################################
        ret, frame = cap.read()
        if not ret:
            break
        debug_image = copy.deepcopy(frame)

        # 推論実施 ########################################################
        bboxes, scores, class_ids = yolox.inference(frame)
        elapsed_time = time.time() - start_time#推論にかかった時間

        #fps
        text = "fps " + "%.0f" % (cap.get(cv2.CAP_PROP_FPS))
        debug_image = cv2.putText(
            debug_image,
            text,
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            thickness=2,
        )
        # デバッグ描画
        debug_image = draw_debug(
            debug_image,
            elapsed_time,
            score_th,
            bboxes,
            scores,
            class_ids,
            coco_classes,
        )

        # キー処理(ESC：終了) ##############################################
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break
        # 画面保存 ####################################################
        write.write(debug_image)
        # 画面反映 #########################################################
        cv2.imshow('YOLOX ONNX Sample', debug_image)
    write.release()
    cap.release()
    cv2.destroyAllWindows()


def draw_debug(
    image,
    elapsed_time,
    score_th,
    bboxes,
    scores,
    class_ids,
    coco_classes,
):
    debug_image = copy.deepcopy(image)

    for bbox, score, class_id in zip(bboxes, scores, class_ids):
        best_score = np.max(scores)
        best_score_index =  np.argmax(scores)
        best_score_bbox = bboxes[best_score_index]
        x1, y1, x2, y2 = int(best_score_bbox[0]), int(best_score_bbox[1]), int(best_score_bbox[2]), int(best_score_bbox[3])
        center = (x1+x2)/2
        print(f"x1:{x1}, x2:{x2}, center:{center}")
        debug_image = cv2.rectangle(
            debug_image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            thickness=2,
        )

        # クラスID、スコア
        best_score = '%.2f' % best_score
        text = '%s:%s' % (str(coco_classes[int(class_id)]), best_score)
        debug_image = cv2.putText(
            debug_image,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            thickness=2,
        )

    # 推論時間
    text = 'Elapsed time:' + '%.0f' % (elapsed_time * 1000)
    text = text + 'ms'
    debug_image = cv2.putText(
        debug_image,
        text,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        thickness=2,
    )

    return debug_image


if __name__ == '__main__':
    main()
