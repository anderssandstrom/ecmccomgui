# ecmc motion system test report

* Data file   : /home/dev/sources/ecmc_bifrost_slits_sat/tests_2/11360/axis2/230_2_step_10_only230.log
* Date        : Fri Oct 29 14:57:55 CEST 2021
* Author      : dev


# Gear Ratios
From | To | Ratio [] | Offset [mm] | Data count [] | Residual error [mm²]
--- | --- | --- | --- | --- | --- |
Openloop | Resolver | -.99998 | 34.94281 | 50.00000 |
Openloop | Reference (ILD2300) | .99828 | 11.09071 | 50.00000 | .02187

# Forward test sequence

i (pos id)| j (cycle)| Tgt_pos(i,j) [mm] | Motor(i,j) [mm] | Resolver(i,j) [mm] | Reference(i,j) [mm] | x(i,j) (diff ref-tgt), [mm]
--- | --- | --- | --- | --- | --- |--- |
1 | 1 | 15.00000 | 15.00070 | 15.00120 | 15.00161 | .00161 |
2 | 1 | 25.00000 | 25.00078 | 25.00135 | 25.02160 | .02160 |
3 | 1 | 35.00000 | 35.00078 | 35.00136 | 34.99089 | -.00911 |
4 | 1 | 45.00000 | 45.00078 | 45.00129 | 44.96872 | -.03128 |
5 | 1 | 55.00000 | 55.00078 | 55.00134 | 55.02660 | .02660 |
1 | 2 | 15.00000 | 15.00070 | 15.00114 | 15.00161 | .00161 |
2 | 2 | 25.00000 | 25.00078 | 25.00124 | 25.02160 | .02160 |
3 | 2 | 35.00000 | 35.00078 | 35.00135 | 34.98946 | -.01054 |
4 | 2 | 45.00000 | 45.00078 | 45.00128 | 44.96811 | -.03189 |
5 | 2 | 55.00000 | 55.00078 | 55.00120 | 55.02619 | .02619 |
1 | 3 | 15.00000 | 15.00070 | 15.00116 | 15.00141 | .00141 |
2 | 3 | 25.00000 | 25.00078 | 25.00127 | 25.02120 | .02120 |
3 | 3 | 35.00000 | 35.00078 | 35.00128 | 34.99007 | -.00993 |
4 | 3 | 45.00000 | 45.00078 | 45.00134 | 44.96791 | -.03209 |
5 | 3 | 55.00000 | 55.00078 | 55.00122 | 55.02476 | .02476 |
1 | 4 | 15.00000 | 15.00070 | 15.00117 | 15.00181 | .00181 |
2 | 4 | 25.00000 | 25.00078 | 25.00127 | 25.02120 | .02120 |
3 | 4 | 35.00000 | 35.00078 | 35.00131 | 34.98987 | -.01013 |
4 | 4 | 45.00000 | 45.00078 | 45.00134 | 44.96771 | -.03229 |
5 | 4 | 55.00000 | 55.00078 | 55.00124 | 55.02558 | .02558 |
1 | 5 | 15.00000 | 15.00070 | 15.00125 | 15.00202 | .00202 |
2 | 5 | 25.00000 | 25.00078 | 25.00135 | 25.02099 | .02099 |
3 | 5 | 35.00000 | 35.00078 | 35.00141 | 34.98967 | -.01033 |
4 | 5 | 45.00000 | 45.00078 | 45.00138 | 44.96811 | -.03189 |
5 | 5 | 55.00000 | 55.00078 | 55.00137 | 55.02558 | .02558 |


# Backward test sequence
i (pos id)| j (cycle)| Tgt_pos(i,j) [mm] | Motor(i,j) [mm] | Resolver(i,j) [mm] | Reference(i,j) [mm] | x(i,j) (diff ref-tgt), [mm]
--- | --- | --- | --- | --- | --- |--- |
1 | 1 | 15.00000 | 14.99929 | 14.99871 | 14.99876 | -.00124 |
2 | 1 | 25.00000 | 24.99929 | 24.99878 | 25.01468 | .01468 |
3 | 1 | 35.00000 | 34.99921 | 34.99859 | 34.98743 | -.01257 |
4 | 1 | 45.00000 | 44.99921 | 44.99860 | 44.96689 | -.03311 |
5 | 1 | 55.00000 | 54.99929 | 54.99874 | 55.02598 | .02598 |
1 | 2 | 15.00000 | 14.99929 | 14.99877 | 14.99896 | -.00104 |
2 | 2 | 25.00000 | 24.99929 | 24.99879 | 25.01529 | .01529 |
3 | 2 | 35.00000 | 34.99921 | 34.99859 | 34.98681 | -.01319 |
4 | 2 | 45.00000 | 44.99921 | 44.99865 | 44.96628 | -.03372 |
5 | 2 | 55.00000 | 54.99929 | 54.99878 | 55.02558 | .02558 |
1 | 3 | 15.00000 | 14.99929 | 14.99877 | 14.99937 | -.00063 |
2 | 3 | 25.00000 | 24.99929 | 24.99886 | 25.01488 | .01488 |
3 | 3 | 35.00000 | 34.99921 | 34.99863 | 34.98661 | -.01339 |
4 | 3 | 45.00000 | 44.99921 | 44.99863 | 44.96669 | -.03331 |
5 | 3 | 55.00000 | 54.99929 | 54.99883 | 55.02578 | .02578 |
1 | 4 | 15.00000 | 14.99929 | 14.99882 | 14.99917 | -.00083 |
2 | 4 | 25.00000 | 24.99929 | 24.99886 | 25.01448 | .01448 |
3 | 4 | 35.00000 | 34.99921 | 34.99866 | 34.98783 | -.01217 |
4 | 4 | 45.00000 | 44.99921 | 44.99865 | 44.96689 | -.03311 |
5 | 4 | 55.00000 | 54.99929 | 54.99885 | 55.02537 | .02537 |
1 | 5 | 15.00000 | 14.99929 | 14.99882 | 14.99896 | -.00104 |
2 | 5 | 25.00000 | 24.99929 | 24.99887 | 25.01468 | .01468 |
3 | 5 | 35.00000 | 34.99921 | 34.99863 | 34.98804 | -.01196 |
4 | 5 | 45.00000 | 44.99921 | 44.99869 | 44.96567 | -.03433 |
5 | 5 | 55.00000 | 54.99929 | 54.99884 | 55.02517 | .02517 |


