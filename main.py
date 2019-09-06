# -*- coding: utf-8 -*

from kivy.config import Config
# ウィンドウサイズの設定
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '720')
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.properties import Clock
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.resources import resource_add_path
from kivy.factory import Factory

import os
import csv
import codecs
import time
import math
import glob
#import vlc
import pygame.mixer
import datetime
from dateutil.relativedelta import relativedelta

# ファイルのパス(main.pyがあるフォルダの中にあるファイルの絶対パス)
# file_path = os.path.dirname(os.path.abspath(__file__))

# フォントの設定
resource_add_path('fonts')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')


# 各種データ一時保存用
class Holder():
    status = ""
    slide_value = 0
    filename = ""
    path = ""
    tracklist = []
    track_num = 0
    
    # 再生中かポーズ中かの判別
    @classmethod
    def setStatus(self, status):
        self.status = status
        
    @classmethod
    def getStatus(self):
        return(str(self.status))
    
    # スライドバーの値の保持
    @classmethod
    def setSlideValue(self, val):
        self.slide_value = val
        
    @classmethod
    def getSlideValue(self):
        return(self.slide_value)
    
    # 音楽ファイルの名前の保持
    @classmethod
    def setFileName(self, name):
        self.filename = name
        
    @classmethod
    def getFileName(self):
        return(self.filename)
    
    # ファイルのパスを記録
    @classmethod
    def setFilePath(self,path):
        self.path = path
        
    @classmethod
    def getFilePath(self):
        return(self.path)
    
    # 再生リストを記録
    @classmethod
    def setTrackList(self, track):
        self.tracklist = track
        
    @classmethod
    def getTrackList(self):
        return(self.tracklist)
    
    # 再生中の曲が何番目かを記録
    @classmethod
    def setTrackNum(self, num):
        self.track_num = num
        
    @classmethod
    def getTrackNum(self):
        return(self.track_num)
        
    

class PopupList(BoxLayout):
    # MusicPlayerクラス内で参照するための設定
    buttonTrack = ObjectProperty(None)
    buttonUp = ObjectProperty(None)
    buttonDown = ObjectProperty(None)
    cancel = ObjectProperty(None)
       
    track_1 = ""
    track_2 = ""
    track_3 = ""
    track_4 = ""
    track_5 = ""
    track_6 = ""
    track_7 = ""
    
    # 再生リスト表示用ボタンのカラー
    track_1_color = .5
    track_2_color = .5
    track_3_color = .5
    track_4_color = .5
    track_5_color = .5
    track_6_color = .5
    track_7_color = .5
        
    @classmethod
    def setTrackLabel(self, flag):
        
        self.setColorGray()
        
        try:
            filename, ext = os.path.splitext(os.path.basename(Holder.getTrackList()[0 + 7 * flag]))
            self.track_1 = filename
            if Holder.getFileName() in self.track_1:
                self.track_1_color = 1
            
        except:
            self.track_1 = ""
            
        try:
            filename, ext = os.path.splitext(os.path.basename(Holder.getTrackList()[1 + 7 * flag]))
            self.track_2 = filename
            if Holder.getFileName() in self.track_2:
                self.track_2_color = 1
                
        except:
            self.track_2 = ""
            
        try:
            filename, ext = os.path.splitext(os.path.basename(Holder.getTrackList()[2 + 7 * flag]))
            self.track_3 = filename
            if Holder.getFileName() in self.track_3:
                self.track_3_color = 1
                
        except:
            self.track_3 = ""
            
        try:
            filename, ext = os.path.splitext(os.path.basename(Holder.getTrackList()[3 + 7 * flag]))
            self.track_4 = filename
            if Holder.getFileName() in self.track_4:
                self.track_4_color = 1
                
        except:
            self.track_4 = ""
            
        try:
            filename, ext = os.path.splitext(os.path.basename(Holder.getTrackList()[4 + 7 * flag]))
            self.track_5 = filename
            if Holder.getFileName() in self.track_5:
                self.track_5_color = 1
                
        except:
            self.track_5 = ""
            
        try:
            filename, ext = os.path.splitext(os.path.basename(Holder.getTrackList()[5 + 7 * flag]))
            self.track_6 = filename
            if Holder.getFileName() in self.track_6:
                self.track_6_color = 1
                
        except:
            self.track_6 = ""
            
        try:
            filename, ext = os.path.splitext(os.path.basename(Holder.getTrackList()[6 + 7 * flag]))
            self.track_7 = filename
            if Holder.getFileName() in self.track_7:
                self.track_7_color = 1
                
        except:
            self.track_7 = ""
       
    
    @classmethod
    def setColorGray(self):
        """再生リスト表示用ボタンのカラーを全てグレーにする"""
        
        self.track_1_color = .5
        self.track_2_color = .5
        self.track_3_color = .5
        self.track_4_color = .5
        self.track_5_color = .5
        self.track_6_color = .5
        self.track_7_color = .5
                    
        
