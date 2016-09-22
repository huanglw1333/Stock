from distutils.core import setup
import py2exe

includes = ['sys', 'time']
packages = ['requests', 'bs4', 'Tkinter', 'webbrowser']

setup(
	windows = ['buyNsell_ui.py'],
	#console = ['tk_ui.py'],
	options = {'py2exe': {'packages':packages,
						  'includes':includes}},
	data_files = [r'C:\Python27\Lib\site-packages\requests\cacert.pem']
	)
