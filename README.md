Converts [taskwarrior](https://taskwarrior.org) exports to [todo.txt](http://todotxt.com)  format

## Features
* creates todo and (optional) archive files
* keeps project, state, due date, creation date and completion date
* converts L/M/H priorities to (A)/(B)/(C)
* converts tags to contexts
* inlines projects and contexts if possible ("Tell Steve to do the thing", tags:Steve,bullying, project:thing" => "Tell @Steve to do the +thing @bullying")

## Usage
Export your taskwarrior tasks

```task export > export.json```

Then convert them

```python3 convert.py -i export.json -o todo.txt -a done.txt```

## Options

* `-i`, `--input`         => input json file
* `-o`, `--output`        => output location
* `-a`, `--archive`       => archive location, otherwise completed tasks are stored in the same file
* `-s`, `--skipCompleted` => ignore completed tasks
* `-ns`, `--noSort`       => do not sort the results
