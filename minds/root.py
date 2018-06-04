kws={
  'root mind': say('- Hello world!'),
  'close assistant': play('beep_close.wav') & mind('boot'),
  'list commands': say('- The currently available voice commands are, root mind, read world news, run diagnostics, sing a song, what day is it, what did i say, what is the weather, what time is it, and close assistant.'),
  'read world news': read_news_feed('https://www.reddit.com/r/worldnews/.rss', 'world'),
  'run diagnostics': diagnostics(),
  'sing a song': play('daisy.wav'),
  'what day is it': say_day(),
  'what did i say': say_last_command('You just said:'),
  'what is the weather': read_forecast(),
  'what time is it': say_time()
}
