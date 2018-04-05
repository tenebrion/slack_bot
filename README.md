# slack_bot
A bot for slack - more of an information bot.

The main program is run through bot.py

This is a personal challenge for myself that I saw on /r/learningpython. What started as a simple bot, 
turned into working with different APIs, adding features, working with json and xml, among many other things. 
The bot connects to my personal slack channel and I don't keep it running all the time. Although I could and 
did from my RaspberryPi. This is merely working with python code, making modular code, and learning new tricks.
It is fun to watch the code grow and evolve over time.

I store all my API keys in a separate TinyDB file that I query when a function is called. Before using the files,
you'll need to register with each platform to obtain API keys / accounts.

I'm continually tweaking the formatting / layout as I learn new techniques. For example, in the bot.py file 
(which is the main file), I setup the list of actions in a dictionary with the value set to the method call.

I'm always open to suggestions and feedback. It's those comments that help us newer coders learn and grow.
