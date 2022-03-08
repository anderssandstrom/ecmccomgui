# ecmc motion system test report

* Data file   : /home/vagrant/sources/ecmc_bifrost_slits_sat/tests_2/11358/axis1/data.log
* Date        : Wed Nov  3 21:10:53 CET 2021
* Author      : vagrant


# Gear Ratios
From | To | Ratio [] | Offset [mm] | Data count [] | Residual error [mm²]
--- | --- | --- | --- | --- | --- |
Target Position | Resolver | -.99980 | -.41372 | 50.00000 | .01002488
Target Position | Reference | .99870 | 11.35544 | 50.00000 | .00139949

# ISO 230-2 motion test

## Configuration

Setting | Value
--- | --- |
Data file | sys.stdin
Reference position source | IOC_TEST:m0s005-Enc01-PosAct
Target position source | IOC_TEST:Axis1-PosSet
Test number source | IOC_TEST:TestNumber
Position count | 5 (i=1..5)
Cycle count |5 (j=1..5)
Unit | mm


## Input data

### Data forward direction

i = Position index []

j = Cycle index []

tgt_pos(i) = Target position at position i [mm]

ref_pos(i,j) = Reference position at position i and cycle j [mm]


i |tgt_pos(i) [mm]|ref_pos(i,1) [mm]|ref_pos(i,2) [mm]|ref_pos(i,3) [mm]|ref_pos(i,4) [mm]|ref_pos(i,5) [mm]|
--- |--- |--- |--- |--- |--- |--- |
1|15.0|15.00335|15.00233|15.00172|15.00213|15.00172|
2|25.2|25.19974|25.20015|25.20096|25.20056|25.20056|
3|35.4|35.40102|35.3996|35.40225|35.40306|35.40449|
4|45.6|45.59151|45.5909|45.59212|45.5909|45.58947|
5|55.8|55.80583|55.80624|55.80685|55.80562|55.80562|

### Data backward direction

i = Position index []

j = Cycle index []

tgt_pos(i) = Target position at position i [mm]

ref_pos(i,j) = Reference position at position i and cycle j [mm]

i |tgt_pos(i) [mm]|ref_pos(i,1) [mm]|ref_pos(i,2) [mm]|ref_pos(i,3) [mm]|ref_pos(i,4) [mm]|ref_pos(i,5) [mm]|
--- |--- |--- |--- |--- |--- |--- |
1|15.0|15.00518|15.00518|15.00416|15.00335|15.00314|
2|25.2|25.19628|25.19607|25.19567|25.19587|25.19526|
3|35.4|35.39817|35.39837|35.3998|35.39939|35.4|
4|45.6|45.59232|45.59191|45.59293|45.59191|45.59151|
5|55.8|55.80705|55.80725|55.80705|55.80705|55.80644|


## ISO230-2 calculations:

### Positioning deviation and reversal error

#### Positioning deviation forward direction (unidirectional)

x(i,j)   = Position deviation at position i, cycle j (reference position - target position) [mm]

x_avg(i) = Mean unidirectional positioning deviation at a position [mm]

i |x(i,1) [mm]|x(i,2) [mm]|x(i,3) [mm]|x(i,4) [mm]|x(i,5) [mm]|x_avg(i) [mm]|
--- |--- |--- |--- |--- |--- |--- |
1|0.00335|0.00233|0.00172|0.00213|0.00172|0.00225|
2|-0.00026|0.00015|0.00096|0.00056|0.00056|0.00039|
3|0.00102|-0.0004|0.00225|0.00306|0.00449|0.00208|
4|-0.00849|-0.0091|-0.00788|-0.0091|-0.01053|-0.00902|
5|0.00583|0.00624|0.00685|0.00562|0.00562|0.00603|

#### Positioning deviation backward direction (unidirectional)

x(i,j)   = Position deviation at position i, cycle j (reference position - target position) [mm]

x_avg(i) = Mean unidirectional positioning deviation at a position [mm]

i |x(i,1) [mm]|x(i,2) [mm]|x(i,3) [mm]|x(i,4) [mm]|x(i,5) [mm]|x_avg(i) [mm]|
--- |--- |--- |--- |--- |--- |--- |
1|0.00518|0.00518|0.00416|0.00335|0.00314|0.0042|
2|-0.00372|-0.00393|-0.00433|-0.00413|-0.00474|-0.00417|
3|-0.00183|-0.00163|-0.0002|-0.00061|0.0|-0.00085|
4|-0.00768|-0.00809|-0.00707|-0.00809|-0.00849|-0.00788|
5|0.00705|0.00725|0.00705|0.00705|0.00644|0.00697|

#### Positioning deviation bi-directional

x_avg(i) = Mean bi-directional positioning deviation at a position [mm]

B(i)     = Reversal error at a position [mm]

i |x_avg(i) [mm]|B(i) [mm]|
--- |--- |--- |
1|0.00323|-0.00196|
2|-0.00189|0.00456|
3|0.00062|0.00293|
4|-0.00845|-0.00114|
5|0.0065|-0.00094|

B = Axis reversal error [mm]

B = 0.00456 [mm]

B_avg = Axis avg. reversal error [mm]

B_avg = 0.00069 [mm]

### Repeatability

S_fwd(i) = Forward estimator for unidirectional axis positiong repeatability at a position [mm]

S_bwd(i) = Backward estimator for unidirectional axis positiong repeatability at a position [mm]

R_fwd(i) = Forward unidirectional positioning repeatability at a position [mm]

