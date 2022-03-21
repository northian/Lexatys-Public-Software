
# SP Data Parser

## How to Format a Template File

Each template file must follow a certain order.  
Here is an example:

```yaml
filter: 57000
labels: [Insertion Loss]
limits:
    0:
        vals: 2
        val1: 2000
        val2: 6000
        limit: 1
        column: [3, 5]
        limitType: Max
        dBc: template
```

## Filter

You first start off with a filter number.  

```yaml
filter: 57000
```

## Labels

Next is the labels section. This one is scaling and can be as many as you'd like. There is a catch though
with the fact that the number of labels ***NEEDS*** to be the same total number of tests/limits. To seperate the labels
you need to have a comma inbetween them. It needs to be within brackets [''].

```yaml
labels: [Insertion Loss, Rejection 1]
```

## Limits

This is the part that has the most variations. Limits are the tests you want to run on the SP data.  
Just like the labels the number of tests you want to run must match the same amount of labels you put before. If either are off the data will be skewed and will not show accurate results.  
***The tests must start with the number 0 and not 1.***
The number of tests you want to run are scaling. Here is a helpful definition for all of the variables you can set.
> **vals**: The number of values used in the limit. Can be either 1 or 2
> **val1 and val2**: Depeneding on the vals section either val1 can be used solely or val1 and val2 are both used
> **limit**: The limit for the test
> **column**: The exact coulmns needed to search. Refer to the chart at the bottom of the page to see what columns to use
> **limitType**: What limit type to use for the test "Min, Max, 1dB, Slope, FCROSS" are all tests that can be used
> **dBc**: To decern if dBc is used at all in the test. You can use "template, use, no".
Template sets the dBc for all other tests that use it. You can set another template later down the line in tests with another template.
Use is simple, it uses the last stored template and must come after a template setting.
No is no. dBc is not used at all for that particular test.

```yaml
limits:
    0:
        vals: 2
        val1: 2000
        val2: 6000
        limit: 1
        column: [3, 5]
        limitType: Max
        dBc: template
```

## Columns

This section will cover the columns used in the limits. The formatting should work for all touchstone formatted files.

- s1p: 0 = Sxx, 1 = Sxx
- s2p: 1 = S11, 3 = S21, 5 = S12, 7 = S22
- s3p: 1 = S11, 3 = S12, 5 = S13, 7 = S21, 9 = S22, 11 = S23, 13 = S31, 15 = S32, 17 = S33
- s4p: 1 = S11, 3 = S12, 5 = S13, 7 = S14, 9 = S21, 11 = S22, 13 = S23, 15 = S24, 17 = S31, 19 = S32, 21 = S33, 23 = S33, 25 = S34, 27 = S41, 29 = S42, 31 = S43, 33 = S44
