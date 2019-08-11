# from kivy.uix.relativelayout import RelativeLayout
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.image import Image
# from kivy.app import App
# from kivy.graphics import *
# from kivy.core.image import Image as coreImage
# import platform
# from kivy.graphics.texture import Texture
from game_manager import *
class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = RelativeLayout()
        print("origin self.size:{self.size}")
        # if platform.system() == "Darwin": #Macbook
        #     import pygame
        #     self.size = (self.w,self.h) = pygame.display.get_surface().get_size()
        # elif platform.system() == "Windows":#at home
        #     #TODO: at school, and others computers, DO NOT hardcode this 
        #     self.size = (self.w,self.h) = (1920,1080)#pygame.display.get_surface().get_size()#MACOSX only?
        self.size = (self.w,self.h) = get_screen_size()   
        i_path = 'res/images/item.jpeg'
        im = coreImage(i_path)
        im_texture = im.texture  
        # tex = coreImage(i_path).texture
        # bottomright = tex.get_region(0, 64, 64, 64)
        # topleft = tex.get_region(0, 64, 64, 64)
        # topright = tex.get_region(64, 64, 64, 64)
        # bottomleft = tex.get_region(0, 0, 64, 64)

        self.root.canvas.add(Color( 195/255, 191/255,195/255, .7))
        self.root.canvas.add(Rectangle(pos=(0,0),size=self.size))

        size = (sx,sy) = (700, 700)
        texture = Texture.create(size=size)
        px_size = sx*sy*3
        buf = [0]*px_size  #round(x * 255 / px_size) 
        # for i,px_int in enumerate(buf):

        #     #if i<100*700*3:#if i>=300*700*3 and i< 400*700*3:
        #         #if i%3 == 2:
        #     buf[i]=255#int(round(255))
        #     # else:
            #     buf[i]=0#int(round(255*.2))
        #bytes_buf = b''.join([b'\xc3',b'\xbf',b'\xc3']*sx*sy )#WHY display this color?

        bytes_buf = b''.join([bytes(bc,encoding='utf-8') for bc in [chr(c) for c in buf]] )
        texture.blit_buffer(bytes_buf, colorfmt='rgb', bufferfmt='ubyte')
        print("bytes_buf len:",len(bytes_buf))
        texture = im_texture
        print(f"texture.width:{texture.width}, texture.height:{texture.height}")
        part = texture.get_region(0, 0, texture.width, texture.height/2) 
      
        print(type(part.pixels))
        print("find:",texture.pixels.find(part.pixels))
        without_a = part.pixels.replace(b'\xff',b'')
        print("without_a len:",len(without_a))
        texture.blit_buffer(without_a+without_a, colorfmt='rgb', bufferfmt='ubyte')
        self.root.canvas.add(Color(1, 1, 1, 1))
        self.root.canvas.add(Rectangle(texture=texture, size = size, pos = (290,5)))
        #Ellipse
        

        # print(f"testing texture:{texture},texture.pixels:{texture.pixels}\n\n")
        # print(f"part:{part.pixels}")
        #print(f"bottomright:{bottomright},topleft:{topleft},topright:{topright},bottomleft:{bottomleft}")
   
    def image_texture_extension(self,texture,extended_width,extended_height):

        #TODO: needed?
        extended_texture = Texture.create(size=(extended_width,extended_height))
        return extended_texture

        # # use any zip file of an animated image
        # self.animated_icon = Image(source='factory_icon.zip')
        # # If I add an Image, the icon animates
        # self.root.add_widget(self.animated_icon)
        # # If I add the Image's texture on to a Rectangle instruction, no animation
        # r = Rectangle(texture=self.animated_icon.texture, size=(100, 100), pos=(100, 100))
        # self.root.canvas.add(r)

    def build(self):
        return self.root

if __name__ == '__main__':
    MainApp().run()