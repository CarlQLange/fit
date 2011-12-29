fit - a basically psychic iTunes controller, kind of
========

The fastest way to show how how this is cool is to show you. This is how it goes:

	~ $ fit play "guitar and a heart" 
	Playing A Guitar and A Heart
	Took 5.4229278564453125 seconds.
	~ $ 

##So basically

fit works by (currently) getting the Levenshtein distance of what you typed and checking it against *all* the songs in your iTunes library and getting the best match. 
It's pretty sweet!

##it still sucks though

Levenshtein distance is _very_ imperfect for this usage. For example:

	~ $ fit play "lower your eyelids"
	Playing Open Your Eyes
	Took 5.201683044433594 seconds.
	~ $ fit play "lower your eyelids to die"
	Playing How Your Heart Is Wired
	Took 5.951024055480957 seconds.

That _should_ have played M83's awesome 3am song "Lower Your Eyelids To Die With The Sun" BUT IT DIDN'T.

I have plans to fix this though.

##OH REALLY

Yes. Because I get _so_ much information from the iTunes library, there's a lot more context I should be using.
I should be, for example, able to handle 
	
	~ $ fit play "coldplay"

or 
	
	~ $ fit play "a song by anamanaguchi"

or 

	~ $ fit play "a song I like but haven't heard in a while"

(By using artists, play count, last play date, etc.)

Obviously, Levenshtein distance sucks for all of this and I'll probably need to do some actual language processing (or I can hide it behind a whole bunch of if statements because nobody knows the difference right?). I'm not doing that right now because it's 9am and I've been awake all night. 
*But!* This is cool and I'll keep working on it. _Probably_.

##Can I use it right now?

Yes! If you like. 

However, this only works on OSX. That's just how life goes - until Windows has Applescript I don't think it's possible to interact with iTunes.
I use applescript to play, pause, and generally make iTunes do things. No other way, as far as I know.

Also! You need python3. Apparently it doesn't come installed by default on OSX, so you'll have to get it yourself. You do that by grabbing the installer from http://python.org/download/releases/3.2.2/ and running it. You could also do 

	brew install python3

if you have brew installed (which you should because package managers are pretty much the best thing). Thanks to Teddy Cross (@tkazec) for pointing it out to me!

*ANYWAY* on OSX you can do 
	
	python3 ./fitunes.py play "till the world ends"

and it will probably work! Maybe!

*OR*

You can actually install fit as an executable-type-thing! Just do 

	python3 ./install.py

and it will move fit to ~/bin. (You might need to add ~/bin to your $PATH, who knows).

##but wait! there's more! (usage)

#####(un)pausing itunes
 
 	fit pause

#####next track
 
 	fit next

#####previous track

	fit prev
	fit last

#####current track

	fit current
	fit track

#####play song

	fit play "a close approximation to the name of the song you want to play"

#####play artist

	fit artist "a close approximation to the name of the artist you want to play"
