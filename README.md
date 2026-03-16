# fishk

fishy task manager for the command line.

```
~o>><>
```

## install

```
pip install resolution_week1_YOUR_USERNAME
```

## usage

```
fishk "buy worms"               # add a task
fishk -l                        # list your catch
fishk -c 1                      # reel it in (complete)
fishk -r 1                      # throw it back (incomplete)
fishk -d 1                      # swallow into the depths (delete)
fishk -e 1 "updated text"       # re-bait a task (edit)
fishk "task" -p high            # set priority: low / medium / high
fishk "task" --due 2025-06-01   # set a due date
fishk --version                 # print version
```

## task display

```
><> (med) 1: buy worms
[x] (!!) 2: catch a fish  -- due: 2025-06-01
```

`><>` = incomplete, `[x]` = done.  
priorities: `(low)`, `(med)`, `(!!)`.

# guys i love fish
