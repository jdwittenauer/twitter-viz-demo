import time

from pattern.web import Twitter

# Another way to mine Twitter is to set up a stream.
# A Twitter stream maintains an open connection to Twitter,
# and waits for data to pour in.
# Twitter.search() allows us to look at older tweets,
# Twitter.stream() gives us the most recent tweets.

# It might take a few seconds to set up the stream.
stream = Twitter().stream("win", timeout=30)

for i in range(100):
    print i
    # Poll Twitter to see if there are new tweets.
    stream.update()
    # The stream is a list of buffered tweets so far,
    # with the latest tweet at the end of the list.
    for tweet in reversed(stream):
        print tweet.text
    # Clear the buffer every so often.
    stream.clear()
    # Wait awhile between polls.
    time.sleep(1)