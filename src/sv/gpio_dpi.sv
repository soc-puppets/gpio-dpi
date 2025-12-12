/*
 * gpio_dpi
 * Testbench module for driving / monitoring a set of GPIO pins.
 * Controlled by the exported DPI functions.
 */

module gpio_dpi #(
  parameter int N_GPIO  = 4     // 1 .. 32
) (
  input  wire  [N_GPIO-1:0]     gpio_out,       // out from the DUT, in to this agent. Names are hard, alright?
  output logic [N_GPIO-1:0]     gpio_in,
  output logic [N_GPIO-1:0]     gpio_in_oe
);

initial begin
  gpio_in = 'x;
  gpio_in_oe = '0;
end

export "DPI-C" function gpio_get_out;
export "DPI-C" function gpio_get_in;
export "DPI-C" function gpio_get_in_oe;

export "DPI-C" function gpio_set_in;
export "DPI-C" function gpio_set_in_oe;

function int unsigned gpio_get_out();
  return gpio_out;
endfunction

function int unsigned gpio_get_in();
  return gpio_in;
endfunction

function int unsigned gpio_get_in_oe();
  return gpio_in_oe;
endfunction

function void gpio_set_in(int unsigned value);
  gpio_in = value;
endfunction

function void gpio_set_in_oe(int unsigned value);
  gpio_in_oe = value;
endfunction

endmodule
