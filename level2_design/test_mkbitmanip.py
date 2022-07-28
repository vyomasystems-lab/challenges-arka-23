# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))
    for i in range(2):
        X = random.randint(0, 2)
        for _ in range(5):
            # reset
            dut.RST_N.value <= 0
            yield Timer(10) 
            dut.RST_N.value <= 1

            ######### CTB : Modify the test to expose the bug #############
            # input transaction
            mav_putvalue_src1 = random.randint(0, 15)
            mav_putvalue_src2 = random.randint(0, 15)
            mav_putvalue_src3 = random.randint(0, 15)        
            mav_putvalue_instr = 0x400170B3 + X

            # expected output from the model
            expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

            # driving the input transaction
            dut.mav_putvalue_src1.value = mav_putvalue_src1
            dut.mav_putvalue_src2.value = mav_putvalue_src2
            dut.mav_putvalue_src3.value = mav_putvalue_src3
            dut.EN_mav_putvalue.value = 1
            dut.mav_putvalue_instr.value = mav_putvalue_instr
        
            yield Timer(1) 

            # obtaining the output
            dut_output = dut.mav_putvalue.value

            cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
            cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
            
            # comparison
            if X:
                error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}. Instruction not present, expected output is {hex(expected_mav_putvalue)}'
                assert dut_output == expected_mav_putvalue, error_message
            else:
                error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}. Logic error in ANDN 1 block'
                assert dut_output == expected_mav_putvalue, error_message
