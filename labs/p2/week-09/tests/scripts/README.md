# Test scripts

`.tst` and `.cmp` files for the Nand2Tetris hardware simulator go here, one pair per chip.

They come with the [Nand2Tetris software suite](https://www.nand2tetris.org/software) under
`projects/01/`, `projects/02/` and `projects/03/`. Copy the ones for the chips in
`tests/run_hdl.py`'s `CHIPS` table into this directory — they are not redistributed here
because they belong to the course authors and are theirs to license.

```bash
# after downloading and unzipping the suite
export N2T=~/nand2tetris
cp $N2T/projects/0{1,2,3}/**/*.tst tests/scripts/
cp $N2T/projects/0{1,2,3}/**/*.cmp tests/scripts/
export NEXUS_HDL_SIM=$N2T/tools/HardwareSimulator.sh
make verify TRACK=basic
```

The one file that is **not** in the suite is `Add16CLA.tst` for the `hard` track — write it
yourself by copying `Add16.tst` and changing the chip name. Doing that is how you find out
that the carry-lookahead adder has to be a drop-in replacement, which is the point.
