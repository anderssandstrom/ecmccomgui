# ISO 230-2 motion test


## Data forward direction:

i |tgt_pos(i) [mm]|ref_pos(i,1) [mm]|ref_pos(i,2) [mm]|ref_pos(i,3) [mm]|ref_pos(i,4) [mm]|ref_pos(i,5) [mm]|
--- |--- |--- |--- |--- |--- |--- |
1|15.0|15.00067|15.00169|15.0021|15.00393|15.00332|
2|25.0|24.99964|24.99964|24.99862|25.00005|24.99924|
3|35.0|35.00025|34.99291|34.99719|34.99964|34.99536|
4|45.0|44.9978|44.99943|44.9982|44.99881|44.99657|
5|55.0|55.00289|55.00085|55.00717|55.00819|55.00044|

## Data backward direction:

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

E_bwd = Backward unidirectional system positioning error of an axis[mm]

E_bwd = 0.01294 [mm]

E = Bi-directional system positioning error of an axis [mm]

E = 0.00845 [mm]

M = Mean bi-directional system positioning error of an axis[mm]

M = 0.00924 [mm]

### Accuracy

A_fwd = Forward unidirectional accuracy of an axis [mm]

A_fwd = 0.02008 [mm]

A_bwd = Backward unidirectional accuracy of an axis [mm]

A_bwd = 0.0191 [mm]

A = Bi-directional accuracy of an axis [mm]

A = 0.02197 [mm]

