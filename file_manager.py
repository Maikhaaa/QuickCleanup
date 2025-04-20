from pathlib import Path
import os, shutil

class ManagedFile:
	def __init__(self, path: str) -> None:
		self.path = Path(path)

		if not self.path.is_file():
			raise FileNotFoundError(f"Invalid file path: {self.path}")
	
		self.name = self.path.name
		self.extension = self.path.suffix


	def move(self, target_directory: str) -> None:
		new_directory = Path(target_directory)

		if not new_directory.exists():
			new_directory.mkdir(parents = True, exist_ok = True)  # Create directory if missing
		target_path = new_directory / self.name

		try:
			shutil.move(str(self.path), str(target_path))
			self.path = target_path  # Update path only if move succeeds

		except Exception as e:
			raise RuntimeError(f"Failed to move {self.path} -> {target_path}") from e

	
	def rename(self, new_name: str) -> None:
		new_path = self.get_directory() / new_name

		if new_path.exists():
			raise FileExistsError(f"File already exists: {new_path}")

		try:
			self.path.rename(new_path)
			self.name = new_name
			self.path = new_path
		except Exception as e:
			raise RuntimeError(f"Failed to rename {self.path} -> {new_name}") from e


	def get_directory(self) -> Path:
		return self.path.parent


	def get_path(self) -> Path: 
		return self.path


	def get_name(self) -> str:
		return self.path.name


	def get_extension(self) -> str:
		return str(self.extension)


	def get_size(self) -> int:
		return self.path.stat().st_size


	def __repr__(self) -> str:
		return f"ManagedFile({self.path})"


managed_files: list[ManagedFile] = []

def rename(file: ManagedFile, new_name ) -> None:
	file.rename(new_name)


def find_files(mode: str, value) -> list[ManagedFile]:
	def filter_files(function) -> list[ManagedFile]:
		files = [*filter(function, managed_files)]
		return files 
	if mode not in {'type', 'name', 'size'}:
		raise ValueError('Invalid mode provided')
	if mode == 'name':
		return filter_files(lambda x: value in x.get_name())
	elif mode == 'type':
		return filter_files(lambda x: value == x.get_extension())
	elif mode == 'size':
		return filter_files(lambda x: x.get_size())
	return []

def load_files(directory: str) -> None:
	path_directory = Path(directory)

	managed_files.clear()
	file_names = os.listdir(directory)

	for name in file_names: 
		load_file(str(path_directory / name))


def load_file(file_path: str) -> None:
	file_path_path = Path(file_path) 

	if not file_path_path.exists():
		raise Exception('Invalid file path')

	if file_path_path.is_dir():
		print(f'{file_path} is not a file')
		return

	new_managed_file = ManagedFile(file_path)
	managed_files.append(new_managed_file)
