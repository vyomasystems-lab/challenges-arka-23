# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0


import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0    
    #await FallingEdge(dut.clk)

    cocotb.log.info('#### CTB: Develop your test here! ######')
    x = [1,0,1,1]
    for i in range(2):
        bit = random.randint(0,1)
        dut.inp_bit.value = bit  
        A = 0
        x.insert(i, bit)
        await FallingEdge(dut.clk)   
        dut._log.info(f'bit={bit:01}  model={A:01} DUT={int(dut.seq_seen.value):01}')          

    #await FallingEdge(dut.clk)
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 0
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1
    await FallingEdge(dut.clk)
    dut.inp_bit.value = 1     
    
        
    #await FallingEdge(dut.clk)
    A = 1
        #await Timer(2, units='ns')        
    await FallingEdge(dut.clk)    
    dut._log.info(f'bit={1:01}  model={A:01} DUT={int(dut.seq_seen.value):01}')

    assert dut.seq_seen.value == A, "Randomised test failed with: sequence - {x} ".format(x = x)
        
        
