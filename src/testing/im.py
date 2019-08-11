from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image  
from kivy.lang import Builder  
from kivy.app import App  
from kivy.uix.floatlayout import FloatLayout  

class RootWidget(FloatLayout):
    pass

class ImageButton(ButtonBehavior, Image):  
    def on_press(self):  
        print ('pressed')

Builder.load_string("""  
<RootWidget>:  
    ImageButton:  
        source:'res/images/items/2.png'  
        size_hint: .2, .2  
""")  

class The_AssignmentApp(App):  
    def build(self):  
        return RootWidget()

if __name__ == "__main__":  
    The_AssignmentApp().run()