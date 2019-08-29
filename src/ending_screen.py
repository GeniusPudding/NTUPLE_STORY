###################################################
# The last screen of this game                    #
###################################################
from game_manager import *

class EndingScreen(Screen):
    end_signal = NumericProperty(0)
    dialogframe_width = NumericProperty(0.92)   
    dialogframe_height = NumericProperty(0.2)
    def __init__(self, **kwargs):
        super(EndingScreen, self).__init__(**kwargs)
        self.displaying_character_labels = []
        self.dialog_events = []    
        self.size = (global_w,global_h)
        print('init end self.size:',self.size)
        with open('res/dialogs/終章.txt','r',encoding='MS950') as f:#,encoding='utf-8')
            r = f.read()
        print(r)
        self.label = Label(text=r,font_size=36,pos=(.2*self.size[0],-1.9*self.size[1]),\
            size=(.6*self.size[0],2*self.size[1]),size_hint=(None,None),font_name='res/HuaKangTiFan-CuTi-1.otf')

        print('init end label.pos:',self.label.pos)
        self.bind(end_signal=self.auto_exit_prompt)
        Window.bind(on_key_down=self.key_action)

        #init end 
        self.canvas.add(Color(rgba=(0,0,0,1),group='bg'))
        self.canvas.add(Rectangle(pos=(0,0),size=(global_w,global_h),group='bg'))
        self.canvas.add(Color(rgba=(1,1,1,1),group='dialogframe'))
        self.canvas.add(Rectangle(source='res/images/new_dialogframe.png',pos=(0,0),size=(global_w*self.dialogframe_width,global_h*(self.dialogframe_height+.07)),group='dialogframe'))

        #for end 5
        self.cur_image_size = (2*self.size[0],2*self.size[1])
        self.cur_image_pos = (-.5*self.size[0],-.5*self.size[1])       
    def auto_exit_prompt(self,instance,end_signal):
        if end_signal >= 2:
            auto_prompt(self,'Enter',{'x':.2,'y':.3},instance=self, prompt=True,extra_info='故事結束\n')

    def load_ending(self):
        print('End The Story')
        
        pickle_path = 'res/pickles/'#破關就刪掉存檔檔案
        for f in os.listdir(pickle_path):
            if '.pickle' in f:
                os.remove(os.path.join(pickle_path,f))


        line_display_scheduler(self,'「叮咚！」',False,.2,.3,.1)
        Clock.schedule_once(self.to_end_1,1.2)
        Clock.schedule_once(self.to_end_2,2.4)
        Clock.schedule_once(self.to_end_3,3.6)
        Clock.schedule_once(self.to_end_4,4.8)
        Clock.schedule_once(self.to_transition,7.8)
        Clock.schedule_once(self.to_end_5,10) 

    def to_end_1(self,*args):
        self.switch_end(1,'李詠晴、')

    def to_end_2(self,*args):
        self.switch_end(2,'楊承恩、')

    def to_end_3(self,*args):
        self.switch_end(3,'孟亦廷、')

    def to_end_4(self,*args): 
        self.switch_end(4,'張怡彤的手機同時收到了一則訊息。')

    def to_transition(self,*args):
        self.switch_end(4,'是孟亦安。')

    def to_end_5(self,*args):
        for c in self.children:
            self.remove_widget(c)
        clear_displayed_text(self,self.displaying_character_labels)
        self.canvas.remove_group('bg')
        self.canvas.remove_group('dialogframe')
        self.canvas.before.add(Rectangle(source='res/images/end.jpg',pos=self.cur_image_pos,size=self.cur_image_size,group='end'))
        self.add_widget(self.label)
        self.up_event = Clock.schedule_interval(partial(self.animate,self.label.pos),.35)
        self.reducing_event = Clock.schedule_interval(self.reducing,.05)

    def switch_end(self,end_id,text):
        self.canvas.remove_group('bg')
        self.canvas.remove_group('dialogframe')
        self.canvas.add(Rectangle(source=f'res/images/終{end_id}.jpg',pos=(0,0),size=(global_w,global_h),group='bg'))
        self.canvas.add(Color(rgba=(1,1,1,1),group='dialogframe'))
        self.canvas.add(Rectangle(source='res/images/new_dialogframe.png',pos=(0,0),size=(global_w*self.dialogframe_width,global_h*(self.dialogframe_height+.07)),group='dialogframe')) 
        line_display_scheduler(self,text,False,.2,.3,.1)

    def key_action(self, *args):
        if self.manager.current == 'ending': 
            print('ending key: ',args)
            press_key_id = args[1]
            if press_key_id == 13:
                if self.end_signal >= 2:
                    self.manager.get_screen('story').exit_game()

    def reducing(self, *args):
        if self.cur_image_size[0] <= self.size[0]:#.1*self.size[0]:
            Clock.unschedule(self.reducing_event)
            self.end_signal += 1
            return 
        rate = 1/1.0004
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
        (ox,oy) = (0,5.2)    

        anim = Animation(pos=(px+ox,py+oy), duration=duration )
        anim.start(self.label)
        self.label.pos = (px+ox,py+oy)
        print(f"After anim... pos:{self.label.pos}")

        