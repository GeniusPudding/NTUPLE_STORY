from game_manager import *

def redraw_widget(self,*args):
    print('redraw_widget args:',args)
class EndingScreen(Screen):
    def __init__(self, **kwargs):
        super(EndingScreen, self).__init__(**kwargs)
        print('init end self.size:',self.size)
        self.label = Label(text='ABCDEFGHIJKLMNOP',font_size=100,pos_hint={'x':.25,'y':.1},size_hint=(.5,.2))
        #self.label.pos = 
        print('init end label.pos:',self.label.pos)
        self.bind(pos=redraw_widget, size=redraw_widget)
        Window.bind(on_key_down=self.key_action)
        
    def load_ending(self):
        #print(f'Show {player_id+1}-th player\'s ending')
        #if last_one:
        print('End The Story')
        #TODO
        self.add_widget(self.label)
        print('load end label.pos:',self.label.pos)
        print('load end self.pos:',self.pos)
        print('load end label.pos_hint:',self.label.pos_hint)
        print('load end label.size_hint:',self.label.size_hint)
        pickle_path = 'res/pickles/'#破關就刪掉存檔檔案
        for f in os.listdir(pickle_path):
            if '.pickle' in f:
                os.remove(os.path.join(pickle_path,f))

        Clock.schedule_interval(partial(self.animate,self.label.pos,274),.35)
    def key_action(self, *args):
        if self.manager.current == 'ending': 
            print('ending key: ',args)
            press_key_id = args[1]#args[1]:ASCII
            if press_key_id in [274,273]:#<-,->     
                self.animate(self.label.pos,press_key_id)

    def animate(self,pos,direction,duration=.35,*args):
        (px,py) = pos
        (ox,oy) = (0,30)
            
        # if direction == 'positive':
        #     (ox,oy) = (10,0)
        #     anim = Animation(pos=(px+ox,py+oy), duration=duration)#(x=px+ox, y=py+oy, duration=1)
        #     anim.start(self)
        #     self.pos = (px+ox,py+oy) 
        if direction == 273:
            (ox,oy) = (0,-30)
        anim = Animation(pos=(px+ox,py+oy), duration=duration )#(x=px-ox, y=py-oy, duration=1)
        anim.start(self.label)
        self.label.pos = (px+ox,py+oy)

        print(f"After anim... pos:{self.label.pos}")