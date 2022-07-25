# Challenges-arka-23
Challenges-arka-23 created by GitHub Classroom
# MUX Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.


![image](https://user-images.githubusercontent.com/70422874/180702143-4cb9c527-dfc5-4a92-a0e4-ea92bc2d5c5a.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (MUX module here) which takes in 5-bit input *sel* and 31 2-bit inputs *inp* and gives 2-bit output *out*

The values are assigned to the input port using 
```
     for i in range(2):
        bit = random.randint(0,1)
        dut.inp_bit.value = bit  
        await FallingEdge(dut.clk)
        
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1   
```
![image](https://user-images.githubusercontent.com/70422874/180702258-0cc62be4-44c0-4bba-8946-211711a2d0c7.png)


The assert statement is used for comparing the MUX's outut to the expected value.

The following error is seen:
```
 AssertionError: Randomised test failed with: sequence - [1, 0, 1, 0, 1, 1]
 ```
 ![image](https://user-images.githubusercontent.com/70422874/180702488-8a9d4b73-537e-4f82-b300-aa490003d755.png)
 
## Test Scenario **(Important)**
- Test Inputs: inp_bit sequence = 101011
- Expected Output: A = 1
- Observed Output in the DUT dut.seq_seen.value = 0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
 line 40 : 5'b01101: out = inp12;
 line 41 : 5'b01101: out = inp13;
```
For the MUX design, line 40 :  5'b01100: out = inp12, instead of  5'b01101: out = inp12; as in the design code.

The following error is seen:
```
 AssertionError: Randomised test failed with: sequence - [0, 1, 1, 0, 1, 1]
```
![image](https://user-images.githubusercontent.com/70422874/180702786-257eec88-8dfc-4511-bd9f-bbbfc1e0f4c9.png)

## Test Scenario **(Important)**
- Test Inputs: inp_bit sequence = 011011
- Expected Output: A = 1
- Observed Output in the DUT dut.seq_seen.value = 0

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
Input not available. Possible error after line no. 57
```
For the MUX design, line 57:  5'b11110: out = inp30, before default: out = 0; as in the design code.



## Design Fix
Updating the design and re-running the test makes the test pass.

![image](https://user-images.githubusercontent.com/70422874/180037501-54e5b02e-0159-4aa2-8aba-880d75ea50b0.png)


## Verification Strategy

## Is the verification complete ?
