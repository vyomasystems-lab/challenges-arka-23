# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
from cocotb.triggers import RisingEdge, FallingEdge



# Sample Test
@cocotb.test()
async def run_test(dut):

    # clock
    clock = Clock(dut.CLK, 10, units="ns")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.RESET.value = 0
    await FallingEdge(dut.CLK)  
    dut.RESET.value = 1    
    
    for i in range(11):
        

        ######### CTB : Modify the test to expose the bug #############
        # input transaction
        a = 253
        b = 254

        # expected output from the model
        expected_value = a*b
        # driving the input transaction
        dut.in_Mx.value = a
        dut.in_My.value = b

           
        await FallingEdge(dut.CLK) 

        # obtaining the output
        dut_output = dut.Prod.value

        cocotb.log.info(f'DUT OUTPUT={dut_output}')
        cocotb.log.info(f'EXPECTED OUTPUT={expected_value}')
        
        # comparison
        error_message = f'Value mismatch DUT = {dut_output} does not match MODEL = {expected_value}'
    assert dut_output == expected_value, error_message

