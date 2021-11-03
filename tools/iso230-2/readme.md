
## Start test sequence example

```bash
bash ecmcTestOneAxisISO230.bash 
```
## Start data logging example

```bash
camonitor -n -g10 IOC_TEST:m0s004-Enc01-PosAct IOC_TEST:m0s005-Enc01-PosAct IOC_TEST:TestNumber IOC_TEST:Axis1-PosAct  IOC_TEST:m0s002-BI01 IOC_TEST:m0s002-BI02 IOC_TEST:Axis1-PosSet | tee 230_2_step_10_test.log
```

## Generate report example

```bash
 bash mainISO230_2.bash data.log report.md
```