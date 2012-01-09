fit - a basically psychic iTunes controller, kind of
========

The fastest way to show how how this is cool is to show you. This is how it goes:

	~ $ fit "play some songs by the foo fighters"
	Playing Everlong by Foo Fighters
	Took 3.789 seconds.
	~ $ 

##So basically

fit is an iTunes controller that tries to understand natural English commands.

I wrote fit as a command-line application so I wouldn't have to tab out of vim to change my song. It's since gotten a web interface too, so you can do it from your browser. AND it has speech support so you can talk to it!

##it still sucks though

fit works by getting the Levenshtein distance from your input to the songs in your iTunes library. (Levenshtein distance is basically an easy way to measure how different two strings are)

Levenshtein distance is _very_ imperfect for this usage. For example:

	~ $ fit "play lower your eyelids"
	Playing Know your enemy
	Took 5.429 seconds.
	~ $ fit "play lower your eyelids to die"
	Playing Closer To The Edge
	Took 5.835 seconds.
	~ $ fit "play lower your eyelids to die with the"
	Playing Lower Your Eyelids To Die With The Sun
	Took 6.485 seconds.
	~ $ 

That _should_ have played M83's awesome 3am song "Lower Your Eyelids To Die With The Sun" BUT IT DIDN'T.

However, you can narrow down what you want by, for example, telling fit who plays the song. (This still doesn't work for the above example, because Levenshtein distance doesn't equalise the length of the strings)

Also, speech support is flaky. This mightn't be the case for you, but it has a damn hard time understanding my irish accent.

##Can I use it right now?

Yes! If you like. 

However, this only works on OSX. That's just how life goes - until Windows has Applescript (as in, never) I don't think it's possible to interact with iTunes.
I use applescript to play, pause, and generally make iTunes do things. No other way, as far as I know.

Also! You need python3. Apparently it doesn't come installed by default on OSX, so you'll have to get it yourself. You do that by grabbing the installer from http://python.org/download/releases/3.2.2/ and running it. You could also do 

	brew install python3

if you have brew installed (which you should because package managers are pretty much the best thing). Thanks to Teddy Cross (@tkazec) for pointing this out to me!

For speech support you need sox installed. Note that fit runs fine without this though, and you still get speech support in-browser (if your browser supports x-webkit-speech).

	brew install sox

*ANYWAY* on OSX you can do 
	
	 $ cd /where/you/downloaded/fit/to
	 $ python3 ./fitunes.py "play till the world ends"

and it will probably work! Maybe!

*OR*

You can actually install fit as an executable-type-thing! Just do 

	 $ cd /where/you/downloaded/fit/to
	 $ ./install.sh

and then you can do

	~ $ fit "play densmore by anamanaguchi"

or you can do 
	
	~ $ fit serve

and then point your browser at 127.0.0.1:5171/_fit/web/ (this is probably what you want to do if you don't use the command-line much)