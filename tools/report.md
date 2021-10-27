# ecmc motion system test report

* Data file   : /home/dev/sources/ecmc_bifrost_slits_sat/tests_2/11360/230_2_slower_rate.log
* Date        : Wed Oct 27 10:04:10 CEST 2021
* Author      : dev


# Gear Ratios
From | To | Ratio [] | Offset [mm] | Data count [] | Residual error [mm²]
--- | --- | --- | --- | --- | --- |
Openloop | Resolver | -.99997 | 67.68714 | 2460.00000 | .56455
Openloop | Reference (ILD2300) | 1.00004 | 8.43081 | 2396.00000 | .42606

# Forward test sequence

j (cycle)| i (pos id)| Tgt_pos [mm] | Motor_pos [mm] | Resolver_pos [mm] | Reference [mm] | Diff ref-tgt, X(i,j) [mm]
--- | --- | --- | --- | --- | --- |--- |
1 | 1 | 15.00000 | 15.00070 | 15.02085 | 14.99906 | -.00094 |
1 | 2 | 25.00000 | 25.00078 | 25.02085 | 24.99832 | -.00168 |
1 | 3 | 35.00000 | 35.00078 | 35.02084 | 34.98106 | -.01894 |
1 | 4 | 45.00000 | 45.00078 | 45.02075 | 45.00725 | .00725 |
1 | 5 | 55.00000 | 55.00078 | 55.02067 | 55.01670 | .01670 |
2 | 1 | 15.00000 | 15.00070 | 15.02084 | 14.99866 | -.00134 |
2 | 2 | 25.00000 | 25.00078 | 25.02079 | 24.99730 | -.00270 |
2 | 3 | 35.00000 | 35.00078 | 35.02077 | 34.98065 | -.01935 |
2 | 4 | 45.00000 | 45.00078 | 45.02072 | 45.00827 | .00827 |
2 | 5 | 55.00000 | 55.00078 | 55.02062 | 55.01813 | .01813 |
3 | 1 | 15.00000 | 15.00070 | 15.02091 | 14.99743 | -.00257 |
3 | 2 | 25.00000 | 25.00078 | 25.02083 | 24.99751 | -.00249 |
3 | 3 | 35.00000 | 35.00078 | 35.02081 | 34.98922 | -.01078 |
3 | 4 | 45.00000 | 45.00078 | 45.02079 | 45.00623 | .00623 |
3 | 5 | 55.00000 | 55.00078 | 55.02069 | 55.01487 | .01487 |
4 | 1 | 15.00000 | 15.00070 | 15.02081 | 14.99662 | -.00338 |
4 | 2 | 25.00000 | 25.00078 | 25.02083 | 24.99567 | -.00433 |
4 | 3 | 35.00000 | 35.00078 | 35.02077 | 34.98249 | -.01751 |
4 | 4 | 45.00000 | 45.00078 | 45.02073 | 45.00684 | .00684 |
4 | 5 | 55.00000 | 55.00078 | 55.02067 | 55.01466 | .01466 |
5 | 1 | 15.00000 | 15.00070 | 15.02095 | 14.99682 | -.00318 |
5 | 2 | 25.00000 | 25.00078 | 25.02092 | 24.99649 | -.00351 |
5 | 3 | 35.00000 | 35.00078 | 35.02083 | 34.99085 | -.00915 |
5 | 4 | 45.00000 | 45.00078 | 45.02081 | 45.00888 | .00888 |
5 | 5 | 55.00000 | 55.00078 | 55.02076 | 55.01181 | .01181 |


