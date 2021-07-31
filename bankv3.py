from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.factory import Factory
from music21 import converter, midi
import time
from kivy.core.audio import SoundLoader
import os

#data store
bank_v3_store = JsonStore('bankv3store.json')

#lists to populate rv data
tune_types_in_store = []
list_for_keys_rv = []
list_for_display_tunes_rv = []
type_pushed_ls = []
search_result_rv_data = []
tune_clicked_id = []
tune_id = []

class BankV3App(App):
	tune_types_in_store = ListProperty()
	tune_type_rv_data = ListProperty()
	list_for_keys_rv = ListProperty()
	tune_keys_rv_data = ListProperty()
	list_for_display_tunes_rv = ListProperty()
	display_tune_rv_data = ListProperty()
	type_pushed_ls = ListProperty()
	search_result_rv_data = ListProperty()
	tune_clicked_id = ListProperty()
	tune_id = ListProperty()


#screens
class MyScreenManager(ScreenManager):
	pass

class LoadingScreen(Screen):
	def load_data(self):
		pass
	
class MainScreen(Screen):
	def populate_tune_types_rv(self):
		for tune in bank_v3_store:
			tune_in_store_type = bank_v3_store.get(tune)['type']
			if tune_in_store_type not in tune_types_in_store:
				tune_types_in_store.append(tune_in_store_type)
		app = App.get_running_app()
		app.tune_type_rv_data = [{'text': str(x + 's')} for x in tune_types_in_store]


class TuneTypesScreen(Screen):
	pass

class TuneKeysScreen(Screen):
	pass

class DisplayTunesScreen(Screen):
	pass

class SearchScreen(Screen):
	search_screen = ObjectProperty()
	def populate_search_rv_data(self):
		print(self.search_screen.text)
		#make the api call that gets the name of the tunes to display as the rv data
		url = 'https://thesession.org/tunes/search?q={}&format=json'.format(self.search_screen.text)
		url = url.replace(' ', '%')
		res = UrlRequest(url, self.get_json)

	def get_json(self, req, data):
		tunes = []
		for tune in data['tunes']:
			tunes.append(tune['name'])
		app = App.get_running_app()
		app.search_result_rv_data = ({'text': x} for x in tunes)


class AddToBankPopup(Popup):
	def add_tune_to_data_base(self):
		#https://thesession.org/tunes/2?format=json
		#make the api call that gets the name of the tunes to display as the rv data
		url = 'https://thesession.org/tunes/{}?format=json'.format(tune_id[0])
		res = UrlRequest(url, self.get_json)

	def get_json(self, req, data):
		bank_v3_store.put(data['name'], name = data['name'], tune_key = data['settings'][0]['key'], type = data['type'], abc = data['settings'][0]['abc'])
		print(data['settings'][0]['key'], data['type'], data['name'], data['settings'][0]['abc'])

class TunePopup(Popup):
	def play_tune(self):
		print('play_tune called')
		s = converter.parse('tempabc.abc')
		s.write('midi', fp='temp.mid')
		self.sound = SoundLoader.load("temp.mid")
		self.sound.play()

	def stop_tune(self):
		try: 
			self.sound.stop()
		except:
			pass

	def del_temp_mid(self):
		def stop_tune(self):
			try: 
				self.sound.stop()
			except:
				pass
		stop_tune(self)
		if os.path.exists('temp.mid'):
			os.remove('temp.mid')
			os.remove('tempabc.abc')
		else:
			os.remove('tempabc.abc')

	def delete_from_tune_bank(self):
		print('delete_from_tune_bank pressed')
		pass

#custom widgets
class TuneTypesRV(RecycleView):
    def __init__(self, **kwargs):
        super(TuneTypesRV, self).__init__(**kwargs)

class TuneKeysRV(RecycleView):
    def __init__(self, **kwargs):
        super(TuneKeysRV, self).__init__(**kwargs)

class DisplayTypesRV(RecycleView):
    def __init__(self, **kwargs):
        super(DisplayTypesRV, self).__init__(**kwargs)

class SearchRV(RecycleView):
    def __init__(self, **kwargs):
        super(SearchRV, self).__init__(**kwargs)

class TuneTypesRVButton(Button):
	def populate_tune_keys_rv(self):
		#populate the tune keys rv data
		#get all of the associeted keys for the tune types in tune_types_in_store
		type_pushed = self.text [0:-1]
		type_pushed_ls.clear()
		type_pushed_ls.append(type_pushed)
		list_for_keys_rv = []
		for tune in bank_v3_store:
			for k, v in bank_v3_store.find(name = tune):
				if v['type'] == type_pushed and v['tune_key'] not in list_for_keys_rv:
					list_for_keys_rv.append(v['tune_key'])
		print(list_for_keys_rv)
		app = App.get_running_app()
		app.tune_keys_rv_data = [{'text': str(x)} for x in list_for_keys_rv]

class TuneKeysRVButton(Button):
	def populate_display_tunes_rv(self):
		list_for_display_tunes_rv.clear()
		key_pushed = self.text
		type_pushed = type_pushed_ls[0]
		#populate with only the names that have the key and type pressed before
		for tune in bank_v3_store.find(type = type_pushed):
			if tune[1]['tune_key'] == key_pushed:
				list_for_display_tunes_rv.append(tune[1]['name'])
		app = App.get_running_app()
		app.display_tune_rv_data = [{'text': str(x)} for x in list_for_display_tunes_rv]

class SearchRVButton(Button):
	def open_popup(self):
		clicked_tune_name = self.text
		#open a pup up and get tune info with an api call
		url = 'https://thesession.org/tunes/search?q={}&format=json'.format(clicked_tune_name)
		url = url.replace(' ', '%20')
		res = UrlRequest(url, self.get_tune_id)

	def get_tune_id(self, req, data):
		tunes = []
		for tune in data['tunes']:
			if self.text == tune['name']:
				tune_id.clear()
				tune_id.append(tune['id'])

		clicked_tune_name = self.text
		AddToBankPopup.title = clicked_tune_name
		Factory.AddToBankPopup().open()

class DisplayTunesScreenButton(Button):
	def open_tune_popup(self):
		Factory.TunePopup().open()
	def create_abc_and_midi(self):
		def get_time_signature(self):
			if bank_v3_store.get(tune)['type'] == 'jig':
				return '6/8'
			elif bank_v3_store.get(tune)['type'] == 'reel':
				return '4/4'

		tune = self.text
		abc_R = "R: " + str(bank_v3_store.get(tune)['type'])
		abc_M = 'M: ' + str(get_time_signature(self))
		abc_L = 'L: 1/8'
		abc_K = 'K: '+ bank_v3_store.get(tune)['tune_key']
		abc_info = abc_R + '\n' + abc_L + '\n' + abc_M + '\n' + abc_K + '\n'
		abc_notes = str(bank_v3_store.get(tune)['abc'])
		abc_string = abc_info + abc_notes
		f = open('tempabc.abc', 'a')
		f.write(abc_string)


		




if __name__ == '__main__':
	BankV3App().run()