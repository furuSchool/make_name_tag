import cv2
import face_recognition
import os
import numpy as np

def make_circle_frame(image, size, face_size, padding):
    h, w = image.shape[:2]
    top, right, bottom, left = face_size
    center_x = int((right + left) / 2)
    center_y = int((top + bottom) / 2)
    r = np.sqrt((right - left) ** 2 + (bottom - top) ** 2)
    r = int(r * (max(padding) + 1))

    # サイズの調整
    if w < 2*r:
        r = int(w/2)
        center_x = int(w/2)
    else:
        if center_x - r < 0:
            center_x = r
        elif center_x + r > w:
            center_x = w - r
    if h < 2*r:
        r = int(h/2)
        center_y = int(h/2)
    else:
        if center_y - r < 0:
            center_y = r
        elif center_y + r > h:
            center_y = h - r


    # 円形マスクを作成
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), r, 255, -1)

    # マスクを適用して切り抜く
    circular_image = cv2.bitwise_and(image, image, mask=mask)
    x1 = center_x - r
    y1 = center_y - r
    x2 = center_x + r
    y2 = center_y + r
    circular_img = circular_image[y1:y2, x1:x2]
    circular_img = cv2.resize(circular_img, (size*2, size*2))

    alpha_channel = mask[y1:y2, x1:x2]
    alpha_channel = cv2.resize(alpha_channel, (size*2, size*2))

    circular_img_with_alpha = cv2.merge((circular_img, alpha_channel))
    
    return circular_img_with_alpha

def make_rect_frame(image, size, face_size, padding):
    h, w = image.shape[:2]
    top, right, bottom, left = face_size
    center_x = (right + left) / 2
    center_y = (top + bottom) / 2
    box_height = bottom - top
    box_width = right - left

    # padding
    top = int(top - box_height * padding[0])
    right = int(right + box_width * padding[1])
    bottom = int(bottom + box_height * padding[2])
    left = int(left - box_width * padding[3])

    top = max(0, top)
    left = max(0, left)
    bottom = min(h, bottom)
    right = min(w, right)

    # resize
    if (bottom - top) / (right - left) > size[1] / size[0]:  # 縦長すぎる
        new_width = (bottom - top) * size[0] / size[1]
        left = int(center_x - new_width / 2)
        right = int(center_x + new_width / 2)

        # 画像がはみ出さないように調整
        if right - left > w:
            right = w
            left = 0
            new_height = (right - left) * size[1] / size[0]
            top = int(center_y - new_height / 2)
            bottom = int(center_y + new_height / 2)
        else:
            if right > w:
                left = w - (right - left)
                right = w
            elif left < 0:
                right = right - left
                left = 0
                
    else:  # 横長すぎる
        new_height = (right - left) * size[1] / size[0]
        top = int(center_y - new_height / 2)
        bottom = int(center_y + new_height / 2)

        # 画像がはみ出さないように調整
        if bottom - top > h:
            top = 0
            bottom = h
            new_width = (bottom - top) * size[0] / size[1]
            left = int(center_x - new_width / 2)
            right = int(center_x + new_width / 2)
        else:
            if bottom > h:
                top = h - (bottom - top)
                bottom = h
            elif top < 0:
                bottom = bottom - top
                top = 0

    rect_img = image[top:bottom, left:right]
    return cv2.resize(rect_img, tuple(size))

# size: rect なら[width, height], circle なら r
# shape = 'rect', 'circle'
# padding: [上,右,下,左] に付与する割合
def make_face_img(image_path, output_path, size, shape="rect", padding=[1, 1, 1, 1]): 
    image = cv2.imread(image_path)
    if image is None:
        print("画像を読み込めませんでした:", image_path)
        return None
    
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        print("顔が検出されませんでした:", image_path)

    if shape == 'rect':
        for i, face_size in enumerate(face_locations):
            face_img = make_rect_frame(image, size, face_size, padding)
            
            output_filename = f"{output_path}/{os.path.splitext(os.path.basename(image_path))[0]}_face_{i}.jpg"
            cv2.imwrite(output_filename, face_img)
            print(f"Saved face image as {output_filename}")
            return f"{output_path}/{os.path.splitext(os.path.basename(image_path))[0]}_face_{i}.jpg"
    elif shape == 'circle':
        for i, face_size in enumerate(face_locations):
            face_img = make_circle_frame(image, size, face_size, padding)
            
            output_filename = f"{output_path}/{os.path.splitext(os.path.basename(image_path))[0]}_face_{i}.png"
            cv2.imwrite(output_filename, face_img)
            print(f"Saved face image as {output_filename}")
            return f"{output_path}/{os.path.splitext(os.path.basename(image_path))[0]}_face_{i}.png"
    else:
        print(f"invalid shape: {shape}")
        return None