# Backward test sequence
j (cycle)| i (pos id)| Tgt_pos(i) [mm] | Motor_pos(i) [mm] | Resolver_pos(i) [mm] | Reference(i) [mm] | Diff ref-tgt, X(i,j) [mm]
--- | --- | --- | --- | --- | --- |--- |
1 | 1 | 15.00000 | 14.99929 | 15.01899 | 14.99682 | -.00318 |
1 | 2 | 25.00000 | 24.99929 | 25.01898 | 24.99730 | -.00270 |
1 | 3 | 35.00000 | 34.99921 | 35.01882 | 34.98249 | -.01751 |
1 | 4 | 45.00000 | 44.99921 | 45.01875 | 45.00827 | .00827 |
1 | 5 | 55.00000 | 54.99929 | 55.01881 | 55.01262 | .01262 |
2 | 1 | 15.00000 | 14.99929 | 15.01900 | 14.99539 | -.00461 |
2 | 2 | 25.00000 | 24.99929 | 25.01904 | 24.99975 | -.00025 |
2 | 3 | 35.00000 | 34.99921 | 35.01882 | 34.99350 | -.00650 |
2 | 4 | 45.00000 | 44.99921 | 45.01876 | 45.00908 | .00908 |
2 | 5 | 55.00000 | 54.99929 | 55.01883 | 55.01568 | .01568 |
3 | 1 | 15.00000 | 14.99929 | 15.01892 | 14.99458 | -.00542 |
3 | 2 | 25.00000 | 24.99929 | 25.01898 | 25.00138 | .00138 |
3 | 3 | 35.00000 | 34.99921 | 35.01879 | 34.99575 | -.00425 |
3 | 4 | 45.00000 | 44.99921 | 45.01870 | 45.00725 | .00725 |
3 | 5 | 55.00000 | 54.99929 | 55.01876 | 55.01711 | .01711 |
4 | 1 | 15.00000 | 14.99929 | 15.01904 | 14.99478 | -.00522 |
4 | 2 | 25.00000 | 24.99929 | 25.01899 | 24.99791 | -.00209 |
4 | 3 | 35.00000 | 34.99921 | 35.01880 | 34.99697 | -.00303 |
4 | 4 | 45.00000 | 44.99921 | 45.01872 | 45.00929 | .00929 |
4 | 5 | 55.00000 | 54.99929 | 55.01882 | 55.01283 | .01283 |
5 | 1 | 15.00000 | 14.99929 | 15.01906 | 14.99335 | -.00665 |
5 | 2 | 25.00000 | 24.99929 | 25.01904 | 24.99649 | -.00351 |
5 | 3 | 35.00000 | 34.99921 | 35.01888 | 34.99269 | -.00731 |
5 | 4 | 45.00000 | 44.99921 | 45.01879 | 45.00643 | .00643 |
5 | 5 | 55.00000 | 54.99929 | 55.01890 | 55.00895 | .00895 |


# Mean Position Deviation and Reversal Error

X_fwd(i) = Mean unidirectional positioning deviation at a position (fwd dir)

X_bwd(i) = Mean unidirectional positioning deviation at a position (bwd dir)

X_avg(i) = Mean bi-directional positioning deviation at a position

B(i) = Reversal error at a position

i (pos id) | Tgt_pos(i) [mm] | X_fwd(i) [mm] | X_bwd(i) [mm] | X_avg(i) [mm] | B(i) [mm]
--- | --- | --- |--- |--- |--- |
1 | 15.00000 | -.00228 | -.00501 | -.00364 | .00273
2 | 25.00000 | -.00294 | -.00143 | -.00218 | -.00151
3 | 35.00000 | -.01514 | -.00772 | -.01143 | -.00742
4 | 45.00000 | .00749 | .00806 | .00777 | -.00057
5 | 55.00000 | .01523 | .01343 | .01433 | .00180

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
1| 15.00000 | .01949 |.02073 | .07796 | .08292 | .08317
2| 25.00000 | .02024 |.01673 | .08096 | .06692 | .07545
3| 35.00000 | .03391 |.02366 | .13564 | .09464 | .12256
4| 45.00000 | .00894 |.00632 | .03576 | .02528 | .03109
5| 55.00000 | 0 |0 | 0 | 0 | .00180

R_fwd = Forward unidirectional positioning repeatability of an axis (max(R_fwd(i)))

R_fwd = .13564

R_bwd = Backward unidirectional positioning repeatability of an axis (max(R_bwd(i)))

R_bwd = .09464

R = Bi-directional positioning repeatability of an axis (max(R_fwd,R_bwd))

R = .13564


E_fwd = Forward unidirectional system positioning error of an axis.

E_fwd = .03037

E_bwd = Backward unidirectional system positioning error of an axis.

E_bwd = .02115
E = Bi-directional system positioning error of an axis.
E = .03037

