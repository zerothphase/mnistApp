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


class PaintWidget(StencilView):

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

    painter = ObjectProperty(None)
    prediction_display = ObjectProperty(None)

    with open("pickle_model.pkl", 'rb') as file:
        pickle_model = pickle.load(file)


    def predict(self, obj):
        self.painter.export_to_png("tmp.png")
        im = imageio.imread('tmp.png', as_gray=True)
        im = utilities.normalize(im)
        pred = self.pickle_model.predict(im)
        self.prediction_display.text = str(pred[0])

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        self.prediction_display.text = ''

    def save_png(self, obj):
        self.painter.export_to_png("untitled.png")


class PredictApp(App):

    def build(self):
        self.parent = Main()
        return self.parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()

    def save_png(self, obj):
        self.painter.export_to_png("untitled.png")


if __name__ == '__main__':
    print(os.path.dirname(kivy.__file__))
    PredictApp().run()
