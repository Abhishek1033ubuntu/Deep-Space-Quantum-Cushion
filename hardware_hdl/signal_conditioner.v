// =============================================================================
// MODULE: signal_conditioner.v
// DESCRIPTION: Real-time hardware detrending filter for atomic telemetry.
//              Uses a parallel shift register moving average to eliminate drift.
// =============================================================================

module ds_quantum_signal_conditioner (
    input  wire        clk,           // Master Flight Clock (50 MHz)
    input  wire        rst_n,         // Active-Low Hardware Reset
    input  wire [15:0] adc_data_in,   // 16-bit Parallel Data from APD Digitizer
    input  wire        adc_valid,     // Data Valid Strobe from ADC
    output reg  [15:0] clean_data_out,// Post-Processed Quantum Signal
    output reg         data_valid_out // Output Data Valid Flag
);

    // Parametric internal window size for moving average (8-stage shift pipe)
    localparam WINDOW_SIZE = 8;
    
    reg [15:0] shift_reg [0:WINDOW_SIZE-1];
    reg [19:0] sum_accumulator;
    wire [15:0] moving_average;
    integer i;

    // Calculate moving average baseline trend via bit-shifting (Divide by 8)
    assign moving_average = sum_accumulator[18:3];

    // Your always block orchestrates the actual hardware logic sequence:
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // 1. ASYNCHRONOUS RESET: Clear all hardware gates to a known safe state
            sum_accumulator <= 20'h0;
            clean_data_out  <= 16'h0;
            data_valid_out  <= 1'b0;
            for (i = 0; i < WINDOW_SIZE; i = i + 1) begin
                shift_reg[i] <= 16'h0;
            end
        end else begin
            if (adc_valid) begin
                // 2. REGISTER PIPELINE: Subtract oldest data leaving, add new data entering
                sum_accumulator <= sum_accumulator - shift_reg[WINDOW_SIZE-1] + adc_data_in;
                
                // Shift data down the internal array tracking pipe
                shift_reg[0] <= adc_data_in;
                for (i = 1; i < WINDOW_SIZE; i = i + 1) begin
                    shift_reg[i] <= shift_reg[i-1];
                end
                
                // 3. CORE FILTER STEP: Subtract the trend line from raw input data
                // This strips out low-frequency thermal/laser drift in real time.
                clean_data_out  <= adc_data_in - moving_average;
                data_valid_out  <= 1'b1;
            end else begin
                data_valid_out  <= 1'b0;
            end
        end
    end

endmodule
