import dearpygui.dearpygui as dpg
from pathlib import Path
import file_manager as fm
import rule_manager as rm

home_directory: Path = Path.home()

directories = {
	'documents' : home_directory / 'documents',
	'images' : home_directory / 'images',
	'videos' : home_directory / 'videos',
	'music' : home_directory / 'music',
	'objects' : home_directory / '3d objects'
}

target_directory: Path = home_directory / 'downloads/weewoo'
sort_directory: Path = home_directory / 'downloads'


def sort_files() -> None:
	try:
		directory = get_directory()
		fm.load_files(directory)

		for rule in rm.get_rules():
			pass

	except Exception as e:
		print(f'error sorting files: {e}')


def get_directory() -> str:
	return dpg.get_value('directory')


def add_rule_to_ui() -> None:
	rule = rm.add_rule('name', '', '')
	rule.make_ui('rules-table')

# ---- ui ----

dpg.create_context()

with dpg.window(tag='main'):
	with dpg.group(horizontal=True):
		dpg.add_text('Sort through directory:')
		dpg.add_input_text(tag='directory', default_value=sort_directory)
	dpg.add_separator()


with dpg.table(tag='rules-table', parent='main'):
	dpg.add_table_column(label='Mode')
	dpg.add_table_column(label='Value')
	dpg.add_table_column(label='Target')
	dpg.add_table_column(width_fixed=True, width=100)


with dpg.group(parent='main'):
	dpg.add_button(label='add rule', callback=add_rule_to_ui)
	dpg.add_separator()
	dpg.add_button(label = 'sort', tag = 'sort', callback = sort_files)


dpg.set_primary_window('main', True)
dpg.create_viewport(title='Sorter 9000', width=600, height=300, resizable=False)
dpg.setup_dearpygui(primary_window='main')
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
