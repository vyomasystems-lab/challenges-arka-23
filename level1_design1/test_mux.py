# See LICENSE.vyoma for details

import cocotb
from cocotb.triggers import Timer
import random
@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""

    cocotb.log.info('##### CTB: Develop your test here ########')
    dut.inp0.value = 1;
    dut.inp1.value = 2;
    dut.inp2.value = 1;
    dut.inp3.value = 2;
    dut.inp4.value = 1;
    dut.inp5.value = 2;
    dut.inp6.value = 1;
    dut.inp7.value = 2;
    dut.inp8.value = 1;
    dut.inp9.value = 2;
    dut.inp10.value = 1;
    dut.inp11.value = 2;
    dut.inp12.value = 1;
    dut.inp13.value = 2;
    dut.inp14.value = 1;
    dut.inp15.value = 1;
    dut.inp16.value = 1;
    dut.inp17.value = 2;
    dut.inp18.value = 1;
    dut.inp19.value = 2;
    dut.inp20.value = 1;
    dut.inp21.value = 2;
    dut.inp22.value = 1;
    dut.inp23.value = 2;
    dut.inp24.value = 1;
    dut.inp25.value = 2;
    dut.inp26.value = 1;
    dut.inp27.value = 2;
    dut.inp28.value = 1;
    dut.inp29.value = 2;
    dut.inp30.value = 1;   


    for i in range(50):

        sel = random.randint(0, 31)
        dut.sel.value = sel
        
        if sel % 2 == 0:
            val = 1
        else:
            val = 2
        
        await Timer(2, units='ns')
        
        dut._log.info(f'sel={sel:05}  model={val:05} DUT={int(dut.out.value):05}')
        assert dut.out.value == val, "Randomised test failed with: {sel} - select = {out}".format(
            sel=dut.sel.value, out=dut.out.value)

