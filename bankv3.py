from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
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
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

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
current_tune_name = []
main_tune_list_rv = []
main_tune_list = []
tune_types_in_store_rv = []
tune_types_in_store = []
tune_keys_in_store = []
tune_keys_in_store_rv = []
update_tunes_key = []
update_tunes_type = []

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
	current_tune_name = ListProperty()
	main_tune_list_rv = ListProperty()
	main_tune_list = ListProperty()
	tune_types_in_store = ListProperty()
	tune_types_in_store_rv = ListProperty()
	tune_keys_in_store = ListProperty()
	tune_keys_in_store_rv = ListProperty()
	update_tunes_key = ListProperty()
	update_tunes_type = ListProperty()


#screens
class MyScreenManager(ScreenManager):
	pass

class LoadingScreen(Screen):
	def load_data(self):
		pass
	
class MainScreen(Screen):
	def populate_tune_types_rv(self):
		#populate the tune keys rv data
		#get all of the associeted keys for the tune types in tune_types_in_store
		tune_types_in_store_rv.clear()
		for tune in bank_v3_store:
			for k, v in bank_v3_store.find(name = tune):
				tune_types_in_store_rv.append(v['type'])
		
		tune_types_in_store_minus_duplicates = list(dict.fromkeys(tune_types_in_store_rv))
		app = App.get_running_app()
		app.tune_types_in_store_rv = [{'text': str(x)} for x in tune_types_in_store_minus_duplicates]

	def populate_tune_keys_rv(self):
		#populate the tune keys rv data
		#get all of the associeted keys for the tune types in tune_types_in_store
		tune_keys_in_store.clear()
		for tune in bank_v3_store:
			for k, v in bank_v3_store.find(name = tune):
				tune_keys_in_store.append(v['tune_key'])
		
		tune_keys_in_store_minus_duplicates = list(dict.fromkeys(tune_keys_in_store))
		app = App.get_running_app()
		app.tune_keys_in_store_rv = [{'text': str(x)} for x in tune_keys_in_store_minus_duplicates]
		print(tune_keys_in_store_minus_duplicates)

	def populalte_main_tune_list_rv(self):
		main_tune_list.clear()
		for tune in bank_v3_store:
			main_tune_list.append(tune)
		app = App.get_running_app()
		app.main_tune_list_rv = [{'text': str(x)} for x in sorted(main_tune_list)]




class TunesInBankScreen(Screen):
	def search_tune_bank(self):
		tune_search = ObjectProperty()
		tunes = []
		for item in bank_v3_store:
			tunes.append(item)
		if self.tune_search.text in tunes:
			main_tune_list.clear()
			main_tune_list.append(self.tune_search.text)
			app = App.get_running_app()
			app.main_tune_list_rv = [{'text': str(x)} for x in sorted(main_tune_list)]


class SearchScreen(Screen):
	search_screen = ObjectProperty()
	def populate_search_rv_data(self):
		print(self.search_screen.text)
		#make the api call that gets the name of the tunes to display as the rv data
		url = 'https://thesession.org/tunes/search?q={}&format=json'.format(self.search_screen.text)
		url = url.replace(' ', '%')
		print(url)
		res = UrlRequest(url, self.get_json)

	def get_json(self, req, data):
		tunes = []
		for tune in data['tunes']:
			tunes.append(tune['name'])
		app = App.get_running_app()
		app.search_result_rv_data = ({'text': x} for x in tunes)


class AddToBankPopup(Popup):
	def add_tune_to_data_base(self):
		print('got here!!')
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
		def populalte_main_tune_list_rv(self):
			main_tune_list.clear()
			for tune in bank_v3_store:
				main_tune_list.append(tune)
			app = App.get_running_app()
			app.main_tune_list_rv = [{'text': str(x)} for x in sorted(main_tune_list)]
		populalte_main_tune_list_rv(self)
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
		def populalte_main_tune_list_rv(self):
			main_tune_list.clear()
			for tune in bank_v3_store:
				main_tune_list.append(tune)
			app = App.get_running_app()
			app.main_tune_list_rv = [{'text': str(x)} for x in sorted(main_tune_list)]
		print('delete_from_tune_bank pressed')
		print(current_tune_name[0])
		bank_v3_store.delete(current_tune_name[0])
		populalte_main_tune_list_rv(self)
		

#custom widgets
		
class TuneTypesInStoreRV(RecycleView):
    def __init__(self, **kwargs):
        super(TuneTypesInStoreRV, self).__init__(**kwargs)

class TuneKeysInStoreRV(RecycleView):
    def __init__(self, **kwargs):
        super(TuneKeysInStoreRV, self).__init__(**kwargs)

class MainTuneListRV(RecycleView):
    def __init__(self, **kwargs):
        super(MainTuneListRV, self).__init__(**kwargs)


class SearchRV(RecycleView):
    def __init__(self, **kwargs):
        super(SearchRV, self).__init__(**kwargs)

