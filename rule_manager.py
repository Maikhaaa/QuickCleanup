from pathlib import Path
import uuid
import dearpygui.dearpygui as dpg

class SortingRule():
	def __init__(self, mode, value, target_directory: str):  
		self.target_directory = Path(target_directory)
		if not self.target_directory.is_dir():
			raise FileNotFoundError(f'Invalid directory path: {self.target_directory}')

		self.mode = mode
		self.value = value
		self.id = str(uuid.uuid4())


	def make_ui(self, parent: str): #TODO move this somewhere so that we ensure each rule has an ui
		with dpg.table_row(tag=f'row-{self.id}', parent=parent):
			with dpg.table_cell():
				dpg.add_combo(items=['type', 'name', 'size'], default_value='name', tag=f'combo-{self.id}', callback=self.update)	

			with dpg.table_cell():
				dpg.add_input_text(default_value='lolz', tag=f'value-{self.id}', callback=self.update)	

			with dpg.table_cell():
				dpg.add_input_text(default_value='target_directory', tag=f'target-{self.id}', callback=self.update)
			
			with dpg.table_cell():
				dpg.add_button(label='x', tag=f'delete-{self.id}', callback=lambda:remove_rule(self.id))


	def update(self):
		self.mode = self.get_mode()
		self.value = self.get_value()
		self.target_directory = self.get_target()
		print(self)


	def get_mode(self):
		mode = dpg.get_value(f"combo-{self.id}")
		return mode


	def get_value(self):
		value = dpg.get_value(f"value-{self.id}")
		return value


	def get_target(self):
		target = dpg.get_value(f"target-{self.id}")
		return target


	def __repr__(self):
		return f'SortingRule{self.mode, self.value, self.target_directory}'


sorting_rules = {}

def add_rule(mode: str, value, target_directory, parent: str="") -> SortingRule:
	new_rule = SortingRule(mode, value, target_directory)
	sorting_rules[new_rule.id] = new_rule
	return new_rule


def remove_rule(rule_id: str) -> None:
	if rule_id in sorting_rules.keys():
		print("---")
		for i in sorting_rules.keys():
			print(sorting_rules[i])
		sorting_rules.pop(rule_id)
		dpg.delete_item(f'row-{rule_id}')
		return
	raise ValueError(f'Rule with ID {rule_id} not found')


def get_all_rules() -> list:
	rules = [*sorting_rules.values()]
	return rules


def update_rule(rule_id: str, mode: str, value: str, target_directory:str):
	rule = find_rule(rule_id)
	if rule:
		rule.mode = mode
		rule.value = value
		rule.target_directory = target_directory


def find_rule(rule_id):
	for rule in sorting_rules:
		if rule.id == rule_id:
			return rule
	print(f"Couldn't find the rule with id: {rule_id}")
	return None