# Mean Position Deviation and Reversal Error

X_fwd(i) = Mean unidirectional positioning deviation at a position (fwd dir)

X_bwd(i) = Mean unidirectional positioning deviation at a position (bwd dir)

X_avg(i) = Mean bi-directional positioning deviation at a position

B(i) = Reversal error at a position

i (pos id) | Tgt_pos(i) [mm] | X_fwd(i) [mm] | X_bwd(i) [mm] | X_avg(i) [mm] | B(i) [mm]
--- | --- | --- |--- |--- |--- |
1 | 15.00000 | .02735 | -.00095 | .01320 | .02830
2 | 25.00000 | .02036 | .01480 | .01758 | .00556
3 | 35.00000 | .00479 | -.01265 | -.00393 | .01744
4 | 45.00000 | -.04454 | -.03351 | -.03902 | -.01103
5 | 55.00000 | -.00777 | .02557 | .00890 | -.03334

B = Axis Reversal Error

B = .03334 [mm]

B_avg = Axis Avg. Reversal Error.

B_avg = .00138 [mm]

# Repeatability

S_fwd(i) = Forward estimator for unidirectional axis positiong repeatability at a position.

S_bwd(i) = Backward estimator for unidirectional axis positiong repeatability at a position.

R_fwd(i) = Forward unidirectional positioning repeatability at a position.

R_bwd(i) = Backward unidirectional positioning repeatability at a position.

R(i) = Bi-directional position repeatability at a position.

i (pos id) | Tgt_pos(i) [mm] | S_fwd(i) [mm] | S_bwd(i) [mm] | R_fwd(i) [mm] | R_bwd(i) [mm] | R(i) [mm]
--- | --- | --- |--- |--- |--- |--- |
1| 15.00000 | 0 |.02949 | 0 | .11796 | .08728
2| 25.00000 | .00547 |.01183 | .02188 | .04732 | .04016
3| 35.00000 | .02323 |.04266 | .09292 | .17064 | .14922
4| 45.00000 | .07854 |.06603 | .31416 | .26412 | .30017
5| 55.00000 | .03741 |0 | .14964 | 0 | .10816

R_fwd = Forward unidirectional positioning repeatability of an axis (max(R_fwd(i)))

R_fwd = .31416 [mm]

R_bwd = Backward unidirectional positioning repeatability of an axis (max(R_bwd(i)))

R_bwd = .26412 [mm]

R = Bi-directional positioning repeatability of an axis (max(R_fwd,R_bwd))

R = .31416 [mm]


# Positioning Error

E_fwd = Forward unidirectional system positioning error of an axis.

E_fwd = .07189 [mm]

E_bwd = Backward unidirectional system positioning error of an axis.

E_bwd = .05908 [mm]

E = Bi-directional system positioning error of an axis.

E = .07189 [mm]

M = Mean bi-directional system positioning error of an axis.

M = .05660 [mm]


# Accuracy

A_fwd = Forward unidirectional accuracy of an axis.

A_fwd = .31416 [mm]

A_bwd = Backward unidirectional accuracy of an axis.

A_bwd = .26412 [mm]

A = Bi-directional accuracy of an axis.

A = .31416 [mm]

# Limit Switch Performance

## Low Limit Engage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | 34.94281 | 0.00000 | 0.00000
2 | 34.94281 | 0.00000 | 0.00000
3 | 34.94281 | 0.00000 | 0.00000
4 | 34.94281 | 0.00000 | 0.00000
5 | 34.94281 | 0.00000 | 0.00000
6 | 34.94281 | 0.00000 | 0.00000
7 | 34.94281 | 0.00000 | 0.00000
8 | 34.94281 | 0.00000 | 0.00000
9 | 34.94281 | 0.00000 | 0.00000
10 | 34.94281 | 0.00000 | 0.00000
AVG | 34.94280 | -34.94280 | 0.00000
STD | 0.00000 | -0.00000 | 0.00000
Range | -20000.00000 | 0.00000

## Low Limit Disengage Position

Test | Openloop [mm]| Resolver [mm]| Diff [mm]
--- | --- | --- |--- |
1 | 34.94281 | 0.00000 | 0.00000
2 | 34.94281 | 0.00000 | 0.00000
3 | 34.94281 | 0.00000 | 0.00000
4 | 34.94281 | 0.00000 | 0.00000
