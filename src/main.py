from game_manager import *
from title_screen import TitleScreen
from intro_screen import IntroScreen
from story_screen import StoryScreen
from ending_screen import EndingScreen
from info_screen import InfoScreen 
from subgame_screen import SubgameManager
from phone_screen import PhoneScreen   
from memory_screen import MemoryScreen   
from prologue_screen import PrologueScreen
from seal_screen import SealScreen
class NTUPLE_Story(App):
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameManagerScreen(name='gm')) 
        print("global_w,global_h:",global_w,global_h)
        sm.add_widget(SealScreen(name='seal'))  
        sm.add_widget(StoryScreen(name='story'))
        sm.get_screen('gm').link_main_screen()
        sm.add_widget(TitleScreen(name='title'))
        sm.add_widget(IntroScreen(name='intro'))
        sm.add_widget(PrologueScreen(name='prologue'))   
        sm.add_widget(MemoryScreen(name='memory'))       
        sm.add_widget(SubgameManager(name='subgames_manager'))
        sm.add_widget(PhoneScreen(name='phone'))
        sm.add_widget(InfoScreen(name='info'))     
        sm.add_widget(EndingScreen(name='ending'))         
        sm.current = 'title'

        return sm

if __name__ == '__main__':
    # sys.stdout = open('debug/stdout.txt', 'a+')
    # sys.stderr = open('debug/stderr.txt', 'a+')
    # sys.stderr.write('#####'+str(datetime.datetime.now())+'#####\n')
    print('#'*10, datetime.datetime.now(), '#'*10, '\n')
    # disable the left click red dot
    #Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    #Config.set('graphics', 'fullscreen', '0')
    #Config.set('graphics', 'position', 'custom')
    #Config.set('graphics', 'left', 0)
    #Config.set('graphics', 'top',  0)

    #Config.set('kivy','exit_on_escape',0)
    Config.set('kivy','keyboard_mode','')
    # TODO: Other needed configs


    with open ('kv/ntu_piece.kv', 'r', encoding='utf-8') as f:
        Builder.load_string(f.read())
    Window.fullscreen = 'auto'#True
    NTUPLE_Story().run()#+collect_submodules('kivy.weakmethod')+collect_submodules('pandas')+

