###################################################
# The last screen of this game                    #
###################################################
from game_manager import *

class EndingScreen(Screen):
    end_signal = NumericProperty(0)
    def __init__(self, **kwargs):
        super(EndingScreen, self).__init__(**kwargs)

        self.size = (global_w,global_h)
        f = open('res/dialogs/終章.txt','r')#,encoding='utf-8')
        r = f.read()
        print(r)
        self.label = Label(text=r,font_size=36,pos=(.2*self.size[0],-1.9*self.size[1]),\
            size=(.6*self.size[0],2*self.size[1]),size_hint=(None,None),font_name='res/HuaKangTiFan-CuTi-1.otf')

        print('init end label.pos:',self.label.pos)
        self.bind(end_signal=self.auto_exit_prompt)
        Window.bind(on_key_down=self.key_action)


        self.cur_image_size = (2*self.size[0],2*self.size[1])
        self.cur_image_pos = (-.5*self.size[0],-.5*self.size[1])       
        self.canvas.before.add(Rectangle(source='res/images/testing/a.jpg',pos=self.cur_image_pos,size=self.cur_image_size,group='end'))
    def auto_exit_prompt(self,instance,end_signal):
        if end_signal >= 2:
            auto_prompt(self,'Enter',{'x':.25,'y':.4},instance=self, prompt=True,extra_info='故事結束\n')

    def load_ending(self):
        print('End The Story')
        self.add_widget(self.label)
        pickle_path = 'res/pickles/'#破關就刪掉存檔檔案
        for f in os.listdir(pickle_path):
            if '.pickle' in f:
                os.remove(os.path.join(pickle_path,f))

        self.up_event = Clock.schedule_interval(partial(self.animate,self.label.pos),.35)
        self.reducing_event = Clock.schedule_interval(self.reducing,.05)

    def key_action(self, *args):
        if self.manager.current == 'ending': 
            print('ending key: ',args)
            press_key_id = args[1]#args[1]:ASCII
            if press_key_id in [274,273]:#<-,->     
                self.animate(self.label.pos,press_key_id)
            if press_key_id == 13:
                if self.end_signal >= 2:
                    self.manager.get_screen('story').exit_game()
    def reducing(self, *args):
        if self.cur_image_size[0] <= self.size[0]:#.1*self.size[0]:
            Clock.unschedule(self.reducing_event)
            self.end_signal += 1
            return 
        rate = 1/1.00031
        self.canvas.before.remove_group('end')
        self.cur_image_size = (self.cur_image_size[0]*rate,self.cur_image_size[1]*rate) 
        self.cur_image_pos = ((self.size[0]-self.cur_image_size[0])/2, (self.size[1]-self.cur_image_size[1])/2)
        self.canvas.before.add(Rectangle(source='res/images/end.jpg',pos=self.cur_image_pos,size=self.cur_image_size,group='end'))


    def animate(self,pos,duration=.07,*args):
        (px,py) = pos
        if py >= self.size[1]:
            Clock.unschedule(self.up_event)
            self.end_signal += 1
            return
        (ox,oy) = (0,2.4)    

        anim = Animation(pos=(px+ox,py+oy), duration=duration )
        anim.start(self.label)
        self.label.pos = (px+ox,py+oy)

        print(f"After anim... pos:{self.label.pos}")

        