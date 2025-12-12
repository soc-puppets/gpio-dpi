module tb();

localparam N_GPIO = 8;

// -----------------------------------------------------------------------------
// Signal declarations
// -----------------------------------------------------------------------------

wire [N_GPIO-1:0]       gpio_in;
wire [N_GPIO-1:0]       gpio_in_oe;
wire [N_GPIO-1:0]       gpio_out;

wire [N_GPIO-1:0]       gpio_tri;

logic clk;
bit tb_done = 0;
int rtn;

// -----------------------------------------------------------------------------
// Module instances
// -----------------------------------------------------------------------------

gpio_dpi #(.N_GPIO(N_GPIO)) u_gpio_dpi (
  .gpio_out,
  .gpio_in,
  .gpio_in_oe
);

for (genvar i=0; i<N_GPIO; i++) begin
  assign gpio_tri[i] = gpio_in_oe[i] ? gpio_in[i] : 1'bz;
end

assign gpio_out = gpio_tri;

// -----------------------------------------------------------------------------
// DPI
// -----------------------------------------------------------------------------

import "DPI-C" context function int pytb_init();
import "DPI-C" context function int pytb_onclock();
import "DPI-C" context function int pytb_shutdown();

export "DPI-C" function simulator_request_finish;

// -----------------------------------------------------------------------------
// Stimulus (via DPI calls)
// -----------------------------------------------------------------------------

initial begin
  clk = 0;
  forever begin
    #5ns;
    clk = !clk;
  end
end

// Main thread
initial begin
  rtn = pytb_init();
  if (rtn != 1) begin
    $error("pytb_init returned %d", rtn);
    tb_done = 1;
  end

  wait(tb_done);
  rtn = pytb_shutdown();
  repeat(10) @(posedge clk);
  $finish;
end

// Call out to the python on every clock.
// In a "real" simulator the python could call tasks that counsume time, but not
// in v e r ilator.
always @(posedge clk) begin
  if (!tb_done)
    rtn = pytb_onclock();
end

function void simulator_request_finish();
  tb_done = 1;
endfunction

// -----------------------------------------------------------------------------
// Waves
// -----------------------------------------------------------------------------

initial begin
  $dumpfile("sim.fst");
  $dumpvars(0, tb);
end

endmodule