class PopupChooseFile(BoxLayout):
    # 現在のカレントディレクトリ。FileChooserIconViewのpathに渡す
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # MusicPlayerクラス内で参照するための設定
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)



class Player(BoxLayout):
    text = StringProperty()
    current_time = StringProperty() # 現在の再生位置
    length = StringProperty() # 曲の長さ
    background = ObjectProperty(None) # アルバムアート
    background_through = ObjectProperty(int()) # アルバムアートの透過度
    image_play = ObjectProperty(None) # 再生ボタン
    
    lrc_r = ObjectProperty(int()) # 歌詞の色 r
    lrc_g = ObjectProperty(int()) # 歌詞の色 g
    lrc_b = ObjectProperty(int()) # 歌詞の色 b
    lrc_through = ObjectProperty(int()) # 歌詞の透過度(一応)
    wb_flag = 0 # 歌詞の色の識別用フラグ
    
    sound_vlc = None # 音楽ファイルの再生用
    sound_kivy = None # 音楽の長さの取得用
    cnt = 0 # 一秒ごとにスライドバーの表示を更新するための変数
    track = None # 再生トラック管理用の配列
    #tracklist = ObjectProperty() # 再生トラック
    flag = 0 # 再生リスト更新用のフラグ
    press_time = 0 # 歌詞ボタンの押下時間計測用
        
    # アプリ実行時の初期化の処理
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)        
        self.ids.current_time.text = "00:00"
        self.ids.length.text = "00:00"
        
        self.lrc_r = 1
        self.lrc_g = 1
        self.lrc_b = 1
        self.lrc_through = 1
        self.wb_flag = 0
        
        self.image_play = "image/play.png"
        
        # アプリ立ち上げ時はsoundフォルダ内のoggファイルを再生リストとする
        pygame.mixer.init()
        
        try:
            # soundフォルダ内のoggファイルを読み込んで配列にする
            self.track = glob.glob("sound//*.ogg")
            path = os.path.abspath(self.track[0])
            Holder.setTrackList(self.track)
            
            # ファイル名の取得
            filename, ext = os.path.splitext(os.path.basename(path))
            self.ids.label.text = filename
            Holder.setFileName(filename)
            Holder.setFilePath(path)
                        
            pygame.mixer.music.load(path)
            self.sound_kivy = SoundLoader.load(path)
            
            Holder.setTrackNum(0)
            self.setImage_Lrc(filename)
                                                                        
        except:
            self.background = 'image/vinyl.png'
            self.background_through = 1
            self.ids.lrc_text.text = ""
            Holder.setFileName("")
            Holder.setFilePath("")

        
        
    def buttonSelect(self):
        """Choose File押下時に呼び出され、ポップアップでファイル選択させる"""
        
        content = PopupChooseFile(select=self.select, cancel=self.cancel)
        self.popup = Popup(title="Select Music File", content=content, size_hint=(.8, .7))
        self.popup.open()
        
        
    def cancel(self):
        """ファイル選択画面でキャンセル"""
        
        self.flag = 0
        self.popup.dismiss()
    
    
    def select(self,path):
        """ファイル選択時"""

