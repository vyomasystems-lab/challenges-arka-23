# Challenges-arka-23
Challenges-arka-23 created by GitHub Classroom
# MUX Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.


![image](https://user-images.githubusercontent.com/70422874/180022741-804d1df6-d9d3-4574-81ac-769b454e18dc.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (MUX module here) which takes in 5-bit input *sel* and 31 2-bit inputs *inp* and gives 2-bit output *out*

The values are assigned to the input port using 
```
    dut.inp0.value = 1
    dut.inp1.value = 2
    dut.inp2.value = 1
    dut.inp3.value = 2
    dut.inp4.value = 1
    dut.inp5.value = 2
    dut.inp6.value = 1
    dut.inp7.value = 2
    dut.inp8.value = 1
    dut.inp9.value = 2
    dut.inp10.value = 1
    dut.inp11.value = 2
    dut.inp12.value = 1
    dut.inp13.value = 2
    dut.inp14.value = 1
    dut.inp15.value = 2
    dut.inp16.value = 1
    dut.inp17.value = 2
    dut.inp18.value = 1
    dut.inp19.value = 2
    dut.inp20.value = 1
    dut.inp21.value = 2
    dut.inp22.value = 1
    dut.inp23.value = 2
    dut.inp24.value = 1
    dut.inp25.value = 2
    dut.inp26.value = 1
    dut.inp27.value = 2
    dut.inp28.value = 1
    dut.inp29.value = 2
    dut.inp30.value = 1 

    dut.sel.value = sel
```

The assert statement is used for comparing the MUX's outut to the expected value.

The following error is seen:
```
AssertionError: Randomised test failed with: select line - 01101 corresponding to two different input lines. Possible error in line no. 40
```
## Test Scenario **(Important)**
- Test Inputs: sel = 01101
- Expected Output: out = 2
- Observed Output in the DUT dut.out = 1

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
 always @(a or b) 
  begin
    sum = a - b;             ====> BUG
  end
```
For the adder design, the logic should be ``a + b`` instead of ``a - b`` as in the design code.

## Design Fix
Updating the design and re-running the test makes the test pass.

![](https://i.imgur.com/5XbL1ZH.png)

The updated design is checked in as adder_fix.v

## Verification Strategy

## Is the verification complete ?
