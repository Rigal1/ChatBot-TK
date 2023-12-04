from PIL import Image, ImageTk
import os

class ImageManager:
    def __init__(self, current_character= "chara", character_list=["chara"]):
        self.current_character = current_character
        self.character_list = character_list
        self.image_paths = {}
        self.image_cache = {}
        self.load_image_path_cache()
        self.load_image_cache()
    
    def set_character_dir(self, character):
        self.current_character = character
    
    def view_image_path_cache(self):
        print(self.image_paths)
    
    def load_image(self, image_path):
        if not os.path.isfile(image_path):
            return None
        # PILを使って画像を開きます。
        image = Image.open(image_path)
        return ImageTk.PhotoImage(image)

    def load_resized_image(self, image_path, resize):
        # PILを使って画像を開き、リサイズします。
        image = Image.open(image_path)
        image = image.resize(resize, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    
    def resize_image(self, image, resize):
        # PILを使って画像を開き、リサイズします。
        # 返り値はImageTk.PhotoImageです。
        image = image.resize(resize, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def load_expression_image(self, expression, resize):
        # ここで画像のファイルパスを選択します。実際には表情に応じた画像を返す必要があります。
        
        if expression not in self.image_paths[self.current_character].keys():
            expression = "NEUTRAL"

        image_path = self.image_paths[self.current_character][expression]
        if image_path in self.image_cache:
            return self.resize_image(self.image_cache[image_path], resize)
        else:
            image = Image.open(image_path)
            self.image_cache[image_path] = image
            return self.resize_image(image, resize)

    def load_image_cache(self):
        # 画像のキャッシュをロードします。
        # 最初にキャッシュするのは、現在のキャラクターの画像のみです。
        for image_path in self.image_paths[self.current_character].values():
            if image_path not in self.image_cache:
                self.image_cache[image_path] = Image.open(image_path)
    
    def load_image_path_cache(self):
        # 画像のパスをキャッシュします。
        for image_dir_name in self.character_list:
            self.image_paths[image_dir_name] = self.find_image(f"data/{image_dir_name}/images")
    
    def find_image(self, image_dir):
        # 画像のパスを取得します。
        # 画像のパスは、表情名で取得される
        image_paths = {}
        for file in os.listdir(image_dir):
            if os.path.isfile(os.path.join(image_dir, file)) and file.endswith(".png"):
                filename = os.path.splitext(file)[0].upper()
                image_paths[filename] = os.path.join(image_dir, file)
        return image_paths
    
if __name__ == "__main__":
    image_manager = ImageManager()
    image_manager.view_image_path_cache()
        