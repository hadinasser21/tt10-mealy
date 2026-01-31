<!--
This file is used to generate your project datasheet.
Fill in the information below and delete unused sections.
-->

# Mealy Machine Model – 101 Sequence Detector

**Author:** Nasser Hadi  
**Top module:** `tt_um_nasser_hadi_mealy_101`  
**Description:** A Mealy finite state machine that detects the bit sequence `101` on a serial input stream.

---

## How it works

This project implements a **Mealy state machine**, where the output depends on both the **current state** and the **current input**.

The design monitors a serial input bit stream (`din`) and asserts the output (`z`) **immediately** when the sequence `101` is detected. Because this is a Mealy machine, the output can change **within the same clock cycle** as the final input bit.

### State encoding

The FSM uses **three states**:

| State | Meaning            |
|------:|--------------------|
| S0    | Idle / no match    |
| S1    | Detected `1`       |
| S2    | Detected `10`      |

### State transitions and output logic

- **S0**
  - `din = 1` → go to **S1**
  - `din = 0` → stay in **S0**

- **S1**
  - `din = 0` → go to **S2**
  - `din = 1` → stay in **S1**

- **S2**
  - `din = 1` → output `z = 1` (sequence `101` detected), go to **S1**
  - `din = 0` → go to **S0**

The output `z` is asserted **only** when the machine is in **S2** and the input `din` is `1`.

### Clocking and reset

- The FSM updates on the **rising edge of `clk`**
- An **active-low reset (`rst_n`)** forces the FSM back to **S0**
- When reset is asserted, the output `z` is cleared to `0`

---

## How to test

Apply a serial bit stream on `din` and observe `z`.

The output should go high **on the same clock cycle** where the final `1` of the sequence `101` is applied.

### Example sequence test

Input stream:
