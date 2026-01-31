<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This design is a Mealy FSM pattern detector for `101`.

- Input `din` is sampled each clock.
- The FSM tracks partial matches (`1`, then `10`).
- When the sequence `101` is completed, `z` goes high immediately (same cycle as the last `1`).
- Overlap is allowed (e.g., `10101` triggers twice).


## How to test

Explain how to use your project

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
