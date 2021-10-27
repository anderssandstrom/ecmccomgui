# ecmc motion system test report

* Data file   : /home/dev/sources/ecmc_bifrost_slits_sat/tests_2/11360/230_2_slower_rate.log
* Date        : Wed Oct 27 11:53:22 CEST 2021
* Author      : dev


# Gear Ratios
From | To | Ratio [] | Offset [mm] | Data count [] | Residual error [mm²]
--- | --- | --- | --- | --- | --- |
Openloop | Resolver | -.99998 | 67.66751 | 50.00000 |
Openloop | Reference (ILD2300) | .99958 | 8.44205 | 50.00000 | .00255

# Forward test sequence

j (cycle)| i (pos id)| Tgt_pos [mm] | Motor_pos [mm] | Resolver_pos [mm] | Reference [mm] | Diff ref-tgt, X(i,j) [mm]
--- | --- | --- | --- | --- | --- |--- |
1 | 1 | 15.00000 | 15.00070 | 15.00091 | 15.00729 | .00729 |
1 | 2 | 25.00000 | 25.00078 | 25.00097 | 25.00196 | .00196 |
1 | 3 | 35.00000 | 35.00078 | 35.00102 | 34.98011 | -.01989 |
1 | 4 | 45.00000 | 45.00078 | 45.00098 | 45.00169 | .00169 |
1 | 5 | 55.00000 | 55.00078 | 55.00096 | 55.00656 | .00656 |
2 | 1 | 15.00000 | 15.00070 | 15.00090 | 15.00688 | .00688 |
2 | 2 | 25.00000 | 25.00078 | 25.00090 | 25.00094 | .00094 |
2 | 3 | 35.00000 | 35.00078 | 35.00094 | 34.97970 | -.02030 |
2 | 4 | 45.00000 | 45.00078 | 45.00095 | 45.00271 | .00271 |
2 | 5 | 55.00000 | 55.00078 | 55.00091 | 55.00799 | .00799 |
3 | 1 | 15.00000 | 15.00070 | 15.00097 | 15.00566 | .00566 |
3 | 2 | 25.00000 | 25.00078 | 25.00095 | 25.00114 | .00114 |
3 | 3 | 35.00000 | 35.00078 | 35.00099 | 34.98827 | -.01173 |
3 | 4 | 45.00000 | 45.00078 | 45.00102 | 45.00067 | .00067 |
3 | 5 | 55.00000 | 55.00078 | 55.00098 | 55.00472 | .00472 |
4 | 1 | 15.00000 | 15.00070 | 15.00087 | 15.00484 | .00484 |
4 | 2 | 25.00000 | 25.00078 | 25.00094 | 24.99931 | -.00069 |
4 | 3 | 35.00000 | 35.00078 | 35.00094 | 34.98154 | -.01846 |
4 | 4 | 45.00000 | 45.00078 | 45.00096 | 45.00129 | .00129 |
4 | 5 | 55.00000 | 55.00078 | 55.00096 | 55.00452 | .00452 |
5 | 1 | 15.00000 | 15.00070 | 15.00101 | 15.00504 | .00504 |
5 | 2 | 25.00000 | 25.00078 | 25.00103 | 25.00012 | .00012 |
5 | 3 | 35.00000 | 35.00078 | 35.00100 | 34.98990 | -.01010 |
5 | 4 | 45.00000 | 45.00078 | 45.00105 | 45.00333 | .00333 |
5 | 5 | 55.00000 | 55.00078 | 55.00105 | 55.00167 | .00167 |


