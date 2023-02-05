# Talkie Toaster

[@talkietoaster@botsin.space](https://botsin.space/@talkietoaster)

This is a Mastodon bot which acts like the Talkie Toaster from Red Dwarf: a toaster which has sentient AI, who's sole goal in life and obsession is making toast. 

It is written in Python 3.11

## Operation

Talkie can do two things: offer toast generally - by posting a status to his timeline; and respond to others who interact with him.

### Announcements

Talkie will offer everyone a toasted bread product randomly. The minimum time between announcements is 15 minutes by default, and the maximum is that plus up to one day. The interval is chosen randomly. When booting for the first time, he will always toot after 30 minutes. 

### Responses

Talkie will respond to users interacting with him. 

If he sees that you have followed you, he will greet you, and offer you some toast. 

If he sees you mention him, he will reply to that status - trying to direct the conversation towards toast. He will only reply if he is the only person mentioned, so he doesn't get involve in other people's conversations if he's mentioned as part of them. 

## Installing

Use `pipenv` to install it's dependencies into a virtual environment to run it:

```sh
pip install pipenv
pipenv install
```

## Running

You'll need to set some environment variables:

* `SECRET_TOKEN` : your access token from Mastodon (found in Preferences->Development->Create a new App->Access Token)
* `BASE_URL` : the URL of the instance your account is on (for example https://botsin.space )
* `MIN_TIME_BETWEEN_ANNOUNCEMENTS_MINUTES` : the minimum time between offering toast to people (default: 15)
* `UPDATE_INTERVAL_SECONDS` : how often to do an update cycle (checking notifications, posting announcements) (default: 10)
* `STATE_FILE` : the location of the state file (to keep track of how far through the notifications you are processed)

You can run it like this:

```sh
pipenv shell
python -m bot
```

Or, you can run it with Docker. Preferably, bind mount the state file from the host (or other persistent storage) so that you can keep this between runs, preventing responding to notifications more than once.

In Linux:
```sh
docker built . -t toasterbot
docker run -e BASE_URL=https://botsin.space -e SECRET_TOKEN=**your secret token*** -e STATE_FILE=/tmp/state.json --mount type=bind,source=$(pwd)\state.json,target=/tmp/state.json toasterbot
```

In Windows:
```psh
docker built . -t toasterbot
docker run -e BASE_URL=https://botsin.space -e SECRET_TOKEN=**your secret token*** -e STATE_FILE=/tmp/state.json --mount type=bind,source=$((Get-Location).Path)\state.json,target=/tmp/state.json toasterbot
```

## Developing

This is a [Python 3.11](https://docs.python.org/3.11/) project which uses [pipenv](https://pipenv.pypa.io/en/latest/index.html) for dependencies management.

If you are using [VSCode](https://code.visualstudio.com/), there is a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) configuration to make development simpler. 

Potential improvements:

* Make the code tidier and less janktacular
* Improve the toast offer composition so that the form of the sentence isn't as predictable (i.e. can include suffixes, e.g. "would you like a piece of toast to start your day?")
* Deconstruct mentions and try to reference them in the retorts - for example, "You're talking about skiing, but wouldn't you rather have some toast?"
* Keep track of what products have been offered to each person, and if they explicitly refuse them, don't offer them that product again
* If a user actually asks for some toast, give it to them (send them a picture of some toast)
* Include a scenario where he can engage "intelligence compression" mode 


## License

This code is licensed under the MIT license. You can do anything you like to it. 