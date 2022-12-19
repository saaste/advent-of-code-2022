# Advent of Code 2022

## How to run

Normal:
```
python day_00.py
```

Test:
```
python day_00.py --test
```

With test input:
```
python day_00.py --test-input
```

Initialize a new day:
```
./new_day.sh
```

# Challenging days

## Day 11
I had no idea how to optimize the second step. After I learned the prime trick from Reddit, things moved forward quite quickly. I didn't want to copy other people's code so I just learned the principle and then did my own implementation.

## Day 12
I managed to get the answer pretty easily, but I couldn't optimize this to be lightning fast. It takes few seconds to run the second step but that is good enough for me. There is probably a trick to skip most of the checks but I just couldn't figure it out and I didn't want to spend the whole day on this.

## Day 16
This was an absolute failure from me. I couldn't figure out even the first part. I didn't check solutions of other people, but I did read some explanations and tips for possible solutions. Clearly, this required algorithm knowledge I simply didn't have. I'll try this later after I've learned the required stuff.

## Day 17
This, too, was challenging. However, I managed to figure out the first part. I tried different kinds of solutions for the second part and all of them worked with the test input but not with my input. I think I'm off by just a little, but couldn't figure out where the problem is.

## Day 19
Similar to day 16. I didn't have a clue how to solve this, but I found out that some people managed to get the right answer
by running a simulation millions of times. Turns out, this gives a right answers pretty consistently for the first part. The performance is poor but I found the solution to be kinda funny :D

For the second  part, it took reeeeeaaally long time to find the right answer and I gave few wrong ones before getting the the star. But now that I got the max geoside count for each blueprint, I could "optimize" the code and check each blueprint as long as we'll have the right answer. Can take a while, but it will give the right answer eventually :D
