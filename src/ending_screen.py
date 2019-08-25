###################################################
# The last screen of this game                    #
###################################################
from game_manager import *

def redraw_widget(self,*args):
    print('redraw_widget args:',args)
class EndingScreen(Screen):
    def __init__(self, **kwargs):
        super(EndingScreen, self).__init__(**kwargs)
        
        print('init end self.size_hint:',self.size_hint)
        self.size = (global_w,global_h)
        print('init end self.size:',self.size)
        f = open('res/dialogs/終章.txt','r')#,encoding='utf-8')
        r = f.read()
        print(r)#'ABCDEFGH\nIJKLM\nNOPQRSTUVW\nXYZ0123456789\n'
        self.label = Label(text=r,font_size=36,pos=(.2*self.size[0],-1.9*self.size[1]),\
            size=(.6*self.size[0],2*self.size[1]),size_hint=(None,None),font_name='res/HuaKangTiFan-CuTi-1.otf')
        #self.label.pos = ()
        print('init end label.pos:',self.label.pos)
        self.bind(pos=redraw_widget, size=redraw_widget)
        Window.bind(on_key_down=self.key_action)

        self.cur_image_size = (.1*self.size[0],.1*self.size[1])
        self.cur_image_pos = (.45*self.size[0],.45*self.size[1])
        self.canvas.before.add(Rectangle(source='res/images/testing/a.jpg',pos=self.cur_image_pos,size=self.cur_image_size,group='end'))

    def load_ending(self):
        #print(f'Show {player_id+1}-th player\'s ending')
        #if last_one:
        print('End The Story')
        #TODO
        self.add_widget(self.label)
        print('load end label.pos:',self.label.pos)
        print('load end self.pos:',self.pos)
        print('load end self.size:',self.size)
        pickle_path = 'res/pickles/'#破關就刪掉存檔檔案
        for f in os.listdir(pickle_path):
            if '.pickle' in f:
                os.remove(os.path.join(pickle_path,f))

        Clock.schedule_interval(partial(self.animate,self.label.pos,274),.35)
        self.amplifying_event = Clock.schedule_interval(self.amplifying,.05)
    def key_action(self, *args):
        if self.manager.current == 'ending': 
            print('ending key: ',args)
            press_key_id = args[1]#args[1]:ASCII
            if press_key_id in [274,273]:#<-,->     
                self.animate(self.label.pos,press_key_id)

    def amplifying(self, *args):
        if self.cur_image_size[0] >= self.size[0]:
            Clock.unschedule(self.amplifying_event)
            return 
        rate = 1.003
        self.canvas.before.remove_group('end')
        self.cur_image_size = (self.cur_image_size[0]*rate,self.cur_image_size[1]*rate) 
        self.cur_image_pos = ((self.size[0]-self.cur_image_size[0])/2, (self.size[1]-self.cur_image_size[1])/2)
        self.canvas.before.add(Rectangle(source='res/images/end.jpg',pos=self.cur_image_pos,size=self.cur_image_size,group='end'))



    def animate(self,pos,direction,duration=.35,*args):
        (px,py) = pos
        (ox,oy) = (0,5)
            
        # if direction == 'positive':
        #     (ox,oy) = (10,0)
        #     anim = Animation(pos=(px+ox,py+oy), duration=duration)#(x=px+ox, y=py+oy, duration=1)
        #     anim.start(self)
        #     self.pos = (px+ox,py+oy) 
        if direction == 273:
            (ox,oy) = (0,-5)
        anim = Animation(pos=(px+ox,py+oy), duration=duration )#(x=px-ox, y=py-oy, duration=1)
        anim.start(self.label)
        self.label.pos = (px+ox,py+oy)

        print(f"After anim... pos:{self.label.pos}")

        