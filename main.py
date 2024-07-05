from PIL import Image, ImageGrab
import pytesseract
import os, time
import translators as ts
import translators.server as tss
import wx 
import threading

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Translator:
    def get_lines(self, x1, y1, x2, y2):
        bbox = (x1, y1, x2, y2)
        im = ImageGrab.grab(bbox)

        text_raw = pytesseract.image_to_string(im, lang="eng", config='--psm 3')
        text = text_raw.replace('/', '!')

        text = '\n'.join([linea.rstrip() for linea in text.splitlines() if linea.strip()])
        lines = text.splitlines()

        return lines

    def start_reading(self, x1, y1, x2, y2):
        frame = TextFrame(None, title="Text and Translation")
        frame.Show()

        frame.SetWindowStyle(wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE)  # Mantener el marco siempre en la parte superior y permitir el movimiento

        def read_text():
            lines = ''
            while True:
                new_lines = self.get_lines(x1, y1, x2, y2)

                if lines != new_lines:
                    lines = new_lines
                    frame.update_text(lines)
                time.sleep(0.1)  

        # Inicia el hilo para el procesamiento de texto
        threading.Thread(target=read_text, daemon=True).start()

class TextFrame(wx.Frame):
    def __init__(self, parent, title):
        super(TextFrame, self).__init__(parent, title=title, size=(400, 300))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        
        panel.SetSizer(vbox)
        self.Centre()

    def update_text(self, lines):
        self.text_ctrl.SetValue('')
        for line in lines:
            self.text_ctrl.AppendText('Original: ' + line + '\n')
            self.text_ctrl.AppendText('Traducción: ' +ts.translate_text(line, to_language='es') + '\n')
            self.text_ctrl.AppendText('--------------------------------------\n')

class DesktopController(wx.Frame):
    def __init__(self, parent, title):
        super(DesktopController, self).__init__(parent, title=title)
        self.SetTransparent(200)

        self.button = wx.Button(self, label="Click Me")
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.button)

        self.SetPosition(wx.Point(0, 0))
        self.Show()

    def on_button_click(self, event):
        size = self.button.GetSize()
        x1, y1 = self.button.GetScreenPosition()
        x2, y2 = x1 + size[0], y1 + size[1]

        self.Hide()

        # Iniciar la traducción
        Translator().start_reading(x1, y1, x2, y2)

if __name__ == '__main__':
    app = wx.App()
    mf = DesktopController(None, title="Selecciona área")
    app.MainLoop()
