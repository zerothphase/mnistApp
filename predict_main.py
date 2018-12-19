import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.stencilview import StencilView
import pickle
import imageio
import utilities


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

    # pickle_model.predict(X)

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
        # self.painter = Main()

        # main_layout = BoxLayout(orientation='horizontal')
        # painter_layout = BoxLayout(orientation='vertical')
        # btn_layout = BoxLayout(orientation='vertical', spacing=10)
        #
        # clear_btn = Button(text='Clear')
        # clear_btn.bind(on_release=self.clear_canvas)
        # save_img_btn = Button(text='Save Image')
        # save_img_btn.bind(on_release=self.save_png)
        #
        #
        # painter_layout.add_widget(self.painter)
        # btn_layout.add_widget(clear_btn)
        # btn_layout.add_widget(save_img_btn)
        #
        # # self.parent.add_widget(self.painter)
        #
        # main_layout.add_widget(painter_layout)
        # main_layout.add_widget(btn_layout)
        # self.parent.add_widget(main_layout)
        # # self.parent.add_widget(save_img_btn)
        return self.parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()

    def save_png(self, obj):
        self.painter.export_to_png("untitled.png")

if __name__ == '__main__':
    print(os.path.dirname(kivy.__file__))
    PredictApp().run()