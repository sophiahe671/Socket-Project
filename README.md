My high level-approach was to start by parsing command-line arguments to determine whether to use a TCP or TLS 
connection. The hostname and username are always required, while the port and the TLS option are optional. Once 
connected to the server, the client engages in a back-and-forth communication, sending word guesses and receiving 
feedback until the correct word is guessed or the server terminates the session.

I initially faced challenges with continuously asking for client input until the word was guessed or the server 
was disconnected. To solve this issue, I wrapped the input in a while look that kept running. I also ran into a couple 
of issues parsing the argument inputs, and it took a couple of tries to fix the logic and allow -p port and -s argument 
to be optional while the hostname and Northeastern username arguments remained required. 

My guessing strategy was to start with a word with a lot of vowels. From there, I would try a couple words with new 
untested vowels and constants until I figured out at least 3 of the letters in the word. From there, I used a 
trial-and-error approach to complete the word.

To test my code, I ran all 4 possible input strings. This included testing TCP/TLS with and without a port specified. 
When running the game, I tested both valid and invalid inputs. Invalid inputs included words that were not 5 letters or 
not in the word list. I completed the game multiple times to ensure the secret flags matched.