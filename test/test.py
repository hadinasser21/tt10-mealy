import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles


def set_din_only(dut, bit):
    dut.ui_in.value = (bit & 1)


def get_z(dut):
    return int(dut.uo_out[0].value)


def get_state_dbg(dut):
    # uo_out[2:1] = state
    s0 = int(dut.uo_out[1].value)
    s1 = int(dut.uo_out[2].value)
    return (s1 << 1) | s0


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start Mealy 101 test (primed)")

    # Start clock
    cocotb.start_soon(Clock(dut.clk, 10, units="us").start())

    # Init
    dut.ena.value = 1
    dut.uio_in.value = 0
    set_din_only(dut, 0)

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1

    # Prime cycle (optional)
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    async def step(bit, label=""):
        # Drive input on falling edge so it is stable before rising edge
        await FallingEdge(dut.clk)
        set_din_only(dut, bit)

        # Mealy output can update immediately after din changes
        z_now = get_z(dut)
        st_now = get_state_dbg(dut)

        # State updates on rising edge; sample again at posedge
        await RisingEdge(dut.clk)
        z_clk = get_z(dut)
        st_clk = get_state_dbg(dut)

        dut._log.info(
            f"{label} din={bit} | immediate: state={st_now:02b} z={z_now} "
            f"| @posedge: state={st_clk:02b} z={z_clk}"
        )

        return z_now, st_now, z_clk, st_clk

    # Stream: 1 0 1 0 1
    bits = [1, 0, 1, 0, 1]

    zs_now = []
    zs_clk = []
    states_clk = []

    for i, b in enumerate(bits, start=1):
        z_now, st_now, z_clk, st_clk = await step(b, f"b{i}")
        zs_now.append(z_now)
        zs_clk.append(z_clk)
        states_clk.append(st_clk)

    # Assertions (use @posedge samples for clean truth-table alignment)
    assert zs_clk[0] == 0
    assert zs_clk[1] == 0
    assert zs_clk[2] == 1
    assert zs_clk[3] == 0
    assert zs_clk[4] == 1
