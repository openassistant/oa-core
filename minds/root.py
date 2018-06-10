kws={
  'root mind': say('- Hello world!'),
  'close assistant': play('beep_close.wav') & mind('boot'),
  'list commands': say('- The currently available voice commands are: \n       "root mind", "what time is it", "what day is it", "what did i say", \n       "run diagnostics", "what is the weather", "read world news", "sing a song", \n        and "close assistant".'),
  'read world news': read_news_feed('https://www.reddit.com/r/worldnews/.rss', 'world'),
  'run diagnostics': diagnostics(),
  'sing a song': play('daisy.wav'),
  'what day is it': say_day(),
  'what did i say': say_last_command('You just said:'),
  'what is the weather': read_forecast(),
  'what time is it': say_time()
}
