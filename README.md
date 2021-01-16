# Simple Tournament Schedule Tool
This is a simple tournament schedule tool and you can use it to generate the race schedule easily.  The algorithm that this tool uses is circle method.

You can use this tool as the following way,

`python main.py [--loop_num] [--home_away] [--input] [--output_mode] [--output]`

The function of these arguments can be seen by inputting `python main.py --help` 

By default, you can edit the "team_list.txt" to add the name of team which you will make the schedule, one line includes one team, like the following example.

```
Arsenal  
Aston Villa
Brighton
Burnley
```

And when not adding any other arguments, the generated schedule (schedule.csv) will be stored in the directory of this repository. Certainly, you can store it on any paths you like when setting the output_path parameter.  

