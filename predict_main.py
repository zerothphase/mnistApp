import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ObjectProperty
from kivy.uix.stencilview import StencilView
import pickle
import imageio
import utilities
import sklearn
import sklearn.neural_network
from settings import *

class PaintWidget(StencilView):
    """
    Canvas for user to draw
    """
    def on_touch_down(self, touch):
        color = (0., 0., 1.)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 24.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=12)

    # being called when an existing touch moves
    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class Main(BoxLayout):
    """
    Main window
    """
    painter = ObjectProperty(None)
    prediction_display = ObjectProperty(None)

    with open(MODEL_PATH, 'rb') as file:
        pickle_model = pickle.load(file)


    def predict(self, obj):
        """
        Make prediction on the image drawn on the PaintWidget and show
        prediction.
        """
        self.painter.export_to_png(str(TMP_IMG_PATH))
        im = imageio.imread(str(TMP_IMG_PATH), as_gray=True)
        im = utilities.normalize(im)
        pred = self.pickle_model.predict(im)
        self.prediction_display.text = str(pred[0])

    def clear_canvas(self, obj):
        """
        Clear the PaintWidget
        """
        self.painter.canvas.clear()
        self.prediction_display.text = ''


class PredictApp(App):

    def build(self):
        self.parent = Main()
        return self.parent


if __name__ == '__main__':
    print(os.path.dirname(kivy.__file__))
    PredictApp().run()
