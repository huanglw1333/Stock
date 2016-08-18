# Stock

The purpose is to calculate the basic and second price of Taiwan stock.  


The py file "setup.py" is using to generate .exe file by the python module py2exe, and the build command as below,  

&gt; _python setup.py install_  
&gt; _python setup.py py2exe_

> To avoid the issue of Requests module, need to modify the following code in the source file of Request module in *\Python27\Lib\site-packages\requests\utils.py*

>`from os.path import abspath, join`  
`DEFAULT_CA_BUNDLE_PATH = join(abspath("."), "cacert.pem")`
