from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

from kivy.core.window import Window
import urllib3
import json
import threading
import time

jogador = -1
sala = -1
class Gerenciador(ScreenManager):
	pass

class Menu(Screen):
	pass

class Jogo(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		threading.Thread(target=self.ver_estado,args=()).start()
	def get_elementos(self):
		return [self.ids.id_1,self.ids.id_2,self.ids.id_3,self.ids.id_4,self.ids.id_5,self.ids.id_6,self.ids.id_7,self.ids.id_8,self.ids.id_9]
	
	def jogada(self,instance):
		global jogador
		http = urllib3.PoolManager()
		r = http.request('GET','http://62747b72735a.ngrok.io/jogada/'+str(sala)+'/'+str(jogador)+'/'+str(instance))
		data = json.loads(r.data)
		if data['situacao']:
			ids = self.get_elementos()
			if jogador == 0:
				self.get_elementos()[int(instance)-1].text = "O"
			elif jogador == 1:
				self.get_elementos()[int(instance)-1].text = "X"
			
	def ver_estado(self):
		global sala, jogador
		while True:
			time.sleep(0.1)
			http = urllib3.PoolManager()
			r = http.request('GET','http://62747b72735a.ngrok.io/estado/'+str(sala))
			data = json.loads(r.data)
			print(data)
			valores = list(data['estado'])
			for i in range(len(valores)):
				if valores[i] != 99:
					if valores[i] == 0:
						self.get_elementos()[i].text = "O"
					elif valores[i] == 1:
						self.get_elementos()[i].text = "X"

			if data['atual'] != 'ainda':
				popup = Popup(title=data['atual']).open()
				sala = -1
			
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.voltar)
	
	def voltar(self,window, key, *args):
		if int(key) == 27:
			App.get_running_app().root.current = 'menu'
			return True
		return False
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.voltar)
class Entrar(Screen):
	def __init__(self, tarefas=[], **kwargs):
		super().__init__(**kwargs)
		for tarefa in tarefas:
			self.ids.box.add_widget(Tarefa(text=tarefa))
	
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.voltar)
	
	def voltar(self,window, key, *args):
		if int(key) == 27:
			App.get_running_app().root.current = 'menu'
			return True
		return False
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.voltar)
	
	def entrar_sala(self):
		self.ids.sala.text
		global jogador, sala
		http = urllib3.PoolManager()
		r = http.request('GET','http://62747b72735a.ngrok.io/entrar/'+str(self.ids.sala.text))
		dados = json.loads(r.data)
		if dados['sala']:
			sala = int(self.ids.sala.text)
			jogador = dados['jogador']
			App.get_running_app().root.current = 'jogo'
			
			
        
'''
<CameraClick>:
	name: 'camera'
	BoxLayout:
		orientation: 'vertical'
		Camera:
			id: camera
			resolution: (640, 480)
			play: False
		ToggleButton:
			text: 'Play'
			on_press: camera.play = not camera.play
			size_hint_y: None
			height: '48dp'
		Button:
			text: 'Capture'
			size_hint_y: None
			height: '48dp'
			on_press: root.capture()



class CameraClick(Screen):
    def capture(self):
        
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        im = Image.open("IMG_{}.png".format(timestr))
        
        model = load_model('facenet_keras.h5')
        im = im.convert('RGB')
        im = im.resize((160, 160))
        im = np.array(im.getdata())
        im = im.reshape((1,160,160,3))
        im = np.array(im)
        p = model.predict(im)
        print("Captured")
class Tarefa(BoxLayout):
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        http = urllib3.PoolManager()
        r = http.request('GET', 'http://62747b72735a.ngrok.io')
        self.ids.label.text = str(r.data)
'''
class test(App):
    def build(self):
        return Gerenciador()

test().run()

