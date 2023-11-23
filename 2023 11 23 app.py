from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import dijkstra_station_use as ds
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase

_routeResult = None
solo = False
multi = False
auto_word_complete = False

class MainWindow(Screen):
    def auto_word_complete(self):
        self.auto_word_output.text = self.startStationInput.text
        print(self.auto_word_output.text)

    def solo_submit(self):
        global _routeResult 
        global solo
        solo = True

        startStation = ds.get_valid_value(self.startStationInput.text, ds.stationNode)
        arriveStation = ds.get_valid_value(self.arriveStationInput.text, ds.stationNode)
        if (startStation != None and arriveStation != None):
            ds.solo(startStation, arriveStation)
            _routeResult = str("출발역 ~ 도착역 : {} \n".format(ds.routeResult))
            _routeResult += str("[거리 : {}(km)]\n".format(ds.shortestDistResult))

        elif (startStation == None and arriveStation != None):
            _routeResult = str("출발역이 잘못 입력되었습니다. 다시 입력해주세요")
        elif (startStation != None and arriveStation == None):
            _routeResult = str("도착역이 잘못 입력되었습니다. 다시 입력해주세요")
        else:
            _routeResult = str("유효하지 않은 입력입니다. 다시 입력해주세요.")

class SecondWindow(Screen):
    def multi_submit(self):
        global _routeResult
        global multi
        global _stopover_arrive_routeResult
        global _startStation1_stopover_routeResult
        global _startStation2_stopover_routeResult
        global _stopover_arrive_shortestDistResult
        global _startStation1_stopover_shortestDistResult
        global _startStation2_stopover_shortestDistResult
        multi = True

        startStation_1 = ds.get_valid_value(self.startStationInput_1.text, ds.stationNode)
        startStation_2 = ds.get_valid_value(self.startStationInput_2.text, ds.stationNode)
        arriveStation = ds.get_valid_value(self.arriveStationInput.text, ds.stationNode)
        if (startStation_1 != None and startStation_2 != None and arriveStation != None):
            ds.multi(startStation_1, startStation_2, arriveStation)
            _stopover_arrive_routeResult = str(ds.stopover_arrive_routeResult)
            _startStation1_stopover_routeResult = str(ds.startStation1_stopover_routeResult)
            _startStation2_stopover_routeResult = str(ds.startStation2_stopover_routeResult)
            _stopover_arrive_shortestDistResult = str(ds.stopover_arrive_shortestDistResult)
            _startStation1_stopover_shortestDistResult = str(ds.startStation1_stopover_shortestDistResult)
            _startStation2_stopover_shortestDistResult = str(ds.startStation2_stopover_shortestDistResult)

            _routeResult = str("출발역 1 ~ 경유역 : {} \n".format(_startStation1_stopover_routeResult))
            _routeResult += str("[거리 : {}(km)]\n".format(_startStation1_stopover_shortestDistResult))
            _routeResult += str("출발역 2 ~ 경유역 : {} \n".format(_startStation2_stopover_routeResult))
            _routeResult += str("[거리 : {}(km)]\n".format(_startStation2_stopover_shortestDistResult))
            _routeResult += str("경유역 ~ 도착역 : {} \n".format(_stopover_arrive_routeResult))
            _routeResult += str("[거리 : {}(km)]\n".format(_stopover_arrive_shortestDistResult))

        elif (startStation_1 == None):
            _routeResult += str("출발역_1이(가) 잘못 입력되었습니다. 다시 입력해주세요" + "\n")
        elif (startStation_2 == None):
            _routeResult += str("출발역_2이(가) 잘못 입력되었습니다. 다시 입력해주세요" + "\n")
        elif (arriveStation == None):
            _routeResult += str("도착역이 잘못 입력되었습니다.다시 입력해주세요." + "\n")
        else:
            _routeResult += str("무언가 잘못 된 것이 있습니다." + "\n")

class ThirdWindow(Screen):
    def on_enter(self):
        global solo
        global multi
        if (solo == True):
            self.printLabel.text = str(_routeResult + "\n")
            solo = False
        elif (multi == True):
            self.printLabel.text = str(_routeResult + "\n")
            multi = False

    def on_pre_leave(self):
        self.printLabel.text = ''

class WindowManager(ScreenManager):
    def auto_word_complete(self):
        global stationNode
        global station_list
        global auto_word_output

        stationNode = ds.stationNode

        station_list = []

    
    def un_auto_word_complete(self):
        global auto_word_complete
        auto_word_complete = False
        self.auto_word_output.text = ""

kv = Builder.load_file("screen_manager.kv")

class MyMainApp(App):
    LabelBase.register(name='nanummyeongjoEB', fn_regular='나눔명조EB.ttf')
    
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()