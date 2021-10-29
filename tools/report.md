# ecmc motion system test report

* Data file   : /home/dev/sources/ecmc_bifrost_slits_sat/tests_2/11360/230_2_step_10_2.log
* Date        : Fri Oct 29 09:18:23 CEST 2021
* Author      : dev


# Gear Ratios
From | To | Ratio [] | Offset [mm] | Data count [] | Residual error [mm²]
--- | --- | --- | --- | --- | --- |
Openloop | Resolver | -1.00043 | 67.70241 | 25.00000 | .00464
Openloop | Reference (ILD2300) | 1.00010 | 8.43220 | 25.00000 | .00058

# Forward test sequence

i (pos id)| j (cycle)| Tgt_pos(i,j) [mm] | Motor(i,j) [mm] | Resolver(i,j) [mm] | Reference(i,j) [mm] | x(i,j) (diff ref-tgt), [mm]
--- | --- | --- | --- | --- | --- |--- |
1 | 1 | 15.00000 | 15.00070 | 15.01163 | 15.00109 | .00109 |
2 | 1 | 25.20000 | 25.20062 | 25.20169 | 25.21013 | .01013 |
3 | 1 | 35.40000 | 35.40078 | 35.38449 | 35.40285 | .00285 |
4 | 1 | 45.60000 | 45.60078 | 45.58673 | 45.60781 | .00781 |
5 | 1 | 55.80000 | 55.80078 | 55.81926 | 55.79726 | -.00274 |
1 | 2 | 15.00000 | 15.00070 | 15.01163 | 14.99865 | -.00135 |
2 | 2 | 25.20000 | 25.20062 | 25.20173 | 25.19830 | -.00170 |
3 | 2 | 35.40000 | 35.40078 | 35.38448 | 35.40183 | .00183 |
4 | 2 | 45.60000 | 45.60078 | 45.58672 | 45.60679 | .00679 |
5 | 2 | 55.80000 | 55.80078 | 55.81924 | 55.79706 | -.00294 |
1 | 3 | 15.00000 | 15.00070 | 15.01164 | 14.99824 | -.00176 |
2 | 3 | 25.20000 | 25.20062 | 25.20165 | 25.20238 | .00238 |
3 | 3 | 35.40000 | 35.40078 | 35.38435 | 35.40693 | .00693 |
4 | 3 | 45.60000 | 45.60078 | 45.58662 | 45.60822 | .00822 |
5 | 3 | 55.80000 | 55.80078 | 55.81922 | 55.79624 | -.00376 |
1 | 4 | 15.00000 | 15.00070 | 15.01161 | 14.99763 | -.00237 |
2 | 4 | 25.20000 | 25.20062 | 25.20165 | 25.19565 | -.00435 |
3 | 4 | 35.40000 | 35.40078 | 35.38428 | 35.40612 | .00612 |
4 | 4 | 45.60000 | 45.60078 | 45.58663 | 45.60638 | .00638 |
5 | 4 | 55.80000 | 55.80078 | 55.81922 | 55.79624 | -.00376 |
1 | 5 | 15.00000 | 15.00070 | 15.01164 | 14.99681 | -.00319 |
2 | 5 | 25.20000 | 25.20062 | 25.20170 | 25.19504 | -.00496 |
3 | 5 | 35.40000 | 35.40078 | 35.38446 | 35.40142 | .00142 |
4 | 5 | 45.60000 | 45.60078 | 45.58665 | 45.59332 | -.00668 |
5 | 5 | 55.80000 | 55.80078 | 55.81930 | 55.79584 | -.00416 |


# Backward test sequence
i (pos id)| j (cycle)| Tgt_pos(i,j) [mm] | Motor(i,j) [mm] | Resolver(i,j) [mm] | Reference(i,j) [mm] | x(i,j) (diff ref-tgt), [mm]
--- | --- | --- | --- | --- | --- |--- |
1 | 1 | | | | | |
2 | 1 | | | | | |
3 | 1 | | | | | |
4 | 1 | | | | | |
5 | 1 | | | | | |
1 | 2 | | | | | |
2 | 2 | | | | | |
3 | 2 | | | | | |
4 | 2 | | | | | |
5 | 2 | | | | | |
1 | 3 | | | | | |
2 | 3 | | | | | |
3 | 3 | | | | | |
4 | 3 | | | | | |
5 | 3 | | | | | |
1 | 4 | | | | | |
2 | 4 | | | | | |
3 | 4 | | | | | |
4 | 4 | | | | | |
5 | 4 | | | | | |
1 | 5 | | | | | |
2 | 5 | | | | | |
3 | 5 | | | | | |
4 | 5 | | | | | |
5 | 5 | | | | | |


# Mean Position Deviation and Reversal Error

X_fwd(i) = Mean unidirectional positioning deviation at a position (fwd dir)

X_bwd(i) = Mean unidirectional positioning deviation at a position (bwd dir)

X_avg(i) = Mean bi-directional positioning deviation at a position

B(i) = Reversal error at a position

i (pos id) | Tgt_pos(i) [mm] | X_fwd(i) [mm] | X_bwd(i) [mm] | X_avg(i) [mm] | B(i) [mm]
--- | --- | --- |--- |--- |--- |
1 | | -.00151 | | |
2 | | .00030 | | |
3 | | .00383 | | |
4 | | .00450 | | |
5 | | -.00347 | | |

B = Axis Reversal Error

B = 0 [mm]

B_avg = Axis Avg. Reversal Error.

B_avg = [mm]

# Repeatability

S_fwd(i) = Forward estimator for unidirectional axis positiong repeatability at a position.

S_bwd(i) = Backward estimator for unidirectional axis positiong repeatability at a position.

