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

#data store
bank_v3_store = JsonStore('bankv3store.json')

#lists to populate rv data
tune_types_in_store = []
list_for_keys_rv = []
list_for_display_tunes_rv = []
type_pushed_ls = []


class BankV3App(App):
	tune_types_in_store = ListProperty()
	tune_type_rv_data = ListProperty()
	list_for_keys_rv = ListProperty()
	tune_keys_rv_data = ListProperty()
	list_for_display_tunes_rv = ListProperty()
	display_tune_rv_data = ListProperty()
	type_pushed_ls = ListProperty()




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
			tune_types_in_store.append(tune_in_store_type)
		app = App.get_running_app()
		app.tune_type_rv_data = [{'text': str(x + 's')} for x in list(dict.fromkeys(tune_types_in_store))]

class TuneTypesScreen(Screen):
	pass

class TuneKeysScreen(Screen):
	pass

class DisplayTunesScreen(Screen):
	pass

class SearchScreen(Screen):
	pass

class AddToBankPopup(Popup):
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
				if v['type'] == type_pushed:
					list_for_keys_rv.append(v['key'])
		app = App.get_running_app()
		app.tune_keys_rv_data = [{'text': str(x)} for x in list(dict.fromkeys(list_for_keys_rv))]

class TuneKeysRVButton(Button):
	def populate_display_tunes_rv(self):
		list_for_display_tunes_rv.clear()
		key_pushed = self.text
		type_pushed = type_pushed_ls[0]
		#populate with only the names that have the key and type pressed before
		for tune in bank_v3_store.find(type = type_pushed):
			if tune[1]['key'] == key_pushed:
				list_for_display_tunes_rv.append(tune[1]['name'])
		app = App.get_running_app()
		app.display_tune_rv_data = [{'text': str(x)} for x in list(dict.fromkeys(list_for_display_tunes_rv))]



if __name__ == '__main__':
	BankV3App().run()