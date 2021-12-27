[![PyPI version](https://badge.fury.io/py/beets-extended-metadata.svg)](https://badge.fury.io/py/beets-extended-metadata) [![Build](https://github.com/calne-ca/beets-plugin-extended-metadata/workflows/Build/badge.svg)](https://github.com/calne-ca/beets-plugin-extended-metadata/actions?query=workflow%3ABuild)

# Beets Extended Metadata Plugin
This is a plugin for the music management tool [beets](https://beets.io).<br>
This plugin adds [Extended Metadata](https://github.com/calne-ca/beets-plugin-extended-metadata/blob/master/EMD.md) capabilities to beets.
It extends the beets query syntax, allowing you to query songs based on Extended Metadata and also allows you to write,
update and view Extended Metadata based on queries.

## Setup

### Install the plugin

````bash
pip beets-extended-metadata
````

### Configure the plugin
Edit your [beets configuration file](https://beets.readthedocs.io/en/stable/reference/config.html) and add the following section:

````yaml
extendedmetadata:
    query_prefix: 'x'
    input_field: 'comments'
````

Also add *extendedmetadata* to the *plugins* section.

The *query_prefix* defines a prefix that you need to add to the parts of your queries which should look into Extended Metadata instead of the normal metadata.

The *input_field* is the name of the audio tag, according to [this audio file fields list](https://github.com/calne-ca/beets-plugin-extended-metadata/blob/master/beetsplug/emd/audiofilefields.py), that contains your Extended Metadata string.
As default, the *comments* field will be used. Depending on what field you choose some software, including beets, will not be able to handle or persist it.
I recommend using the *comments* field, since most software out there will be able to work with this field and having any other information in this field is usually unnecessary.

## Limitations

The query syntax as well as the *emd* sub-command syntax have some limitations regarding the characters you can use for tag names / tag values.

**Tag Name Limitations:**<br>
A tag name may only contain letters and numbers (including unicode letters) as well as hyphens, underscores and spaces.

**Tag Value Limitations:**<br>
A tag value may contain any character except for commas, also it cannot start with a colon.
This limitation is necessary because colons and commas are special characters that cannot be escaped in any way without breaking the query/command syntax.

## Writing Queries

### Assumptions:
- You configured *x* as the query prefix and *comments* as the input field.
- Your library contains songs with Extended Metadata strings in the *comments* field.
- You imported the songs into your beets library after writing the metadata to the files.

### Examples

**Note**: All queries are case-insensitive.
If you have a value *Abc* it will match the query value *abc*.
If you want to query case-sensitive, use [regex queries](#searching-for-all-rock-variant-songs).

#### Searching for all russian songs

This assumes you have a custom tag *language* containing the language of the song.


````bash
beet list x:language:russian
````

Here you can see how you can reference a custom tag from your Extended Metadata.
You start a query part with your query prefix *x*, followed by a colon.
After that the syntax is the same as with normal beets queries, but it will reference tag names and values from the Extended Metadata instead.

#### Searching for all songs that use synthesizer v

This assumes you have a custom tag *vocal_synth* containing the vocal synthesizer used in the song.

````bash
beet list x:vocal_synth:"syntheszer v"
````

You can query for values containing spaces by enclosing them in parentheses or quotes.
This is just the way a shell works and is not done by this plugin.

#### Searching for all songs that are either japanese or chinese

This assumes you have a custom tag *language* containing the language of the song.

````bash
beet list x:language:japanese,chinese
````

By passing multiple values, separated by commas, you can query files that match one of the provided values

#### Searching for all rock variant songs

This assumes you have a custom tag *genre* containing the genre of the song.

````bash
beet list x:genre::.+rock
````

Here you can see how you can use [regex](https://en.wikipedia.org/wiki/Regular_expression) to make your queries more flexible.
Just like with beets you can specify that your query value is regex by using the double colon *::* instead of a single colon.

#### Searching for all songs in japanese that to not come from japan from the last 3 years

This assumes you have a custom tag *language* containing the language of the song and a custom tag *origin* containing the origin country.

````bash
beet list x:.language:japanese x:.origin:'!japan' year:2010..2020
````

In this example you can see how to easily combine Extended Metadata queries with normal audio field queries.
It also shows how to negate query values. If you prefix the query tag value with ! it will mean *not equals* / *not contains*.

## Managing Extended Metadata

The query capabilities work as long as the Extended Metadata has been written to the files according to the [Extended Metadata documentation](EMD.md).
This means it is not required to use this plugin to write the Extended Metadata to your files.

The plugin provides an *emd* subcommand to write, update and show Extended Metadata based on beets queries.
The sub command requires a beets query that matches the items you want to apply options to, and a list of options that define what you want to do.
To get an overview of all options you can use the *--help* option:

```shell
$ beet emd --help
Usage: beet emd <query> [options]

Options:
  -h, --help            show this help message and exit
  -y, --yes             automatically confirms yes/no prompts that require
                        user input
  -u UPDATE_EXPRESSION, --update=UPDATE_EXPRESSION
                        update or move a tag value. Example: "tag1:v1/tag1:v2"
                        or "tag1:v1/tag2:v1" or "tag1:v1/tag2:v2".
  -r RENAME_EXPRESSION, --rename=RENAME_EXPRESSION
                        rename a tag. Example: "tag1/tag2".
  -a ADD_EXPRESSION, --add=ADD_EXPRESSION
                        add a tag value. Example: "tag1:v1" or
                        "tag1:v1,v2,v3".
  -c COPY_EXPRESSION, --copy=COPY_EXPRESSION
                        copy a tag value from/to extended metadata or normal
                        metadata. Tags prefixed with . refer to tags of normal
                        metadata. Examples: "tag1/tag2", ".artist/tag2",
                        "tag1/.artist", ".artist/.album_artist"
  -d DELETE_EXPRESSION, --delete=DELETE_EXPRESSION
                        delete a tag value or tag. Example: "tag1" or
                        "tag1:v1".
  -s, --show            show the extended meta data of the items
```

The query argument can be passed to the *emd* command in the same way you pass it to the *list* command.
The options are optional, but you have to set at least one option.
All non-flag options are repeatable. By repeating an option you can apply multiple actions of the same type.

### Examples

#### Show Extended Metadata of matching files

```shell
beet emd artist:ギガP album:'No title' -s
```

With the *show* option the Extended Metadata of each matching file will be printed to the screen.
The Extended Metadata will be shown in its json format.
You can also combine this option with any other options,
in which case the shown Extended Metadata represents the resulting Extended Metadata after all other option have been applied.

#### Add tags for a specific artist

```shell
beet emd artist:REOL -a language:japanese -a origin:japan
```

Here you can see how to add new tag values to the Extended Metadata of the file.
You can add multiple tags by repeating the *add* option.

#### Remove a tag from all files

```shell
beet emd '' -d genre
```

You can match all files by simply passing an empty string to the *query* option.
This deletes the *genre* tag from all files, regardless of its value.

#### Remove a tag value for certain audio formats

```shell
beet emd path::*\.flac -d tag:uncompressed
```

Here we do not delete the entire tag but only a certain value of the tag.
You can use a path query to apply the changes to certain directories or, in this case, certain audio formats by using regex.

#### Rename a tag in all files

```shell
beet emd '' -r singer/vocals
```

With the *rename* option you can rename a tag by passing the old- and the new tag name separated by */*.

#### Update a tag value

```shell
beet emd x:origin:germany -u category:good/category:favorite
```

With the *update* option you can change a tag value.
The syntax is the same as with the *rename* option but it also includes a tag value.

#### Move a tag value in all files

```shell
beet emd '' -u tag:metal/genre:metal
```

By defining different tag names ins the old- and new value expression you can move a value from one tag to another.

#### Move and update a tag value in all files

```shell
beet emd '' -u tag:'thrash metal'/genre:metal
```

By defining different tags and values in both the old- and new tag value expression you can move and change a tag value at the same time.

#### Copy a value from normal metadata to extended metadata in all files
```shell
beet emd '' -c .comments/lyrics
```

In a copy expression your can use normal metadata tags as source or destination for a copy operation by prefixing the tag name with a dot.
In this example the value from the normal metadata tag *comments* will be copied to an EMD tag *lyrics*.
When the destination tag does not exist it will be created, if it does exist the value will be appended to existing values.

**Hint:** When adding EMD to a file for the first time you can use this to back up existing tag values from the tag that will be used to store the EMD.

#### Everything combined

```shell
beet emd x:origin:germany,austria x:language:'!german' -a tag:western,lederhosen -a category:good -d circle -u circle:'hyper hyper'/tag:hyper -r category/rating -c .artist:artist -s
```

This adds the values *western* and *lederhosen* to the tag *tag*, 
adds *good* to the tag *category*, 
deletes the tag *circle*, 
moves the value *hyper hyper* from tag *circle* to the tag *tag* and changes it to *hyper*,
renames the tag *origin* to country, copies the value from the normal tag *artist* to the emd tag *artist*
and prints the resulting Extended Metadata to the screen
for all songs from *germany* or *austria* that are *not* *german*.

Here we delete and rename tags that are also referenced in add and update operations.
In general this works, but it is important to be aware of the order in which the options are applied:
1. Update
2. Rename
3. Add
4. Copy
5. Delete
6. Show

So in this example we rename *category* to *rating* before we add the value *good* to the tag *category*.
So we basically add a tag with the old name after renaming it.
This is probably not what we want. In this example we could easily fix this by simply using the new tag name for adding the value.