# Backward test sequence
j (cycle)| i (pos id)| Tgt_pos(i) [mm] | Motor_pos(i) [mm] | Resolver_pos(i) [mm] | Reference(i) [mm] | Diff ref-tgt, X(i,j) [mm]
--- | --- | --- | --- | --- | --- |--- |
1 | 1 | 15.00000 | 14.99929 | 14.99904 | 15.00504 | .00504 |
1 | 2 | 25.00000 | 24.99929 | 24.99910 | 25.00094 | .00094 |
1 | 3 | 35.00000 | 34.99921 | 34.99899 | 34.98154 | -.01846 |
1 | 4 | 45.00000 | 44.99921 | 44.99898 | 45.00271 | .00271 |
1 | 5 | 55.00000 | 54.99929 | 54.99911 | 55.00248 | .00248 |
2 | 1 | 15.00000 | 14.99929 | 14.99906 | 15.00362 | .00362 |
2 | 2 | 25.00000 | 24.99929 | 24.99915 | 25.00338 | .00338 |
2 | 3 | 35.00000 | 34.99921 | 34.99899 | 34.99255 | -.00745 |
2 | 4 | 45.00000 | 44.99921 | 44.99899 | 45.00353 | .00353 |
2 | 5 | 55.00000 | 54.99929 | 54.99912 | 55.00554 | .00554 |
3 | 1 | 15.00000 | 14.99929 | 14.99898 | 15.00280 | .00280 |
3 | 2 | 25.00000 | 24.99929 | 24.99910 | 25.00502 | .00502 |
3 | 3 | 35.00000 | 34.99921 | 34.99896 | 34.99479 | -.00521 |
3 | 4 | 45.00000 | 44.99921 | 44.99893 | 45.00169 | .00169 |
3 | 5 | 55.00000 | 54.99929 | 54.99905 | 55.00697 | .00697 |
4 | 1 | 15.00000 | 14.99929 | 14.99909 | 15.00301 | .00301 |
4 | 2 | 25.00000 | 24.99929 | 24.99911 | 25.00155 | .00155 |
4 | 3 | 35.00000 | 34.99921 | 34.99897 | 34.99601 | -.00399 |
4 | 4 | 45.00000 | 44.99921 | 44.99896 | 45.00373 | .00373 |
4 | 5 | 55.00000 | 54.99929 | 54.99911 | 55.00268 | .00268 |
5 | 1 | 15.00000 | 14.99929 | 14.99912 | 15.00158 | .00158 |
5 | 2 | 25.00000 | 24.99929 | 24.99916 | 25.00012 | .00012 |
5 | 3 | 35.00000 | 34.99921 | 34.99906 | 34.99173 | -.00827 |
5 | 4 | 45.00000 | 44.99921 | 44.99902 | 45.00088 | .00088 |
5 | 5 | 55.00000 | 54.99929 | 54.99919 | 54.99881 | -.00119 |


# Mean Position Deviation and Reversal Error

X_fwd(i) = Mean unidirectional positioning deviation at a position (fwd dir)

X_bwd(i) = Mean unidirectional positioning deviation at a position (bwd dir)

X_avg(i) = Mean bi-directional positioning deviation at a position

B(i) = Reversal error at a position

i (pos id) | Tgt_pos(i) [mm] | X_fwd(i) [mm] | X_bwd(i) [mm] | X_avg(i) [mm] | B(i) [mm]
--- | --- | --- |--- |--- |--- |
1 | 15.00000 | .00594 | .00321 | .00457 | .00273
2 | 25.00000 | .00069 | .00220 | .00144 | -.00151
3 | 35.00000 | -.01609 | -.00867 | -.01238 | -.00742
4 | 45.00000 | .00193 | .00250 | .00221 | -.00057
5 | 55.00000 | .00509 | .00329 | .00419 | .00180

B = Axis Reversal Error [mm]: .00742

B_avg = Axis Avg. Reversal Error [mm]: -.00099

# Repeatability

S_fwd(i) = Forward estimator for unidirectional axis positiong repeatability at a position.

S_bwd(i) = Backward estimator for unidirectional axis positiong repeatability at a position.

R_fwd(i) = Forward unidirectional positioning repeatability at a position.

R_bwd(i) = Backward unidirectional positioning repeatability at a position.

R(i) = Bi-directional position repeatability at a position.

i (pos id) | Tgt_pos(i) [mm] | S_fwd(i) [mm] | S_bwd(i) [mm] | R_fwd(i) | R_bwd(i) | R(i)
--- | --- | --- |--- |--- |--- |--- |
1| 15.00000 | 0 |0 | 0 | 0 | .00273
2| 25.00000 | .00447 |.00316 | .01788 | .01264 | .01677
3| 35.00000 | .02366 |.01341 | .09464 | .05364 | .08156
4| 45.00000 | .00316 |.00316 | .01264 | .01264 | .01321
5| 55.00000 | 0 |0 | 0 | 0 | .00180

R_fwd = Forward unidirectional positioning repeatability of an axis (max(R_fwd(i)))

R_fwd = .09464

R_bwd = Backward unidirectional positioning repeatability of an axis (max(R_bwd(i)))

R_bwd = .05364

R = Bi-directional positioning repeatability of an axis (max(R_fwd,R_bwd))

R = .09464


# Positioning Error

E_fwd = Forward unidirectional system positioning error of an axis.

E_fwd = .02203

E_bwd = Backward unidirectional system positioning error of an axis.

E_bwd = .01196

E = Bi-directional system positioning error of an axis.

E = .02203

M = Mean bi-directional system positioning error of an axis.

M = .01695


# Accuracy

A_fwd = Forward unidirectional accuracy of an axis.

A_fwd = .09464

A_bwd = Backward unidirectional accuracy of an axis.

A_bwd = .05364

A = Bi-directional accuracy of an axis.

A = .09464

