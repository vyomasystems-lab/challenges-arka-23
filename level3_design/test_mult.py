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
    a = random.randint(0, 1024)
    b = random.randint(0, 255)
    x = []
    y = []
    for i in range(11):  
        ######### CTB : Modify the test to expose the bug #############

        # input transaction       
        # driving the input transaction
        dut.in_Mx.value = a
        dut.in_My.value = b           
        await FallingEdge(dut.CLK) 

        # obtaining the output
        dut_output = dut.Prod.value        
       
        if i >= 1:
            if int(dut.Prod.value) != 0:
                x.append(bin(dut.Prod.value))
                y.append(dut_output)
        if i != 10:        
            cocotb.log.info(f'DUT OUTPUT={dut_output}')
        else:
            cocotb.log.info(f'DUT OUTPUT={dut_output}')
            cocotb.log.info(f'DUT DECIMAL OUTPUT={int(dut_output)}')

    
    # expected output from the model
    expected_value = a*b    
    cocotb.log.info(f'EXPECTED OUTPUT={expected_value}')

    temp1 = bin(a)   
    print("MULTIPLICAND : ", format(a, "b"))
    print("ACCUMULATOR OUTPUT WHEN LOADED WITH MULTIPLICAND FOR THE FIRST INSTANCE: ", y[0])

    if temp1 not in x[0]:
        z = 1
    else:
        z = 0        
        # comparison
    if z == 1:    
        error_message = f'Value mismatch DUT = {int(dut_output)} does not match MODEL = {expected_value}. Accumulator loaded with incorrect value, check Load-In block.'
        assert dut_output == expected_value, error_message
    else:
        error_message = f'Value mismatch DUT = {int(dut_output)} does not match MODEL = {expected_value}. Accumulator loaded with incorrect value, check Load-In block.'
        assert dut_output == expected_value, error_message


