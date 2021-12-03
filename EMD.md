# Extended Metadata

## Disclaimer
This article only describes what Extended Metadata is and how it should be used.
Actually reading or writing Extended Metadata to files is out of scope of this article.

## Introduction

*Extended Metadata* describes a way of storing additional metadata in your audio files without writing them into specific audio tags or using custom audio tags.
The goal of Extended Metadata is to give you a uniform way of storing custom metadata that does not depend on the audio format.

## Structure

The structure of Extended Metadata is quite simple.
It uses [JSON](https://en.wikipedia.org/wiki/JSON) to store key value pairs of data.
The values can either be single values or arrays.
Extended Metadata uses a flat hierarchy, so objects or nested arrays are not supported.

Here is an example of Extended Metadata:

````json
{
  "language": "japanese",
  "origin": "japan",
  "genre": "rock",
  "vocals": ["初音ミク", "巡音ルカ"]
}
````

The keys of the JSON represent the name of the custom tag.
You can store one or multiple values for each custom tag.

## File Storage

Extended Metadata is attached to audio files by using existing, common audio tags.
This means that one audio tag has to be sacrificed. The best choice would be a tag that all audio formats support that you usually don't need.
For example, the *Comment* tag could be used since all audio formats have it and it rarely stores any meaningful information.

The JSON containing the custom tags will not be written directly to this field, instead it will be encoded using [Base64](https://en.wikipedia.org/wiki/Base64) and prefixed with *EMD:*.
So, the example from above would result in the following string:

````
EMD: ewogICJsYW5ndWFnZSI6ICJqYXBhbmVzZSIsCiAgIm9yaWdpbiI6ICJqYXBhbiIsCiAgImdlbnJlIjogInJvY2siLAogICJ2b2NhbHMiOiBbIuWInemfs+ODn+OCryIsICLlt6Hpn7Pjg6vjgqsiXQp9
````

This is how a client that supports writing Extended Metadata must behave.
Clients that read Extended Metadata then need to read the value of the chosen audio tag, check that its prefixed with *EMD:* and then Base64 decode the string to read the Extended Metadata.