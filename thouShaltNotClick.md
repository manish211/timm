# Gudeilines for Writing data mining scripts

## Share and Enjoy

+ Place the scripts in a repo others can comment on, raise issues, contribute to,  fork and make their own.
+ Do unto others as you wish they do unto you. When commenting on other people's code, be kind. One day, it will be your turn to receive comments and then...

## Know Thy Parameters

At the end of each run

+ Print the parameter settings that were in force during that run.
+ Also print out the source of the data (some unique string) and the date.

## Write to Run

+ Demo Scripts

## Write to Test

Seperate training from test set:

+ Leave-one-out for short data sets of, say, less than 100 records);
+ 5-by-5 cross val for others (25 repeats is more than the 20 requierd for the legenadary, dare I say "mythical"
  central limit theorem to apply.
+ Or, of streaming, before updating the models with the new data, test that new data on the old data.  

Expect a crash:

+ Given a long run, things may barph and die. So write the code such that if some test dies half way through,
  it is possible to resume from that point onwards.
  
## Write to Scale

If possible:

+ Eschew batch processing for streaming (better for scalability).
+ Use randomized algorithms (better for distribution over a CPU farm).

## Write to read

To allow for include in 2 column papers, narrow and short functions/classes/comments:

+ Favor high-level scripting languages (e.g. Python) to more verbose ones (e.g. C);
+ 50 chars wide, or less;
+ Functions: 50 lines or less (and much less is much better)
+ Classes: try for 50 lines or less and if that fails, make the metods 50 lines or less.
+ indent = 2 blanks
+ if possible, not _self_ or _this_ but _me_ or _i_.
