import os
import json
import click
from PIL import Image

@click.command()
@click.option('--image_dir', prompt='Image Folder')
@click.option('--label_dir', prompt='Label Folder')
@click.option('--output_file', prompt='Output File')
@click.option('--base_url', prompt='Base url')
def convert_yolo_to_label_studio(image_dir, label_dir, output_file, base_url):
    data_root = []

    for image_file in os.listdir(image_dir):

        im_w, im_h = Image.open(os.path.join(image_dir,image_file)).size

        image_url = base_url + image_file
        label_path = os.path.join(label_dir, image_file.replace('.jpg', '.txt'))

        data_obj = {
            "data": {
                "image": image_url,
            },
            "predictions":[]
        }

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                prediction = {
                    "model_version": "one",
                    "result": []
                }

                lines = f.readlines()

                for line in lines:
                    line = line.strip().split(' ')
                    class_id = int(line[0])

                    result_obj = {
                        "original_widht": im_w,
                        "original_height": im_h,
                        "image_rotation": 0,
                        "value": {
                            "x": float(line[1]) * 100,
                            "y": float(line[2]) * 100,
                            "width": float(line[3]) * 100,
                            "height": float(line[4]) * 100,
                            "rotation": 0,
                            "rectanglelabels": [
                                "Airplane"
                            ]
                        },
                        "from_name": "label",
                        "to_name": "image",
                        "type": "rectanglelabels"
                    }
                    prediction["result"].append(result_obj)
        
            data_obj["predictions"].append(prediction)

        data_root.append(data_obj)
  
        json.dump(data_root, open(output_file, 'w'))

if __name__ == "__main__":
    convert_yolo_to_label_studio()