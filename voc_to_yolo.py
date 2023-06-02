import os
import glob
import xml.etree.ElementTree as ET
# import tqdm


def get_classes(classes_path):
    with open(classes_path, encoding='utf-8') as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names, len(class_names)


def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


if __name__ == '__main__':
    # 设置xml文件的路径和要保存的txt文件路径
    xml_root_path = r'D:\pythonItem\VOC2YOLO\VOCdevkit\dataSet\droneData\val\labels'
    txt_save_path = r'D:\pythonItem\VOC2YOLO\VOCdevkit\dataSet\droneData\val\yololabels'
    if not os.path.exists(txt_save_path):
        os.makedirs(txt_save_path)
    xml_paths = glob.glob(os.path.join(xml_root_path, '*.xml'))
    # classes_path = 'labels.txt'
    classes_path =r"D:\pythonItem\VOC2YOLO\VOCdevkit\VOC2007\labels.txt"
    classes, _ = get_classes(classes_path)

    for xml_id in xml_paths:
        txt_id = os.path.join(txt_save_path, (xml_id.split('\\')[-1])[:-4] + '.txt')
        txt = open(txt_id, 'w')
        xml = open(xml_id, encoding='utf-8')
        tree = ET.parse(xml)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = 0
            if obj.find('difficult') != None:
                difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('xmax').text)),
                 int(float(xmlbox.find('ymin').text)), int(float(xmlbox.find('ymax').text)))
            box = convert((w, h), b)
            txt.write(str(cls_id) + ' ' + ' '.join([str(a) for a in box]) + '\n')
        txt.close()