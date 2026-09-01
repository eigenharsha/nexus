# starter/

Your `.hdl` files go here. Eight of them are stubbed with the right interface; the rest of
the chips in `tests/run_hdl.py`'s `CHIPS` table you create yourself.

Every chip must be built from `Nand` and from chips you have already built. That constraint
is the lab: by the time you have `ALU`, you will have built it out of about 500 NAND gates
and you will be able to say which 500.

Order matters — build them in this order and each one uses the last:

```
Not And Or Xor  ->  Mux DMux  ->  Not16 And16 Or16 Mux16  ->  Or8Way
Mux4Way16 Mux8Way16 DMux4Way DMux8Way                      (basic)
HalfAdder FullAdder Add16 Inc16  ->  ALU                   (basic -> standard)
Bit Register RAM8 RAM64 RAM512 RAM4K RAM16K PC             (standard)
Add16CLA                                                   (hard)
```

Before you write a line of the ALU, fill in its truth table by hand for the six control
bits `zx nx zy ny f no`. If you can derive `x-y` from the bits without looking it up, the
HDL takes twenty minutes.
