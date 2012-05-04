import os

def gitupdate():
	os.system("""
		mkdir ~/bin/.fitupdate
	 && git clone -b git://github.com/CarlQLange/fit.git master
	 && ./install.sh
	 && rm -r ~/bin/.fitupdate
	""")