R_bwd(i) = Backward unidirectional positioning repeatability at a position [mm]

R(i) = Bi-directional position repeatability at a position [mm]

i |S_fwd(i) [mm]|S_bwd(i) [mm]|R_fwd(i) [mm]|R_bwd(i) [mm]|R(i) [mm]|
--- |--- |--- |--- |--- |--- |
1|0.00067|0.00097|0.00268|0.00388|0.00524|
2|0.00046|0.00039|0.00186|0.00157|0.00628|
3|0.00188|0.00083|0.0075|0.00333|0.00835|
4|0.00098|0.00054|0.00393|0.00216|0.00419|
5|0.00052|0.00031|0.00208|0.00124|0.00259|

R_fwd = Forward unidirectional positioning repeatability of an axis (max(R_fwd(i))) [mm]

R_fwd = 0.0075 [mm]

R_bwd = Backward unidirectional positioning repeatability of an axis (max(R_bwd(i))) [mm]

R_bwd = 0.00388 [mm]

R = Bi-directional positioning repeatability of an axis (max(R_fwd,R_bwd)) [mm]

R = 0.0075 [mm]

### Positioning Error

E_fwd = Forward unidirectional system positioning error of an axis [mm]

E_fwd = 0.01505 [mm]

E_bwd = Backward unidirectional system positioning error of an axis [mm]

E_bwd = 0.01485 [mm]

E = Bi-directional system positioning error of an axis [mm]

E = 0.01485 [mm]

M = Mean bi-directional system positioning error of an axis [mm]

M = 0.01495 [mm]

### Accuracy

A_fwd = Forward unidirectional accuracy of an axis [mm]

A_fwd = 0.01806 [mm]

A_bwd = Backward unidirectional accuracy of an axis [mm]

A_bwd = 0.01655 [mm]

A = Bi-directional accuracy of an axis [mm]

A = 0.01858 [mm] 

# Limit Switch Performance

## Configuration

Setting | Value |
--- | --- |
Data file | /home/vagrant/sources/ecmc_bifrost_slits_sat/tests_2/11358/axis1/data.log |
Reference position source | IOC_TEST:m0s004-Enc01-PosAct |
Reference gear ratio | -0.9998085624 |
Reference offset | -0.4137274628 |
Low Limit source | IOC_TEST:m0s002-BI01 |
High Limit source | IOC_TEST:m0s002-BI02 |
Test number source | IOC_TEST:TestNumber |
Unit | mm |

## Low Limit

Test | Engage [mm] | Disengage [mm] |
--- | --- | --- |
1 | -0.39861 | -0.01605 |
2 | -0.37186 | -0.01664 |
3 | -0.39201 | -0.01916 |
4 | -0.36995 | -0.02128 |
5 | -0.35549 | -0.02128 |
6 | -0.34295 | -0.02439 |
7 | -0.33603 | -0.02381 |
8 | -0.33299 | -0.02496 |
9 | -0.32678 | -0.02437 |
10 | -0.31750 | -0.29179 |
AVG   | -0.35442 | -0.04837 |
STD   | 0.02640 | 0.00000 |
Range | 0.08111 | 0.27574 |

Low limit engage range    = 0.08111 
Low limit disengage range = 0.27574 

Test | Engage [mm] | Disengage [mm] |
--- | --- | --- |
1 | 66.74026 | 65.51832 |
2 | 66.74283 | 65.52016 |
3 | 66.72932 | 65.52647 |
4 | 66.71826 | 65.52438 |
5 | 66.73428 | 65.53559 |
6 | 66.70614 | 65.53146 |
7 | 66.70467 | 65.53677 |
8 | 66.69933 | 65.54314 |
9 | 66.69838 | 65.54106 |
10 | 66.69793 | 65.54720 |
AVG   | 33.18140 | 65.53250 |
STD   | 33.53579 | 0.00000 |
Range | 0.04490 | 0.02888 |

High limit engage range    = 0.04490 
High limit disengage range = 0.02888 


# Resolver Performance

## Configuration

Setting | Value |
--- | --- |
Data file | /home/vagrant/sources/ecmc_bifrost_slits_sat/tests_2/11358/axis1/data.log |
Resolver position source | IOC_TEST:m0s004-Enc01-PosAct |
Resolver gain | -0.9998085624 |
Resolver offset | -0.4137274628 |
Target position source | IOC_TEST:Axis1-PosSet |
Test number source | IOC_TEST:TestNumber |
Unit | mm |

## Resolver reading over one turn
Measured at 8 positions offset by 45deg resolver shaft angle.
The distrubution values are based on 10 values at each location.

Test | Setpoint [mm] | Resolver AVG[mm] | Diff [mm] | Resolver STD[mm]
--- | --- | --- | --- | --- |
1 | 36.12570 | 36.1442000 | 0.0184969 | 0.0000148
2 | 36.25070 | 36.2319000 | -0.0188031 | 0.0000152
3 | 36.37570 | 36.3941000 | 0.0183969 | 0.0000136
4 | 36.50070 | 36.4813000 | -0.0194031 | 0.0000147
5 | 36.62570 | 36.6440000 | 0.0182969 | 0.0000189
6 | 36.75070 | 36.7316000 | -0.0191031 | 0.0000098
7 | 36.87570 | 36.8943000 | 0.0185969 | 0.0000149
8 | 37.00070 | 36.9813000 | -0.0194031 | 0.0000137

Resolver standstill error: 0.0194031 [mm]

