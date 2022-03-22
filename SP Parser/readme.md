
# SP Data Parser

## How to Format a Template File

Each template file must follow a certain order.  
Here is an example of a simple template:

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
    1:
        vals: 2
        val1: 2000
        val2: 8000
        limit: 20
        column: [13]
        limitType: Min
        dBc: use
```

## Filter

You first start off with a filter number.  

```yaml
filter: 57000
```

## Labels

Next is the labels section. You can input as many labels as you'd like. There is a catch though,
the number of labels ***NEEDS*** to be the same total number of tests/limits. labels are seperated by a comma inbetween them. It also needs to be within brackets [  ].

```yaml
labels: [Insertion Loss, Rejection 1]
```

## Limits

Limits are the tests you want to run on the SP data. There are example templates at the bottom of the document to showcase the differnt types.  
Just as it was mentioned in the Labels section, labels and limits are connected. The number of labels and the number of limits must be the same. If either are off the data will be skewed and will not show accurate results.  
***The tests must start with the number 0 and not 1.***
This section has the most variables, but all of them are required for the test to work.  
Here is a helpful list of all the variables you can set.

- **vals**: The number of values used in the limit. Can be either 1 or 2.  
- **val1 and val2**: Depeneding on the vals section either val1 can be used solely or val1 and val2 are both used.  
- **limit**: The limit for the test.  
- **column**: The exact coulmns needed to search. Refer to the chart at the bottom of the page to see what columns to use. They also need to be in brackets [  ].  
- **limitType**: What limit type to use for the test ["Min, Max, 1dB, Slope, FCROSS"] are all tests that can be used.  
-- **Max**: Gets the lowest number (Mostly used for finding insertion loss).  
-- **Min**: Gets the highest number (Mostly used for finding rejections).  
-- **1dB**: Gets the freq where the insertion loss is 1 less than the middle freq insertion loss.  
-- **Slope**: Gets the differece of the highest and lowest within a range of frequences.  
-- **FCROSS**: Gets the freq where 
- **dBc**: To decern if dBc is used at all in the test. You can use ["template, use, no"].  
-- **template** sets the dBc for all other tests that use it. You can set another template later down the line in tests with another template.  
-- **use** is simple, it uses the last stored template and must come after a template setting.  
-- **no** is no. dBc is not used at all for that particular test.  

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

# Template Test Examples

## Max

```yaml
0:
    vals: 2
    val1: 2000
    val2: 6000
    limit: 1
    column: [13]
    limitType: Max
    dBc: template
```

## Min

```yaml
0:
    vals: 2
    val1: 9200
    val2: 14100
    limit: 20
    column: [13]
    limitType: Min
    dBc: use
```

## 1dB

```yaml
0:
    vals: 1
    val1: 10000
    limit: 100
    column: [3, 5]
    limitType: 1dB
    dBc: no
```

## Slope

```yaml
0:
    vals: 2
    val1: 2000
    val2: 6000
    limit: 1
    column: [13] 
    limitType: Slope
    dBc: no
```

## FCROSS

```yaml
0:
    vals: 2
    val1: 0
    val2: 1
    limit: 0
    column: [7]
    limitType: FCROSS
    dBc: no
```
