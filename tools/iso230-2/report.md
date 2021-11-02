# ecmc motion system test report

* Data file   : /home/pi/sources/ecmc_bifrost_slits_sat/tests_2/11360/axis1/230_2_3.log
* Date        : Tue 02 Nov 2021 11:44:23 AM CET
* Author      : pi


# Gear Ratios
From | To | Ratio [] | Offset [mm] | Data count [] | Residual error [mm²]
--- | --- | --- | --- | --- | --- |
Openloop | Resolver | -.99998 | 67.66363 | 50.00000 |
Openloop | Reference (ILD2300) | .99942 | 8.57125 | 50.00000 | .00084

# ISO 230-2 motion test

## Configuration

### General

Setting | Value
--- | --- |
Input file | sys.stdin
Time | 2021-11-02 11:45:13.579476
User | pi

### Cycle information

Setting | Value
--- | --- |
Position count | 5 (i=1..5)
Cycle count |5 (j=1..5)
Unit | mm
Reference position source | IOC_TEST:m0s005-Enc01-PosAct
Target position source | IOC_TEST:Axis1-PosSet
Test number source | IOC_TEST:TestNumber


## Input data

### Data forward direction

i = Position index []

j = Cycle index []

tgt_pos(i) = Target position at position i [mm]

ref_pos(i,j) = Reference position at position i and cycle j [mm]


i |tgt_pos(i) [mm]|ref_pos(i,1) [mm]|ref_pos(i,2) [mm]|ref_pos(i,3) [mm]|ref_pos(i,4) [mm]|ref_pos(i,5) [mm]|
--- |--- |--- |--- |--- |--- |--- |
1|15.0|15.00067|15.00169|15.0021|15.00393|15.00332|
2|25.0|24.99964|24.99964|24.99862|25.00005|24.99924|
3|35.0|35.00025|34.99291|34.99719|34.99964|34.99536|
4|45.0|44.9978|44.99943|44.9982|44.99881|44.99657|
5|55.0|55.00289|55.00085|55.00717|55.00819|55.00044|

### Data backward direction

i = Position index []

j = Cycle index []

tgt_pos(i) = Target position at position i [mm]

ref_pos(i,j) = Reference position at position i and cycle j [mm]

i |tgt_pos(i) [mm]|ref_pos(i,1) [mm]|ref_pos(i,2) [mm]|ref_pos(i,3) [mm]|ref_pos(i,4) [mm]|ref_pos(i,5) [mm]|
--- |--- |--- |--- |--- |--- |--- |
1|15.0|15.00475|15.00475|15.00495|15.00638|15.00679|
2|25.0|24.9974|24.99842|24.9974|24.99822|24.99862|
3|35.0|34.98965|34.9925|34.99332|34.99413|34.99332|
4|45.0|44.9978|44.99841|44.99881|44.99841|45.00024|
5|55.0|55.00268|55.00289|55.00696|55.00574|55.00289|


## ISO230-2 calculations:

### Positioning deviation and reversal error

#### Positioning deviation forward direction (unidirectional)

x(i,j)   = Position deviation at position i, cycle j (reference position - target position) [mm]

x_avg(i) = Mean unidirectional positioning deviation at a position

i |x(i,1) [mm]|x(i,2) [mm]|x(i,3) [mm]|x(i,4) [mm]|x(i,5) [mm]|x_avg(i)[mm]|
--- |--- |--- |--- |--- |--- |--- |
1|0.00067|0.00169|0.0021|0.00393|0.00332|0.00234|
2|-0.00036|-0.00036|-0.00138|5e-05|-0.00076|-0.00056|
3|0.00025|-0.00709|-0.00281|-0.00036|-0.00464|-0.00293|
4|-0.0022|-0.00057|-0.0018|-0.00119|-0.00343|-0.00184|
5|0.00289|0.00085|0.00717|0.00819|0.00044|0.0039|

#### Positioning deviation backward direction (unidirectional)

x(i,j)   = Position deviation at position i, cycle j (reference position - target position) [mm]

x_avg(i) = Mean unidirectional positioning deviation at a position

i |x(i,1) [mm]|x(i,2) [mm]|x(i,3) [mm]|x(i,4) [mm]|x(i,5) [mm]|x_avg(i)[mm]|
--- |--- |--- |--- |--- |--- |--- |
1|0.00475|0.00475|0.00495|0.00638|0.00679|0.00552|
2|-0.0026|-0.00158|-0.0026|-0.00178|-0.00138|-0.00199|
3|-0.01035|-0.0075|-0.00668|-0.00587|-0.00668|-0.00742|
4|-0.0022|-0.00159|-0.00119|-0.00159|0.00024|-0.00127|
5|0.00268|0.00289|0.00696|0.00574|0.00289|0.00423|

#### Positioning deviation bi-directional

x_avg(i) = Mean bi-directional positioning deviation at a position[mm]

B(i)     = Reversal error at a position [mm]

i |x_avg(i) [mm]|B(i) [mm]|
--- |--- |--- |
1|0.00393|-0.00318|
2|-0.00127|0.00143|
3|-0.00517|0.00449|
4|-0.00155|-0.00057|
5|0.00407|-0.00033|

B = Axis reversal error [mm]

B = 0.00449 [mm]

B_avg = Axis avg. reversal error [mm]

B_avg = 0.00037 [mm]

### Repeatability

S_fwd(i) = Forward estimator for unidirectional axis positiong repeatability at a position [mm]

S_bwd(i) = Backward estimator for unidirectional axis positiong repeatability at a position [mm]

R_fwd(i) = Forward unidirectional positioning repeatability at a position [mm]

R_bwd(i) = Backward unidirectional positioning repeatability at a position [mm]

R(i) = Bi-directional position repeatability at a position [mm]

