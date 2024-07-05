import wx
import translators as ts

class Translator:
    def translate_text(self, text):
        return ts.translate_text(text, to_language='es')

class TranslatorFrame(wx.Frame):
    def __init__(self, parent, title):
        super(TranslatorFrame, self).__init__(parent, title=title, size=(500, 200), style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        splitter = wx.SplitterWindow(self)
        splitter.SetMinimumPaneSize(100)  # Establece el tamaño mínimo de las partes del splitter

        panel_left = wx.Panel(splitter)
        panel_left.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)  # Agrega evento de clic izquierdo

        panel_right = wx.Panel(splitter)

        self.text_ctrl = wx.TextCtrl(panel_left, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)  # Agrega wx.TE_PROCESS_ENTER
        self.text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_translate_enter)  # Agrega evento al presionar Enter

        vbox_left = wx.BoxSizer(wx.VERTICAL)
        vbox_left.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        panel_left.SetSizer(vbox_left)

        self.translation_ctrl = wx.TextCtrl(panel_right, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox_right = wx.BoxSizer(wx.VERTICAL)
        vbox_right.Add(self.translation_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        panel_right.SetSizer(vbox_right)

        splitter.SplitVertically(panel_left, panel_right)
        self.Centre()

    def on_translate(self, event):
        text_to_translate = self.text_ctrl.GetValue()
        translated_text = Translator().translate_text(text_to_translate)
        self.translation_ctrl.SetValue(translated_text)

    def on_translate_enter(self, event):
        self.on_translate(event)  # Llama a la función de traducción al presionar Enter

    def on_left_down(self, event):
        self.CaptureMouse()  # Captura el mouse al hacer clic en el panel izquierdo
        self.delta = self.ClientToScreen(event.GetPosition())  # Obtiene la posición del clic
        self.delta = self.GetPosition() - self.delta

    def on_motion(self, event):
        if event.Dragging() and event.LeftIsDown():
            pos = wx.GetMousePosition()
            self.Move(pos + self.delta)

    def on_left_up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

class MainApp(wx.App):
    def OnInit(self):
        frame = TranslatorFrame(None, title="English to Spanish Translator")
        frame.Show(True)
        return True

if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()