class MainTuneListRVButton(Button):

	def open_tune_popup(self):
		current_tune_name.clear()
		current_tune_name.append(self.text)
		print(current_tune_name[0])
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
		print('function called')

class DisplayTunesScreenButton(Button):
	def open_tune_popup(self):
		current_tune_name.clear()
		current_tune_name.append(self.text)
		print(current_tune_name[0])
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
		print('function called')

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabelTuneType(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabelTuneType, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabelTuneType, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            main_tune_list.clear()
            update_tunes_type.append(self.text)
            print('update tune type list', update_tunes_type)
            for tune in bank_v3_store:
                if len(update_tunes_key) >= 1:
                    for tune in bank_v3_store:
                        if bank_v3_store.get(tune)['type'] in update_tunes_type:
                            if bank_v3_store.get(tune)['tune_key'] in update_tunes_key:
                                main_tune_list.append(bank_v3_store.get(tune)['name'])

                elif bank_v3_store.get(tune)['type'] in update_tunes_type:
                    main_tune_list.append(bank_v3_store.get(tune)['name'])



            app = App.get_running_app()
            app.main_tune_list_rv = [{'text': str(x)} for x in sorted(list(dict.fromkeys(main_tune_list)))]
        else:
            #print("selection removed for {0}".format(rv.data[index]))
            try: 
                main_tune_list.clear()
                update_tunes_type.remove(self.text)
                print('update tune type list', update_tunes_type)
                for tune in bank_v3_store:
                    if len(update_tunes_key) >= 1:
                        for tune in bank_v3_store:
                            if bank_v3_store.get(tune)['type'] in update_tunes_type:
                                if bank_v3_store.get(tune)['tune_key'] in update_tunes_key:
                                    main_tune_list.append(bank_v3_store.get(tune)['name'])

                    elif bank_v3_store.get(tune)['type'] in update_tunes_type:
                        main_tune_list.append(bank_v3_store.get(tune)['name'])

        
                if len(main_tune_list) == 0:
                	for tune in bank_v3_store:
                		main_tune_list.append(tune)
                	app = App.get_running_app()
                	app.main_tune_list_rv = [{'text': str(x)} for x in sorted(list(dict.fromkeys(main_tune_list)))]


                else:
                	app = App.get_running_app()
                	app.main_tune_list_rv = [{'text': str(x)} for x in sorted(list(dict.fromkeys(main_tune_list)))]
            except:
            	pass

class SelectableLabelTuneKey(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabelTuneKey, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabelTuneKey, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            main_tune_list.clear()
            update_tunes_key.append(self.text)
            print('update tune key list', update_tunes_key)
            for tune in bank_v3_store:
                if len(update_tunes_type) >= 1:
                    for tune in bank_v3_store:
                        if bank_v3_store.get(tune)['type'] in update_tunes_type:
                            if bank_v3_store.get(tune)['tune_key'] in update_tunes_key:
                                main_tune_list.append(bank_v3_store.get(tune)['name'])

                elif bank_v3_store.get(tune)['tune_key'] in update_tunes_key:
                    main_tune_list.append(bank_v3_store.get(tune)['name'])

            app = App.get_running_app()
            app.main_tune_list_rv = [{'text': str(x)} for x in sorted(list(dict.fromkeys(main_tune_list)))]
        else:
            #print("selection removed for {0}".format(rv.data[index]))
            try: 
                main_tune_list.clear()
                update_tunes_key.remove(self.text)
                print('update tune key list', update_tunes_key)
                if len(update_tunes_type) >= 1 and len(update_tunes_key) == 0:
                	for tune in bank_v3_store:
                		if bank_v3_store.get(tune)['type'] in update_tunes_type:
                			main_tune_list.append(bank_v3_store.get(tune)['name'])


                elif len(update_tunes_type) >= 1:
                    for tune in bank_v3_store:
                        if bank_v3_store.get(tune)['type'] in update_tunes_type:
                            if bank_v3_store.get(tune)['tune_key'] in update_tunes_key:
                                main_tune_list.append(bank_v3_store.get(tune)['name'])

                elif bank_v3_store.get(tune)['tune_key'] in update_tunes_key:
	                    main_tune_list.append(bank_v3_store.get(tune)['name'])

                if len(main_tune_list) == 0 and len(update_tunes_key) == 0 and len(update_tunes_type) == 0:
                	for tune in bank_v3_store:
                		main_tune_list.append(tune)
                	app = App.get_running_app()
                	app.main_tune_list_rv = [{'text': str(x)} for x in sorted(list(dict.fromkeys(main_tune_list)))]


                else:
                	app = App.get_running_app()
                	app.main_tune_list_rv = [{'text': str(x)} for x in sorted(list(dict.fromkeys(main_tune_list)))]
            except:
            	pass

if __name__ == '__main__':
	BankV3App().run()