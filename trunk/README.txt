Hi!

So this is a very early version. Not ready for prime time.
But if you are so interested as to jump into sharks just to
be able to get your greasy fingertips all over your shiny
new 24 inch HD LCD monitor setup, this file may guide you in
the epic journey of doing so.

So the first part is getting stuff from SVN, which I figure 
you have already done so, or you are using that text browser
on Google Code and then you are lame. So the first thing you 
need to do is to svn checkout and get a local copy of this
folder.

After that, you need to make sure your webcam works. Actually
this should be step -1, because there's no way for it to work
if it doesn't work. Make sure it works somewhere.

If you run Windows, please read up on VideoCapture's API and
port this over to VideoCapture. It honestly shouldn't be hard
at all. The file that you may need to edit is shinytouch.py and
you should learn by comparing videocapture.py and webcam.py
both in the test directory of this folder.

You need OpenCV (or VideoCapture if you port it on windows), 
PIL and pyGame.  

NOT FINISHED