#        if self.sound_vlc:
#            self.sound_vlc.stop()

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.ids.slider.value = 0
            Holder.setSlideValue(self.ids.slider.value)
            Clock.unschedule(self.position)
            Holder.setStatus("stop")
            self.sound_kivy.unload()
            self.image_play = "image/play.png"
                    
        try:

            # ファイル名の取得
            filename, ext = os.path.splitext(os.path.basename(path))
            self.ids.label.text = filename
            Holder.setFileName(filename)
            Holder.setFilePath(path)
                        
            # self.sound_vlc = vlc.MediaPlayer()
            # self.sound_vlc.set_mrl(path)
            
            self.track = glob.glob(path.replace(filename, '*'))
            self.track.insert(0, self.track.pop(self.track.index(path)))
            
            Holder.setTrackList(self.track)
            pygame.mixer.music.load(self.track[0])
            self.sound_kivy = SoundLoader.load(path)
            
            Holder.setTrackNum(0)
            self.setImage_Lrc(filename)
            
            # 歌詞の色を白にする
            self.lrc_r, self.lrc_g, self.lrc_b = 1, 1, 1
            self.wb_flag = 0
                        
        except:
            self.ids.label.text = "Please select a ogg file."
            self.background = 'image/vinyl.png'
            self.background_through = 1
            self.ids.lrc_text.text = ""
            Holder.setFileName("")
            Holder.setFilePath("")
                    
                
        # ポップアップを閉じる
        self.popup.dismiss()
    
    
    def setImage_Lrc(self, filename):
        """アルバムアートと歌詞のセット"""
        
        filename, ext = os.path.splitext(os.path.basename(Holder.getFilePath()))
        # lrcファイルの読み込み
        try:
            self.background_through = 0.7
            self.lrc_through = 1
            file = open(Holder.getFilePath().replace(ext, '.txt'), "r")
            lrc = file.read()
            self.ids.lrc_text.text = lrc
            file.close()

        except:
            self.background_through = 1
            self.lrc_through = 1
            self.ids.lrc_text.text = ""

        # 背景画像のセット(フォルダに同じ名前のjpgがあったらそれを、なければフォルダ内にあるjpgを見つけてセット)
        if os.path.exists(Holder.getFilePath().replace(ext, '.jpg')):
            self.background = Holder.getFilePath().replace(ext, '.jpg')
            
        else:
            try:
                pictures = glob.glob(os.path.dirname(Holder.getFilePath()) + '/*.jpg')
                self.background = pictures[0]
            
            except:
                # 背景画像が用意されていない場合の処理
                self.background = 'image/vinyl.png'

        # 時間表示の更新
        self.ids.length.text = "{0.minutes:02}:{0.seconds:02}".format(relativedelta(seconds=int(self.sound_kivy.length)))
        self.ids.slider.value = 0
        self.ids.slider.max = int(self.sound_kivy.length)

        # ポーズ中ではないことを記録
        Holder.setStatus("stop")
        Holder.setSlideValue(0)

        #self.sound_kivy.unload()
        #self.sound_kivy = None
    
    
    def buttonPlay(self):
        """再生ボタンクリック時"""
        
        try:
            if not Holder.getStatus() == "" and not Holder.getStatus() == "play":
                # 再生中でなければ
                try:
                    pygame.mixer.music.play(0, Holder.getSlideValue())
                    Clock.schedule_interval(self.position, 0.1)
                    self.image_play = "image/pause.png"
#                    self.sound_vlc.play()
#                    self.sound_vlc.set_time(int(Holder.getSlideValue() * 1000))
                    Holder.setStatus("play")
                    
                except:
                    pass

            else:                
                Holder.setSlideValue(self.ids.slider.value)
                pygame.mixer.music.pause()
                self.image_play = "image/play.png"
#                self.sound_vlc.pause()
                Clock.unschedule(self.position)
                Holder.setStatus("pause")
                
        except:
            pass
        
            
    def position(self, *arg):
        """schedule_intervalで0.1秒ごとに呼び出される部分。現在の再生位置を読み込み、それを表示&バーに反映"""
        
        # 現在の再生位置の表示の更新
        self.ids.current_time.text = "{0.minutes:02}:{0.seconds:02}".format(relativedelta(seconds=int(self.ids.slider.value)))
        # スライドバーの位置を1秒ごとに更新
        if self.cnt % 10 == 0:
            self.ids.slider.value += 1
        self.cnt += 1
        
        # 最後まで再生したら停止、次の曲があればそれを再生
        if self.ids.slider.value > self.ids.slider.max:
            pygame.mixer.music.stop()
            self.buttonNext()
            self.image_play = "image/play.png"
                                
