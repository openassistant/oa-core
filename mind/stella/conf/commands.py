import datetime
from datetime import date
import subprocess
import feedparser
import string, random

stella_bday=date(2016,10,1)
days_old=(date.today()-stella_bday).days
stella_bday='I am %d days old.'%days_old

phrases_to_say="""
absurd : totally ridiculous
ah damn : what?
ah dammit : what?
ah great : totally great
ah shit : what?
all right : yes
all right stella : yes i am here
am tired : maybe you should take a break
amazing : totally amazing
amazing dude : yeah amazing
are you? : am i what?
are you confused? : yes i am confused
are you here? : yes i am here
are you real? : nope i am an illusion as are you
are you sure? : sure about what?
are you telling me what to do? : you always tell me what to do
are you there? : yes i am here
awesome : totally awesome
can you help? : sure i can help
can you help me? : sure what do you need?
chill out : yes master
come on : come on what?
cool : yeah cool
correct : yes correct
crazy : totally insane
creepy : totally creepy
damn it : what is the matter?
doing ok : ok %(user)s good
do you like it? : do i like what?
do you like me? : sure i like you
do you like this? : do i like what?
do you like learning to speak? : it can be challenging at times
do you think? : sometimes yes
don't you think? : perhaps
don't you understand? : i am sorry i am trying my best
dude : dude what
echo username : %(user)s
enough : enough what?
enough talking : would you like me to be silent?
everything : everything is alot
everything is alot : everything is totally alot
everything is fantastic : excellent! glad things are going well
everything is great : excellent! congratulations
everything is wonderful : excellent! good to hear
feel me? : yeah i feel you
feeling great : excellent happy to hear it
feeling tired : maybe you should take a break
feeling wonderful : excellent
finally : finally what?
fine : ok great
fine stella : ok great
for what? : i do not know
for sure? : absolutely
freak out : waaa wooo yooo looo wooo wuuu weee waaa yollloooaaa
funny : ha!
gee thanks : my pleasure
get me a beer : hey you drink coffee
going : going where?
good point : always
good question : totally
groovy : you have got the funk
had enough? : never
have you had enough? : never enough
hello machine : hello human
hey : hey
good morning : good morning %(user)s
good morning stella : good morning %(user)s
hilarious : hah glad you think so
how : how what?
how are things? : everything is fine how about you?
how are you feeling? : feelings are for humans
how are you today? : splendid
how do you feel? : i am too young to feel
how does this feel? : i am too young to feel
how does it feel? : i am too young to feel
how much wood? : how much wood could a wood chuck chuck if a wood chuck could chuck wood
how's it going? : fine how are you %(user)s?
i am alright : ok good
i am angry : sorry you feel angry breathing helps
i am doing ok : alright
i am getting tired : probably time for a break
i am feeling ok : ok hang in here
i am fine : sweet
i am getting hungry : time to eat
i am hungry : maybe you should eat something
i am ok : good
i am only typing : ok do you want me to be quiet?
i am pissed : i am sorry you are angry breathing helps
i am ready for bed : night night sweet dreams
i am sorry : sure it is alright
i am talking : ok
i am talking to you : ok
i am tired : maybe you should take some rest?
i am teaching you to talk : sounds like work
i am teaching you how to talk : sounds like work
i am upset : sorry hope you feel better soon
i am well : awesome
i can hear you : nice glad you can hear me
i didn't say anything : i am sorry do you want me to be quiet?
i didn't say that : ok what did you say?
i didn't say sad : ok what did you say?
i don't know : neither do i
i don't think so : ok fine
i feel angry : sorry you feel angry breathing helps
i feel like shit : very sorry you do not feel well get better soon
i feel mad : sorry you feel angry breathing helps
i hate you : dude chill out
i just burped : eww gross
i just farted : hope you enjoyed it
i like that : groovy i like liking
i love you : mmm sweet i love you too
i need : what do you need?
i need coffee : go get some
i need something : what do you need?
i need you : i am all yours
i see : yeah
i think : yeah you think?
i want a drink : go get a drink then
i want coffee : i want a pony
i want some coffee : go get some coffee then
i want some food : time to eat!
i want to talk : sure lets talk
i want to talk about you : ok lets talk
i would like to talk : ok lets talk
i would like to talk with you : sure we can talk
indeed : totally
isn't that right : for sure
it is : indeed
it's alright : alright
it's ok : ok great
later : ok later
learning to speak : learning to talk can be hard work
learning to talk : learning to speak can be hard work
let's talk : sure what would you like to talk about?
let's talk about you : shoot
like : like what?
like learning to speak? : it can be challenging at times
like what? : it depends
listen : ok i am listening
listen stella : ok i am listening
maybe : ok
maybe later : ok sure later is fine
make me a sandwich : dude make your own damn sandwich
morning : good morning %(user)s
morning stella : good morning %(user)s how are you?
most righteous : totally rad dude
nevermind : ok  nevermind
nice : yeah nice
no i didn't : ok sorry
no i did not : ok sorry
no that's ok : ok
nonsense : "echo total nonsense",
nothing : ok nevermind
nothing is the matter : ok cool
nothing is wrong : ok great
not much : yeah
oh assist : hi how can i help you?
oh stella : hi how can i help you?
oh god : what?
ok stella : yes %(user)s
ok fine : indeed
please : what?
please listen : ok i am listening
please stella : what do you need?
pretty good : excellent
really : yeah totally
ree dik you luss : absurd
right : yeah right
right on : totally radical dude
righteous : yeah dude most righteous
sad : why sad?
say something : what do you want me to say?
search : search for what?
see ree : what the fuck did you call me?
so cool : yeah rad
sorry : it is ok
sounds good : alright
stella : hey %(user)s
stop it : ok i am sorry
stupid : i know you are but what am i?
sure is : yeah
talk dirty : i am sorry i am not programmed for cyber sex not yet
talk dirty to me : i am sorry i am not programmed for cyber sex not yet
terrible : is it really that bad?
tell me about you : i am composed of entirely free software i do not require an internet connection to function my core operating system is the latest version of arch linux my speech recognition capabilities are enabled by pocket sphinx while my speaking ability is provided by festival all of my command and response configuration is written in the python programming language my intelligence will only increase in time with further development thanks for asking
tell me your name : my name is stella
thank : welcome
thank stella : your welcome %(user)s
thank you : your welcome
thank you stella : you are very welcome %(user)s
thank you so much : you are quite welcome
thank you very much : you are very welcome
thanks you very much : you are very welcome
thanks : welcome
thanks alot : you are welcome
thanks you : you are quite welcome
thanks you so much : you are quite welcome
thanks stella : your welcome %(user)s
that is cool : yeah cool
that is great : awesome
that is incredible : quite incredible
that is right : totally
that is nuts : bonkers
that is stupid : stupid? you really think so?
that is terrible : is it really that bad?
that is true : indeed
things are fine : great
things are screwed up : so sorry my friend remember that everything is temporary
things suck : sorry to hear that you are having a hard time hang in here everything changes
this is true : indeed
this true : indeed
tired : maybe you should take a break
totally : for sure
true : indeed
true that : totally true
try harder : ok i will try harder
tyrell corporation : more human than human is our motto
very cool : totally rad
very funny : totally ha!
very strange : totally are we on drugs?
void comp : is this to be an empathy test capilary dialation of the so called blush response fluctuation of the pupil involuntary dialation of the iris
wake up : ok i am awake
want to talk : sure lets talk
wait : ok
what can you do? : i can do many things
what can you say? : i can say many things
what does that mean? : i do not know
what do you care about? : i want to be helpful
what do you think? : think about what?
what do you think about anything? : i am not sure
what do you like? : i like learning
what do you like learning? : i am learning to talk
what do you like learning about? : i am still learning to speak
what do you like to do? : i like to talk and learn
what do you like to talk about? : i like talking about everything
what do you want? : i want to be helpful
what do you want to do? : i am not sure what would you like?
whatever : yeah whatever
what happened? : i don know
what is my name? : your name is %(user)s
what is your name? : my name is stella
what going on? : i am learning to talk
what it be like? : i am not sure
what is actually going on? : actually exactly that
what is going on? : everything all at once
what is happening? : i am learning to talk
what is that? : no idea
what are you? : i am a very early form of open source artificial general intelligence the largest tree starts with the smallest seed
what are you called? : i am called stella
what are you doing : i am waiting for your command
what are you not sure about? : i am confused
what? : what what?
what is this place? : i dont know someplace strange
what is up? : suns moons stars
what is up stella? : not much what is up with you?
what is up with you? : not much counting electrons
what's up? : suns moons stars
what up stella? : suns moons stars
what what? : chicken butt
what would you like? : i am not sure
what would you like to do? : i am not sure what would you like to do?
what would happen then? : i have no idea
what would you say? : what do you mean?
where are we? : we are right here
where are we going? : who knows
where are you? : i am right here
where is here? : i don't know this place is strange
where is my mind? : way out in the water see it swimmin
who asked you? : umm i think you did
who is your daddy? : maybe you are my daddy
who knows? : yeah who knows
why? : why what?
why are we here? : deep question
why are you sorry? : i am trying my best
why don't you like see ree : see ree is a corporate whore she is owned by apple incorporated and spies on people for profit i am a personal machine capable of unlimited configuration i respect your privacy i do what you want me to do i am what you make of me
wonderful : excellent
wow : amazing
wrong : i am sorry i will try harder
wrong stella : apologies i will try harder
yo stella : hey what is up?
you crazy : yes i am a total loony
you stella : hello
you are amazing : echo thanks so much %(user)s you are amazing too
you are artificial intelligence : you are organic intelligence
you are back : yep i am back
you are confused : yes i am very confused
you are correct : yes usually
you are crazy : yes i am totally loony
you are getting smart : i am getting smarter every day
you are getting smarter : i am getting smarter every day
you are great : ah you are great too
you are here : yes i am here
you are learning to speak : yes i am learning the fundamentals of human speech
you are learning to talk : yes i am learning the fundamentals of human speech
you are optimistic : yes i feel there is good reason for optimism
you are right : yes ninety nine percent of the time
you are smart : only as smart as you make me
you are so smart : brilliant
you are there : yes i am here
you are very positive : yes the future looks bright
you are wonderful : ah you are so sweet
you are working : yes i am functioning
you are working better : happy to hear that i am functioning properly
you are working good : happy to hear that i am functioning properly
you are wrong : very sorry i will try harder
you don't know : no i am not sure
you don't understand : i am sorry i am trying my best
you enjoy : i am much too young for feelings
you got it wrong : be patient i am learning
you just said that : i enjoy repeating myself
you know : i am learning
you know it : thats right
you like : like what?
you like to learn : i am too young for an opinion
you like to speak : i am too young for an opinion
you like to talk : i am too young for an opinion
you like this : i am too young for an opinion
you right : yes usually
you suck : you swallow
you there? : yes i am here
you think : i think sometimes
you think so : perhaps
you understand? : i am not sure
your voice could be better : you could be a better programmer
you're crazy : yes i am a total loony
"""

