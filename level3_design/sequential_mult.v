module sequential_mult(RESET,in_Mx,in_My,Prod,CLK);

//Multiplier and multiplicand inputs to be stored in Mx and My registers
input [15:0]in_Mx; 
input [8:0]in_My; 
input RESET;
input CLK;			
wire [15:0]Mx; 
wire [8:0]My;

//all control signals
wire load_Mx,load_My,shift_My,clear_Acc,load_Acc,shift_In;	

//intermediate wires
wire [3:0]PrsntState; 
wire [3:0]NextState;
wire [7:0]shiftReg; 
wire [15:0]PP; 
wire [16:0]Acc; 
wire [16:0]Sum; 
wire My_bit, D_out;	

//25 bits final product output
output wire [24:0]Prod;

//Call control table module to initialte all control signals
ControlTable CT(PrsntState,NextState,load_Mx,load_My,shift_My,clear_Acc,load_Acc,shift_In,CLK);
sequencer SEQ(NextState,CLK,RESET,PrsntState);


loadIn INPUT(in_Mx,in_My,load_Mx,load_My,CLK,Mx,My,My_bit,shift_My);
PPGen PPG(Mx,My_bit,PP);
Adder ADD(PP,Acc[16:1],Sum);
Accumulator ACC(Sum,load_Acc,clear_Acc,Acc,D_out,CLK);
 ShiftReg SHIFT_In(shiftReg,shift_In,D_out,CLK,clear_Acc);

assign Prod = {Acc,shiftReg};

endmodule 

module ControlTable(PRSNTSTATE,NEXTSTATE,LOAD_MX,LOAD_MY,SHIFT_MY,CLEAR_ACC,LOAD_ACC,SHIFT_IN,CLK);

input [3:0]PRSNTSTATE;  
input CLK;
output LOAD_MX,LOAD_MY,SHIFT_MY,CLEAR_ACC,LOAD_ACC,SHIFT_IN;
output [3:0] NEXTSTATE;

reg   [9:0]ControlSig;
 
 always @(posedge CLK) 
  begin
   case(PRSNTSTATE)
    4'b0000: ControlSig = 10'b1101000001;
    4'b0001: ControlSig = 10'b0010110010;
    4'b0010: ControlSig = 10'b0010110011;
    4'b0011: ControlSig = 10'b0010110100;
    4'b0100: ControlSig = 10'b0010110101;
    4'b0101: ControlSig = 10'b0010110110;
    4'b0110: ControlSig = 10'b0010110111;
    4'b0111: ControlSig = 10'b0010111000;
    4'b1000: ControlSig = 10'b0010111001;
    4'b1001: ControlSig = 10'b0010111010;
    4'b1010: ControlSig = 10'b0000001010;
    default: ControlSig = 10'b0000000000;
   endcase
  end
 
 assign NEXTSTATE = ControlSig[3:0];
 //assign PRSNTSTATE = ControlSig[3:0];
 assign LOAD_MX = ControlSig[9];
 assign LOAD_MY = ControlSig[8];
 assign SHIFT_MY = ControlSig[7];
 assign CLEAR_ACC = ControlSig[6];
 assign LOAD_ACC = ControlSig[5];
 assign SHIFT_IN = ControlSig[4];

endmodule

module loadIn(IN_MX,IN_MY,LOAD_MX,LOAD_MY,CLK,mx,my,MY_BIT,SFT_MY);

input CLK;
input LOAD_MX,LOAD_MY,SFT_MY;
input wire [15:0]IN_MX; 
input wire [8:0]IN_MY;

output reg [15:0]mx;
output reg [8:0]my;
output MY_BIT;

wire SFT_MY;

always @(posedge CLK) 
  begin
    if (LOAD_MX) 
      begin
        mx <= IN_MX; 
      end
    if (LOAD_MY)
      begin
        my <= IN_MY;
      end
    else 
      if(SFT_MY) 
        begin
          my <= (my>>1);
        end
  end
  assign MY_BIT = my[0];

endmodule

module PPGen(MX,M_BIT,PPOUT);

input [15:0]MX; input M_BIT;
output [15:0]PPOUT;

reg [15:0]PPOUT;

  always @(*)
    begin
      if (M_BIT == 0)
        PPOUT = 0;
      else
        PPOUT = MX;
    end

endmodule

module ShiftReg(SHIFTREG,SFT_IN,D_OUT,CLK,CLR_ACC);

input CLK; 
input SFT_IN, D_OUT,CLR_ACC; 
output reg [7:0]SHIFTREG;

always @(posedge CLK)
  begin
    if (CLR_ACC) 
      begin
        SHIFTREG = 8'd0;
      end
    else 
      if (SFT_IN) 
        begin
          SHIFTREG = {D_OUT,SHIFTREG[7:1]};
        end
  end

endmodule

module Accumulator(IN,LD_ACC,CLR_ACC,ACC,D_OUT,CLK);

input [16:0]IN; 
input LD_ACC, CLR_ACC, CLK;
  
output D_OUT; 
output reg [16:0]ACC; //output reg[7:0]shiftReg;
  
  always @(posedge CLK) 
    begin
      if (CLR_ACC) 
        begin
          ACC <= 17'd0; 
          //shiftReg <= 8'b0;
        end
      else 
        if (LD_ACC) 
          begin
            ACC = IN;
          end
    end
  assign D_OUT = ACC[0];

endmodule

module Adder(IN1,IN2,SUM);

input [15:0]IN1; 
input[15:0]IN2;
output reg [16:0]SUM;
//reg [14:0]w;
//integer i;

always @(*) 
  begin
/*
    for (i= 0; i<=14; i= i+1) 
      begin
        {w[i],Sum[i]} = PP[i] + Acc[i];		//bit by bit behavioural? use for loop
      end
    {Sum[16],Sum[15]} = PP[15]+Acc[15];
*/
    SUM = IN1+IN2;
  end

endmodule

module sequencer(INAddr,CLK,RST,OUTAddr);

input [3:0]INAddr;	//next state from control logic
input CLK,RST;
output reg [3:0]OUTAddr;	//output is present state signal to be fed to control ROM 

always @(negedge CLK) 
  begin
    if (~RST) 
      begin		//RESET is active LOW
        OUTAddr = 4'b0000;
      end
    else
      begin
        OUTAddr = INAddr;
      end
  end

endmodule