#        self.ids.slider.value = round(int(self.sound_vlc.get_time() / 1000))
        
        
    def slide(self):
        """スライドバーの値が変化するたびに呼び出される関数"""
        
        try:
            # 現在の再生位置の表示の更新
            self.ids.current_time.text = "{0.minutes:02}:{0.seconds:02}".format(relativedelta(seconds=int(self.ids.slider.value)))
            
            # 再生中にスライドバーを動かした場合にその位置に再生位置を更新する
            if Holder.getStatus() == "play" and not (self.ids.slider.value - Holder.getSlideValue()) == 1:
                pygame.mixer.music.pause()
                pygame.mixer.music.play(0, self.ids.slider.value)
                self.image_play = "image/pause.png"
                                                
#           if self.sound_vlc.get_time() - (Holder.getSlideValue() * 1000) < 1000:
#                self.sound_vlc.set_time(int(self.ids.slider.value) * 1000)
            
            Holder.setSlideValue(self.ids.slider.value)
                    
        except:
            pass
        
    
    def buttonBack(self):
        """戻るボタンクリック時"""
        
        if Holder.getTrackNum() - 1 >= 0:
            # 再生中の曲を止める
            pygame.mixer.music.stop()
            self.ids.slider.value = 0
            Holder.setSlideValue(self.ids.slider.value)
            Clock.unschedule(self.position)
            self.sound_kivy.unload()
                        
            # 一個前の曲の再生
            Holder.setTrackNum(Holder.getTrackNum() - 1)
            pygame.mixer.music.load(self.track[Holder.getTrackNum()])
            self.sound_kivy = SoundLoader.load(self.track[Holder.getTrackNum()])
            pygame.mixer.music.play()
            Clock.schedule_interval(self.position, 0.1)
            self.image_play = "image/pause.png"
            
            # ファイルのパスの更新
            Holder.setFilePath(self.track[Holder.getTrackNum()])
            # ファイル名の取得
            filename, ext = os.path.splitext(os.path.basename(Holder.getFilePath()))
            self.ids.label.text = filename
            Holder.setFileName(filename)
            Holder.setFilePath(Holder.getFilePath())
            self.setImage_Lrc(Holder.getFileName())
            Holder.setStatus("play")
            
            # 歌詞の色を白にする
            self.lrc_r, self.lrc_g, self.lrc_b = 1, 1, 1
            self.wb_flag = 0
                        
        else:
            pass
    
    
    def buttonNext(self):
        """進むボタンクリック時"""
        
        if Holder.getTrackNum() + 1 < len(self.track):
            # 再生中の曲を止める
            pygame.mixer.music.stop()
            Clock.unschedule(self.position)
            self.ids.slider.value = 0
            Holder.setSlideValue(self.ids.slider.value)
            
            # 一個後の曲の再生
            Holder.setTrackNum(Holder.getTrackNum() + 1)
            pygame.mixer.music.load(self.track[Holder.getTrackNum()])
            self.sound_kivy = SoundLoader.load(self.track[Holder.getTrackNum()])
            pygame.mixer.music.play()
            Clock.schedule_interval(self.position, 0.1)
            self.image_play = "image/pause.png"
            
            # ファイルのパスの更新
            Holder.setFilePath(self.track[Holder.getTrackNum()])
            # ファイル名の取得
            filename, ext = os.path.splitext(os.path.basename(Holder.getFilePath()))
            self.ids.label.text = filename
            Holder.setFileName(filename)
            Holder.setFilePath(Holder.getFilePath())
            self.setImage_Lrc(Holder.getFileName())
            Holder.setStatus("play")
            
            # 歌詞の色を白にする
            self.lrc_r, self.lrc_g, self.lrc_b = 1, 1, 1
            self.wb_flag = 0
                        
        else:
            pass
    
    
    def startTime(self):
        """歌詞ボタンを押した時にタイマー起動"""
        
        self.press_time = time.time()
    
    
    def buttonLrc(self):
        """歌詞の表示/非表示"""
        
        if (time.time() - self.press_time) > 0.3:
            self.changeLrcColor()
        
        # lrcファイルの読み込み
        filename, ext = os.path.splitext(os.path.basename(Holder.getFilePath()))
        if len(self.ids.lrc_text.text) == 0:
            try:
                self.background_through = 0.7
                self.lrc_through = 1
                file = open(Holder.getFilePath().replace(ext, '.txt'), "r")
                lrc = file.read()
                self.ids.lrc_text.text = lrc
                file.close()
                
            except:
                self.background_through = 1
                self.lrc_through = 1
                self.ids.lrc_text.text = ""
                
        else:
            self.background_through = 1
            self.lrc_through = 1
            self.ids.lrc_text.text = ""
    
    
    def changeLrcColor(self):
        """歌詞の色の変更"""
        
        if self.wb_flag == 0:
            self.lrc_r, self.lrc_g, self.lrc_b = 0, 0, 0
            self.wb_flag = 1
            
        else:
            self.lrc_r, self.lrc_g, self.lrc_b = 1, 1, 1
            self.wb_flag = 0
        
    
    def buttonList(self):
        """リストボタンクリック時"""
        
        # 再生リストを記録
        Holder.setTrackList(self.track)
        # 再生リストの表示を更新
        PopupList.setTrackLabel(self.flag)
                
        content = PopupList(buttonUp=self.buttonUp, buttonDown=self.buttonDown, buttonTrack=self.buttonTrack, cancel=self.cancel)
        self.popup = Popup(title="Play List", content=content, size_hint=(.8, .7))
        self.popup.open()
        
        
    def buttonUp(self):
        """upボタンを押した時"""

        self.popup.dismiss()
        self.flag -= 1
        if self.flag < 0:
            self.flag = 0
        self.buttonList()
        
    
    def buttonDown(self):
        """downボタンを押した時"""
        
        self.popup.dismiss()
        if (self.flag + 1) * 7 < len(self.track):
            self.flag += 1
        self.buttonList()
        
    
    def buttonTrack(self, num):
        """再生リスト"""
        
        if (num + 7 * self.flag) < len(self.track):
            # 再生中の曲を止める
            pygame.mixer.music.stop()
            Clock.unschedule(self.position)
            self.ids.slider.value = 0
            Holder.setSlideValue(self.ids.slider.value)

            # 選択したところの曲の再生
            Holder.setTrackNum(num + 7 * self.flag)
            pygame.mixer.music.load(self.track[Holder.getTrackNum()])
            self.sound_kivy = SoundLoader.load(self.track[Holder.getTrackNum()])
            pygame.mixer.music.play()
            Clock.schedule_interval(self.position, 0.1)
            self.image_play = "image/pause.png"

            # ファイルのパスの更新
            Holder.setFilePath(self.track[Holder.getTrackNum()])
            # ファイル名の取得
            filename, ext = os.path.splitext(os.path.basename(Holder.getFilePath()))
            self.ids.label.text = filename
            Holder.setFileName(filename)
            Holder.setFilePath(Holder.getFilePath())
            self.setImage_Lrc(Holder.getFileName())
            Holder.setStatus("play")
            
            # 歌詞の色を白にする
            self.lrc_r, self.lrc_g, self.lrc_b = 1, 1, 1
            self.wb_flag = 0
            
            # ポップアップを閉じる
            self.popup.dismiss()
            
        else:
            pass
        
        
    """
    def buttonClicked(self):
        #with open(os.path.join(file_path, 'task_data.csv'),'a') as f:
        # csvファイルに書き込み
        file = open("task_data.csv","a",newline='')
        writer = csv.writer(file)
        txt = []
        txt.append(self.ids['display_input'].text)
        writer.writerow(txt)
        file.close()
        
        # csvファイルを読み込んで表示
        file = open("task_data.csv","r")
        lines = file.read()
        self.text = str(lines)
        file.close()
    """
        
        

class PlayerApp(App):
    # kivy launcherでのリスト表示時におけるタイトルとアイコンの設定
    title = 'player'
    icon = 'icon.png'

    def build(self):
        return Player()

    # アプリをポーズした時
    def on_pause(self):
        return True
    
    # アプリ終了時
    #def on_stop(self):

if __name__ == '__main__':
    PlayerApp().run()
    