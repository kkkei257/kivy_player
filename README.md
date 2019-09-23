# kivy_player

## 概要
Kivyを用いて音楽プレーヤーを作成しました。macOSとAndroidで動作確認済みです。<br><br>

・再生/一時停止ボタンを押すと楽曲の再生（再生中の場合は一時停止）、＞ボタンで次のトラック、＜ボタンで前のトラックを再生することができます。

・右下のアイコンは再生リストでこのボタンを押すと再生リストを表示させることが出来ます。再生リストにおいて曲名を選択するとその曲を再生することができます。

・右上には2つアイコンがあり、右は歌詞の表示/非表示ボタンでここを押すと歌詞を表示したり非表示にできます。なお長押しすると歌詞の色を黒/白と変更することもできます。<br>
また左のアイコンはフォルダボタンで、ここから別の音楽フォルダを参照することができます。初期状態ではsoundフォルダ内の楽曲を再生リストに登録するようになっており、別のフォルダの楽曲を再生したい場合にはこのフォルダアイコンから該当するフォルダを選択してください。

・再生中にスライドバーを動かすと再生位置を変えることができます。スライドバーの値(再生時間[秒])が変更される度にon_value部分の関数が実行されるので、そのことを利用してスライドバーを動かす度にpygame.micxer.music.play()の引数にスライドバーの値を渡しその部分から再生されるようにしています。
~~~
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

        Holder.setSlideValue(self.ids.slider.value)

    except:
        pass
~~~
なお再生中1秒ごとにスライドバーが動きますが、変化分が1秒の場合はこの処理が行われないようになっています（schedule_intervalによりpositionメソッドが繰り返し実行されるようになっており、このpositionメソッドを用いてスライドバーの位置が自動的に1秒ごとに動くようにしています）。

最後まで再生されると自動的に次のトラックが再生されます。
~~~
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
~~~
<br>
・アルバムアートについては指定したフォルダ内に楽曲と同じ名前のjpgファイルがあればそれを読み出し、なければフォルダ内に存在するjpgファイルを、画像データが存在しなければimageフォルダ内にあるデフォルトの画像を読み込むようになっています。そのため好きな画像をアルバムアートとして表示できます。<br>
また楽曲と同じ名前のtxtファイルがあれば楽曲再生時にtxtファイル内の文字列が歌詞としてアルバムアート上に表示されます（txtファイルが存在しなければ表示されない）。歌詞は右上のアイコンを押すことで非表示にすることも可能です。

<br>余談：<br>
初めは音楽ファイルの再生にvlcのMediaPlayerを使用しようと思っていたのですが、androidでプログラムを実行する際にエラーが出てしまったのでpygameのmixerを用いています。pygame.mixer.music.play()の引数に再生位置を与えることで任意の位置から再生することができます。


<img src="screenshot1.png" width="33%"> <img src="screenshot2.png" width="33%"> <img src="screenshot3.png" width="33%">