i |S_fwd(i) [mm]|S_bwd(i) [mm]|R_fwd(i) [mm]|R_bwd(i) [mm]|R(i) [mm]|
--- |--- |--- |--- |--- |--- |
1|0.0013|0.00098|0.0052|0.00393|0.00775|
2|0.00054|0.00058|0.00216|0.00231|0.00366|
3|0.00304|0.00174|0.01216|0.00696|0.01404|
4|0.00108|0.00092|0.00433|0.00367|0.00457|
5|0.00358|0.00199|0.01434|0.00794|0.01434|

R_fwd = Forward unidirectional positioning repeatability of an axis (max(R_fwd(i))) [mm]

R_fwd = 0.01434 [mm]

R_bwd = Backward unidirectional positioning repeatability of an axis (max(R_bwd(i))) [mm]

R_bwd = 0.00794 [mm]

R = Bi-directional positioning repeatability of an axis (max(R_fwd,R_bwd)) [mm]

R = 0.01434 [mm]

### Positioning Error

E_fwd = Forward unidirectional system positioning error of an axis [mm]

E_fwd = 0.00684 [mm]

E_bwd = Backward unidirectional system positioning error of an axis [mm]

E_bwd = 0.01294 [mm]

E = Bi-directional system positioning error of an axis [mm]

E = 0.00845 [mm]

M = Mean bi-directional system positioning error of an axis [mm]

M = 0.00924 [mm]

### Accuracy

A_fwd = Forward unidirectional accuracy of an axis [mm]

A_fwd = 0.02008 [mm]

A_bwd = Backward unidirectional accuracy of an axis [mm]

A_bwd = 0.0191 [mm]

A = Bi-directional accuracy of an axis [mm]

A = 0.02197 [mm] 

# Limit Switch Performance

## Low Limit Engage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | -0.43016 | -0.45864 | -0.02848
2 | -0.43016 | -0.45864 | -0.02848
3 | -0.43391 | -0.45931 | -0.02540
4 | -0.42945 | -0.45844 | -0.02899
5 | -0.42492 | -0.45696 | -0.03203
6 | -0.43539 | -0.45957 | -0.02417
7 | -0.43086 | -0.45880 | -0.02794
8 | -0.43242 | -0.45908 | -0.02666
9 | -0.43398 | -0.45931 | -0.02533
10 | -0.43688 | -0.45983 | -0.02295
AVG | -0.43181 | -0.45886 | 0.02704
STD | 0.00328 | 0.00076 | 0.00251
Range | 0.01195 | 0.00287

## Low Limit Disengage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | -0.31211 | -0.33053 | -0.01842
2 | -0.31141 | -0.32939 | -0.01798
3 | -0.30438 | -0.31896 | -0.01458
4 | -0.30836 | -0.32491 | -0.01655
5 | -0.30758 | -0.32377 | -0.01619
6 | -0.30828 | -0.32476 | -0.01648
7 | -0.30984 | -0.32705 | -0.01721
8 | -0.30984 | -0.32705 | -0.01721
9 | -0.30836 | -0.32481 | -0.01645
10 | -0.30672 | -0.32247 | -0.01575
AVG | -0.30869 | -0.32537 | 0.01668
STD | 0.00214 | 0.00318| -0.00104
Range | 0.00773 | 0.01157

## High Limit Engage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | 67.29305 | 67.28490 | -0.00815
2 | 67.33125 | 67.29710 | -0.03415
3 | 67.32078 | 67.29140 | -0.02938
4 | 67.30875 | 67.28880 | -0.01995
5 | 67.32977 | 67.29610 | -0.03367
6 | 67.36500 | 67.32490 | -0.04010
7 | 67.39203 | 67.35490 | -0.03713
8 | 67.30805 | 67.28870 | -0.01935
9 | 67.32227 | 67.29180 | -0.03047
10 | 67.34937 | 67.31060 | -0.03877
AVG | 67.33200 | 67.30290 | 0.02910
STD | 0.02802 | 0.02075 | 0.00727
Range | 0.09898 | 0.07000

## High Limit Disengage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | 66.63945 | 66.60030 | -0.03915
2 | 66.64172 | 66.60300 | -0.03872
3 | 66.64250 | 66.60400 | -0.03850
4 | 66.64320 | 66.60500 | -0.03820
5 | 66.64406 | 66.60600 | -0.03806
6 | 66.64023 | 66.60120 | -0.03903
7 | 66.64242 | 66.60390 | -0.03852
8 | 66.64633 | 66.60860 | -0.03773
9 | 66.64766 | 66.61040 | -0.03726
10 | 66.64852 | 66.61140 | -0.03712
AVG | 66.64360 | 66.60540 | 0.03820
STD | 0.00288 | 0.00354| -0.00066
Range | 0.00906 | 0.01110


## Resolver Value Distribution

Measured at 8 positions offset by 45deg resolver shaft angle. The distrubution values are based on 10 values at each location.

Test | Setpoint [mm] | Resolver AVG[mm] | Diff [mm} | Resolver STD[mm]
--- | --- | --- | --- | --- |
1 | 36.12562 | 36.0860000 | -0.0396250 | 0.0000107
2 | 36.25062 | 36.2518000 | 0.0011750 | 0.0000118
3 | 36.37562 | 36.3362000 | -0.0394250 | 0.0000130
4 | 36.50062 | 36.5017000 | 0.0010750 | 0.0000184
5 | 36.62562 | 36.5858000 | -0.0398250 | 0.0000129
6 | 36.75062 | 36.7514000 | 0.0007750 | 0.0000127
7 | 36.87562 | 36.8362000 | -0.0394250 | 0.0000139
8 | 37.00062 | 37.0017000 | 0.0010750 | 0.0000168

Accuracy standstill (Resolver): 0.0398250