R_fwd(i) = Forward unidirectional positioning repeatability at a position.

R_bwd(i) = Backward unidirectional positioning repeatability at a position.

R(i) = Bi-directional position repeatability at a position.

i (pos id) | Tgt_pos(i) [mm] | S_fwd(i) [mm] | S_bwd(i) [mm] | R_fwd(i) [mm] | R_bwd(i) [mm] | R(i) [mm]
--- | --- | --- |--- |--- |--- |--- |
1| | 0 | | 0 | |
2| | .00316 | | .01264 | |
3| | .00774 | | .03096 | |
4| | .00836 | | .03344 | |
5| | 0 | | 0 | |

R_fwd = Forward unidirectional positioning repeatability of an axis (max(R_fwd(i)))

R_fwd = .03344 [mm]

R_bwd = Backward unidirectional positioning repeatability of an axis (max(R_bwd(i)))

R_bwd = 0 [mm]

R = Bi-directional positioning repeatability of an axis (max(R_fwd,R_bwd))

R = .03344 [mm]


# Positioning Error

E_fwd = Forward unidirectional system positioning error of an axis.

E_fwd = .00797 [mm]

E_bwd = Backward unidirectional system positioning error of an axis.

E_bwd = [mm]

E = Bi-directional system positioning error of an axis.

E = .00797 [mm]

M = Mean bi-directional system positioning error of an axis.

M = [mm]


# Accuracy

A_fwd = Forward unidirectional accuracy of an axis.

A_fwd = .03344 [mm]

A_bwd = Backward unidirectional accuracy of an axis.

A_bwd = [mm]

A = Bi-directional accuracy of an axis.

A = .03344 [mm]

# Limit Switch Performance

## Low Limit Engage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | -0.44078 | -0.45317 | -0.01239
2 | -0.43398 | -0.45222 | -0.01824
3 | -0.43469 | -0.45230 | -0.01762
4 | -0.42945 | -0.45150 | -0.02205
5 | -0.42945 | -0.45151 | -0.02205
6 | -0.42969 | -0.45153 | -0.02184
7 | -0.43328 | -0.45213 | -0.01885
8 | -0.42945 | -0.45153 | -0.02207
9 | -0.42648 | -0.45097 | -0.02449
10 | -0.43766 | -0.45277 | -0.01512
AVG | -0.43249 | -0.45196 | 0.01947
STD | 0.00418 | 0.00064 | 0.00354
Range | 0.01430 | 0.00220

## Low Limit Disengage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | -0.29297 | -0.30071 | -0.00774
2 | -0.30461 | -0.31753 | -0.01292
3 | -0.30078 | -0.31161 | -0.01082
4 | -0.30766 | -0.32218 | -0.01453
5 | -0.30234 | -0.31399 | -0.01165
6 | -0.30453 | -0.31743 | -0.01290
7 | -0.30219 | -0.31394 | -0.01175
8 | -0.30375 | -0.31640 | -0.01265
9 | -0.30383 | -0.31644 | -0.01261
10 | -0.30523 | -0.31854 | -0.01331
AVG | -0.30279 | -0.31488 | 0.01209
STD | 0.00373 | 0.00546| -0.00173
Range | 0.01469 | 0.02148

## High Limit Engage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | 67.31187 | 67.32726 | 0.01538
2 | 67.31414 | 67.32760 | 0.01346
3 | 67.32391 | 67.32964 | 0.00574
4 | 67.31937 | 67.32847 | 0.00910
5 | 67.36289 | 67.35751 | -0.00538
6 | 67.33742 | 67.33719 | -0.00023
7 | 67.31273 | 67.32740 | 0.01467
8 | 67.32695 | 67.33071 | 0.00375
9 | 67.31117 | 67.32714 | 0.01597
10 | 67.33297 | 67.33414 | 0.00117
AVG | 67.32530 | 67.33270 | -0.00740
STD | 0.01523 | 0.00885 | 0.00638
Range | 0.05172 | 0.03036

## High Limit Disengage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | 66.64938 | 66.64596 | -0.00342
2 | 66.65391 | 66.65165 | -0.00226
3 | 66.65617 | 66.65455 | -0.00162
4 | 66.65242 | 66.64955 | -0.00287
5 | 66.65312 | 66.65057 | -0.00256
6 | 66.65305 | 66.65057 | -0.00248
7 | 66.65312 | 66.65059 | -0.00253
8 | 66.65992 | 66.65967 | -0.00025
9 | 66.65617 | 66.65456 | -0.00162
10 | 66.65539 | 66.65352 | -0.00188
AVG | 66.65430 | 66.65210 | 0.00220
STD | 0.00268 | 0.00350| -0.00082
Range | 0.01055 | 0.01372


## Resolver Value Distribution

Measured at 8 positions offset by 45deg resolver shaft angle. The distrubution values are based on 10 values at each location.

Test | Setpoint [mm] | Resolver AVG[mm] | Diff [mm} | Resolver STD[mm]
--- | --- | --- | --- | --- |
1 | 36.12578 | 36.1064000 | -0.0193812 | 0.0000144
2 | 36.25078 | 36.2722000 | 0.0214188 | 0.0000200
3 | 36.37578 | 36.3566000 | -0.0191813 | 0.0000116
4 | 36.50078 | 36.5220000 | 0.0212187 | 0.0000185
5 | 36.62578 | 36.6063000 | -0.0194812 | 0.0000149
6 | 36.75078 | 36.7720000 | 0.0212187 | 0.0000134
7 | 36.87578 | 36.8567000 | -0.0190813 | 0.0000181
8 | 37.00078 | 37.0225000 | 0.0217187 | 0.0000161

Accuracy standstill (Resolver): 0.0217187

