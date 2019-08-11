from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.app import App
from kivy.graphics import Rectangle


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.root = RelativeLayout()



        animated_icon2 = Image(source='loading.gif')
        animated_icon2.bind(texture=self.update_texture2)

        self.r2 = Rectangle(texture=animated_icon2.texture, size=(1280, 800), pos=(0, 0))
        self.root.canvas.add(self.r2)
    #     animated_icon = Image(source='test.gif')
    #     animated_icon.bind(texture=self.update_texture)

    #     self.r = Rectangle(texture=animated_icon.texture, size=(500, 255), pos=(100, 100))
    #     self.root.canvas.add(self.r)
    # def update_texture(self, instance, value):
    #     self.r.texture = value
    def update_texture2(self, instance, value):   
        self.r2.texture = value

    def build(self):
        return self.root


if __name__ == '__main__':
    MainApp().run()