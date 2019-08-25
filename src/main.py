###################################################
# Executable entry of the game program            #
###################################################

from game_manager import *
from cover_screen import CoverScreen
from intro_screen import IntroScreen
from story_screen import StoryScreen
from ending_screen import EndingScreen
from info_screen import InfoScreen 
from subgame_screen import SubgameManager
from epo_screen import ePoScreen
from memory_screen import MemoryScreen   
from prologue_screen import PrologueScreen

class NTUPLE_Story(App):
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameManagerScreen(name='gm')) 
        print("global_w,global_h:",global_w,global_h)
        sm.add_widget(StoryScreen(name='story'))
        sm.get_screen('gm').link_main_screen()
        sm.add_widget(CoverScreen(name='cover'))
        sm.add_widget(IntroScreen(name='intro'))
        sm.add_widget(PrologueScreen(name='prologue'))   
        sm.add_widget(MemoryScreen(name='memory'))       
        sm.add_widget(SubgameManager(name='subgames_manager'))
        sm.add_widget(ePoScreen(name='epo'))
        sm.add_widget(InfoScreen(name='info'))     
        sm.add_widget(EndingScreen(name='ending'))         
        sm.current = 'cover'

        return sm

if __name__ == '__main__':
    #sys.stdout = open('stdout.txt', 'a+')
    # sys.stderr = open('debug/stderr.txt', 'a+')
    # sys.stderr.write('#####'+str(datetime.datetime.now())+'#####\n')
    print('#'*10, datetime.datetime.now(), '#'*10, '\n')
    
    # disable the left click red dot
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Config.set('graphics', 'fullscreen', '0')

    #Config.set('kivy','exit_on_escape',0)
    Config.set('kivy','keyboard_mode','')

    with open ('kv/NTUPLE_Story.kv', 'r', encoding='utf-8') as f:
        Builder.load_string(f.read())
    if OS == "Windows":
        Window.fullscreen = 'auto'
    NTUPLE_Story().run()

