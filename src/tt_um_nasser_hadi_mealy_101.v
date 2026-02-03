`default_nettype none

module tt_um_nasser_hadi_mealy_101 (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,    // Dedicated outputs
    input  wire [7:0] uio_in,    // IOs: Input path
    output wire [7:0] uio_out,   // IOs: Output path
    output wire [7:0] uio_oe,    // IOs: Enable path (1=output)
    input  wire       ena,       // always 1 when powered
    input  wire       clk,       // clock
    input  wire       rst_n       // active-low reset
);

    // Input mapping
    wire din = ui_in[0];

    // State encoding (iverilog-friendly)
    // S0: idle (no match)
    // S1: saw "1"
    // S2: saw "10"
    localparam [1:0] S0_IDLE = 2'b00;
    localparam [1:0] S1_1    = 2'b01;
    localparam [1:0] S2_10   = 2'b10;

    reg [1:0] state, next_state;

    // Mealy output depends on state AND input
    // Detect "101" when currently in S2_10 and din==1
    wire z = (state == S2_10) && (din == 1'b1);

    // Next-state logic (overlap allowed)
    always @(*) begin
        next_state = state;
        case (state)
            S0_IDLE: next_state = (din) ? S1_1    : S0_IDLE;
            S1_1:    next_state = (din) ? S1_1    : S2_10;
            S2_10:   next_state = (din) ? S1_1    : S0_IDLE; // if din=1, we detected 101 and keep overlap by going to S1
            default: next_state = S0_IDLE;
        endcase
    end

    // State register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= S0_IDLE;
        else
            state <= next_state;
    end

    // Outputs
    assign uo_out[0] = z;

    // Debug: expose state bits (optional)
    assign uo_out[2:1] = state;

    // Debug: expose din for easier waveform reading (Surfer-friendly)
    assign uo_out[3]   = din;     // din debug bit
    assign uo_out[7:4] = 4'b0;    // remaining unused


    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Silence unused warnings
    wire _unused = &{ena, ui_in[7:1], uio_in, 1'b0};

endmodule
