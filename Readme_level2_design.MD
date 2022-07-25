# Challenges-arka-23
Challenges-arka-23 created by GitHub Classroom
# Bitmanipulation Coprocessor Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/70422874/180822711-e2e6a748-2a70-4796-b0f3-eadaa179a8f1.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (Sequence Detector module here) which takes in 1-bit inputs *inp_bit* as a sequence synchronized to a clock, a 1-bit *reset* and gives 1-bit output *seq_seen*

The values are assigned to the input port using 
```
      for i in range(2):
        # reset
        dut.RST_N.value <= 0
        yield Timer(10) 
        dut.RST_N.value <= 1

        ######### CTB : Modify the test to expose the bug #############
        # input transaction
        mav_putvalue_src1 = i
        mav_putvalue_src2 = i + 1
        mav_putvalue_src3 = 0x0
        mav_putvalue_instr = 0x610150B3

        # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

        # driving the input transaction
        dut.mav_putvalue_src1.value = mav_putvalue_src1
        dut.mav_putvalue_src2.value = mav_putvalue_src2
        dut.mav_putvalue_src3.value = mav_putvalue_src3
        dut.EN_mav_putvalue.value = 1
        dut.mav_putvalue_instr.value = mav_putvalue_instr
```
![image](https://user-images.githubusercontent.com/70422874/180823145-7092481d-7673-41ab-8a23-abbb9c3acd8f.png)


The assert statement is used for comparing the MUX's outut to the expected value.

## The following error is seen:
```
 AssertionError: Value mismatch DUT = 0x2 does not match MODEL = 0x0. Instruction not present, expected output is 0x0
 ```
![image](https://user-images.githubusercontent.com/70422874/180706148-a7f4a163-e191-4496-ab6b-4658d6147896.png)
 
## Test Scenario **(Important)**
- mav_putvalue_src1 = i
- mav_putvalue_src2 = i + 1
- mav_putvalue_src3 = 0x0
- mav_putvalue_instr = 0x110150B3
- Expected Output: expected_mav_putvalue = 0x0
- Observed Output in the DUT dut_output = 0x2

Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, we see the following

```
Instruction not present, expected output is 0x0
```

## Design Fix
Updating the design and re-running the test makes the test pass.


## Verification Strategy

## Is the verification complete ?
