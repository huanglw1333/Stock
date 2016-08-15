from distutils.core import setup
import py2exe

includes = ['lxml']
packages = ['requests', 'bs4', 'Tkinter']

setup(
	windows = ['tk_ui.py'],
	#console = ['tk_ui.py'],
	options = {'py2exe': { 'includes':includes, 'packages':packages}},
	data_files = [r'C:\Python27\Lib\site-packages\requests\cacert.pem']
	)