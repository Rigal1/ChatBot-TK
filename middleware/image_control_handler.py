class ImageControlHandler:
    def __init__(self, image_control):
        self.image_control = image_control

    def load_image(self, path):
        return self.image_control.load_image(path)
    
    def load_resized_image(self, path, resize):
        return self.image_control.load_resized_image(path, resize)
    
    def load_expression_image(self, emotion, resize):
        return self.image_control.load_expression_image(emotion, resize)