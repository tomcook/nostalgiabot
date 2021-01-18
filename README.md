# nostalgiabot

This is a twitter bot that randomly selects old photos from a data source and posts them, along with some metadata, to twitter. It runs entirely within GitHub via [GitHub Actions](https://github.com/features/actions) and has no external dependencies except the Twitter API.

## Example

![example tweet](https://raw.githubusercontent.com/tomcook/nostalgiabot/main/example.png)

## Active Accounts

Currently this only posts data to the [Obama Nostalgia](https://twitter.com/ObamaNostalgia) twitter account. It can be extended to support other "nostalgia sources"  and multiple bots could run within this repo without too much effort.

## Content Licensing

More details on the licensing of this content can be found in each individual content repo's DISCLAIMER file, such as [this one](https://github.com/tomcook/nostalgiabot-obama/blob/main/DISCLAIMER.md) for the Obama archive. I believe that since everything in that repo was produced by employees of the United States Government (meaning they are in the public domain) and I'm using them for a noncommercial purpose then then this use is allowable.

## Cost

GitHub Actions are entirely free for public repositories. All of the data the bot fetches from is also stored in GitHub, either in a repository or as [Gists](https://gist.github.com/). Running this code is entirely cost free. Additionally, I make no money from the bot.

## Resources

The bot relies on three sources of data:

- **This repo** which stores the code and GitHub Actions workflow definition files. Under the [Actions](https://github.com/tomcook/nostalgiabot/actions) menu there are two separate workflows. One automatically executes every six hours and actually posts to twitter, while the other one is for manual invocation only and runs as a "Dry Run" to test the bot without posting to Twitter. The bot is written in Python.

- **Content repos** which hold the [images](https://github.com/tomcook/nostalgiabot-obama/tree/main/photos) and "memory" metadata in a [big json file](https://github.com/tomcook/nostalgiabot-obama/blob/main/memories.json). Right now the only repo in use is [nostalgiabot-obama](https://github.com/tomcook/nostalgiabot-obama).

- **A GitHub Gist** for storing long-term state. We use this to track all of the previously posted memories to ensure that we don't re-post a memory. Instead of storing this in an actual database it seemed workable to use json in a Gist, since they can store up to 10MB of text each. The current database is [here](https://gist.github.com/tomcook/d34ccb38adf1b9ec9366b892b3e40ae6).

## Future Improvements

- The bot right now just blows up if the tweet to be posted is longer than 280 characters. I've attempted to reduce the size of many of the captions provided by the White House/Archives, but many of them are very very long and would require some real editorial judgement to pare down.

- For now the bot operates on a static data source that was "frozen" in 2017 at the end of the Barack Obama administration. I'd like to add more data sources, including those that may be updating in real time, such as currently-ongoing administrations or other sources, but that would require writing a scraper and better parsers to live-extract all the data.

- Eventually the bot will post every memory in its database and break. I'll need to build a process for removing old posts from the state database so they over time be cycled back into rotation. Once that's done the bot can probably run forever, or at least until the Twitter/GitHub APIs implement breaking changes. 

- There are probably other bugs and stylistic improvements to be made to the bot code.

## Contact

If you've got questions or what to chat about this project, the best bet is to reach out to me on twitter. My handle is [@ywxwy](https://twitter.com/ywxwy). All other public contact info is on [tom.horse](https://tom.horse).