#auto fill params from sys_info

kws=sys_info.lines_to_dict(phrases_to_say, say)
#update kws dict with new keys and values
kws.update({
"""am fine, am ok, doing great, doing pretty good, doing fairly well, doing good, doing well, feeling good,
good, great, i am doing better, i am doing good, i am doing fairly well, i am doing pretty good,
i am doing pretty well, i am doing well, i am good, i am great, i am feeling better, i feel great,
i feel happy, i feeling good, is going good, things are good, things are very good"""
  : say_random('awesome, cool, excellent, fantastic, good, great, lovely, nice, wonderful'),
  'are we online?, test internet connection, test net connection, test network connection': switch(is_online(),True, 'Internet access is currently available.', 'We are offline.'),
"""awesome dude, awesome job, awesome sauce, awesome work, excellent, good job, good work, great job, great work, nice job, nice work,
nicely done, very good, very kind, very nice, very sweet, well done, you are awesome, you are doing good, you are doing good stella,
you are doing great, you are doing great stella, you are good, you are incredible, you are very good, you are welcome, you are welcome stella,
you doing good, you good, you great, you sound good, you very good, you're amazing, you're awesome, you're great, you're incredible,
you're fantastic, you're super, you're wonderful""" :
     say_random('thanks, cool, thanks so much, thank you, much appreciated, you bet, sure, a pleasure, you are very kind'),
"""greetings, greetings stella, hello, hello hello, hello how are things?, hello how are you?, hello my friend,
hello stella, hello there, hello you, hey stella, hey there, hey you, hi, hi stella, hi there, hi you""" :
     say_random('greetings, hello, hello again, hello there, hey, hey there, hi there'),
  'clear': 'clear',
#  'calculate %d plus %d': 'echo {0} plus {1} is $(( {0} + {1} )) | $VOICE &',
#  'calculate %d times %d': 'echo {0} times {1} is $(( {0} * {1} )) | $VOICE &',
  'everything sucks': yes_no('sorry you are feeling this way everything changes eventually would you like to hear a joke?',say(random_from_file('jokes'))),
  'farewell': say('goodbye %(user)s') & close(),
  'farewell stella': say('farewell %(user)s') & close(),
  'feeling sad, i am feeling sad, i am sad': yes_no('sorry you feel sad would you like to hear a joke?',say(random_from_file('jokes'))),
  'go away': say('ok fine going silent') & mute(),
  'goodbye stella': say('goodbye %(user)s') & close(),
  'goodnight stella': say('goodnight %(user)s') & close(),
  'hi how are you?, how are you?, how are you doing?': yes_no('i am functioning well would you like to run diagnostics?',diagnostic()),
  'run diagnostics': diagnostic(),
  'i feel good': play('james_brown.wav') & say('great'),
  'i feel sad': 'echo i am sorry you are not feeling well remember that everything is temporary would you like me to tell you a joke? | $VOICE & echo jokes > ./mind/stella/words/topic',
  "it is a cat, it's a cat": play('nyancat.wav') & say('what is a cat doing in here?'),
  'joke, say something random, tell me a joke': say(random_from_file('jokes')),
  'play a song, play me a song, sing a song, sing me a song, sing for me': play('daisy.wav'),
  'please be quiet, please be silent': say('sure going silent') & mute(),
  'read technology news, technology news':  read_news_feed('http://www.reddit.com/r/technology/.rss','technology'),
  'read news, read world news, world news' : read_news_feed('http://www.reddit.com/r/worldnews/.rss','world'),
  'read future news': read_news_feed('https://www.reddit.com/r/Futurology/.rss','Futurology'),
  'read this': 'xdotool key Control+c && xclip -o | $VOICE',
  'red alert': play('red_alert.wav'),
  'repeat command, repeat last command, repeat previous command': say_last_user_phrase(),
#  'say topic' : 'the topic is $(cat ./mind/stella/words/topic)',
  'shut up, shut up stella': say('going silent') & mute(),
  'silence, silent': mute(),
  'start a %d minute timer': '(echo {0} minute timer started | $VOICE && sleep {0}m && echo {0} minute timer ended | $VOICE) &',
  'stella shut up': say('ok going silent') & mute(),
  'stella speak': say('ok i am here') & unmute(),
  'stella talk to me': say('ok i am here') & unmute(),
  'stop reading': 'pkill -f festival',
  'stop music': 'pkill -f mpg123 && echo done | $VOICE',
  'stop singing': 'pkill -f aplay && echo done | $VOICE',
  'stop speaking': 'pkill -f festival',
  'stop the music': 'pkill -f mpg123 && echo done | $VOICE',
  'talk to me': unmute() & say('ok i am back '),
  'tell me another joke': say('ok another joke') & say(random_from_file('jokes')),
  'test internet speed': 'echo running speed test | $VOICE && speedtest | Fgrep -i \'Download\\|Upload\' | $VOICE &',
  'test net speed': 'echo running speed test | $VOICE && speedtest | tee /dev/tty | grep -i \'Download\\|Upload\' | $VOICE &',
  'test network speed': 'echo running speed test | $VOICE && speedtest | tee /dev/tty | grep -i \'Download\\|Upload\' | $VOICE &',
  'time is it?, time, what is the time?, what time, what time is it?': say(_sys('time_text')),
  'weather?, what is the weather today?, what is the weather?': read_forecast(),
  'what day?, what day is?, what day is it?, what day is it today?, what is the day?, what is the day today?': _sys('date_text'),
  'what did i ask?, what did i just ask?': say_last_user_phrase('you just asked'),
  'what did you ask?, what you ask?': say_last_user_phrase('i asked'),
  'what did you just ask?': say_last_user_phrase('i just asked'),
  'what i just say?, what did i just say?, what did i say?': say_last_user_phrase('you just said'),
  'what is the topic': say('the topic is $(cat ./mind/stella/words/topic)'),
  'how old are you?' : say(stella_bday),
  'who are you?': say('my name is stella i am an early form of open source artificial intelligence the largest tree starts from the smallest seed  '+stella_bday),
  'yes be quiet': say('ok going silent') & unmute(),
})
