[![PyPI version](https://badge.fury.io/py/beets-extended-metadata.svg)](https://badge.fury.io/py/beets-extended-metadata)

# Beets Extended Metadata Plugin
This is a plugin for the music management tool [beets](https://beets.io).<br>
This plugin extends beets query capabilities allowing you to query your music library based on [Extended Metadata](EMD.md).

## Disclaimer
This plugin does not help you writing Extended Metadata to your audio files.
Currently, there is no published client application that can write Extended Metadata to audio files.
If you want to use this plugin regardless, you have to write it to your files manually for now, or wait until I publish a client application some day.

## Setup

### Install the plugin

````bash
pip beets-extended-metadata
````

### Configure the plugin
Edit your [beets configuration file](https://beets.readthedocs.io/en/stable/reference/config.html) and add the following section:

````yaml
extendedmetadata:
    query_field: 'x'
    input_field: 'comments'
````

Also add *extendedmetadata* to the *plugins* section.

The *query_field* is the name for the beets internal media field where the extended meta data will be stored in beet's database.
You can choose whatever name you like, the default is *x*. This name will be used as prefix to your extended metadata queries.

The *input_field* is the name of the audio tag, according to [this audio file fields list](beetsplug/emd_audiofilefields.py), that contains your Extended Metadata string.
The value of this audio tag will be decoded and stored in the media field specified in *query_field*.
As default, the *comment* field will be used. Depending on what field you choose some software, including beets, will not be able to handle or persist it.
I recommend using the *comment* field, since most software out there will be able to work with this field and having any other information in this field is usually unnecessary.

## Usage

### Assumptions:
- You configured *x* as the query field and *comment* as the input field.
- Your library contains songs with Extended Metadata strings in the *comment* field.
- You imported the songs into your beets library after writing the metadata to the files.

### Examples

**Note**: All queries are case-insensitive.
If you have a value *Abc* it will match the query value *abc*.
If you want to query case-sensitive, use [regex queries](#searching-for-all-rock-variant-songs).

#### Searching for all russian songs

This assumes you have a custom tag *language* containing the language of the song.


````bash
beet list x:.language:russian
````

Here you can see how you can reference a custom tag from your Extended Metadata *x*.
You simply prefix it with a dot, after that the syntax is equivalent to normal beets queries.

#### Searching for all songs that use synthesizer v

This assumes you have a custom tag *vocal_synth* containing the vocal synthesizer used in the song.

````bash
beet list x:.vocal_synth:"syntheszer v"
````

You can query for values containing spaces by enclosing them in parentheses or quotes.
This is just the way a shell works and is not done by this plugin.

#### Searching for all rock variant songs

This assumes you have a custom tag *genre* containing the genre of the song.

````bash
beet list x:.genre::.+rock
````

Here you can see how you can use [regex](https://en.wikipedia.org/wiki/Regular_expression) to make your queries more flexible.
Just like with beets you can specify that your query value is regex by using the double colon *::* instead of a single colon.

#### Searching for all songs in japanese that to not come from japan from the last 3 years

This assumes you have a custom tag *language* containing the language of the song and a custom tag *origin* containing the origin country.

````bash
beet list x:.language:japanese x:.origin:'!japan' year:2010..2020
````

In this example you can see how to easily combine extended metadata queries with normal audio field queries.
It also shows how to negate query values. If you prefix the query tag value with ! it will mean *not equals* / *not contains*.
