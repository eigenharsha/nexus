# solution/

Reference `.hdl` files are **not** distributed with this lab.

That is deliberate, and it is the one place in this course where the solution is withheld.
Every chip here has an exact, machine-checkable answer, the file is fifteen lines, and
reading it costs you the entire week's learning in ninety seconds. `make verify` is a
complete grader — you do not need a reference to know whether you are right.

If you are genuinely stuck on one chip after an hour:

1. Draw the truth table. Not in your head — on paper.
2. Write the boolean expression from the truth table.
3. Translate the expression to NAND. `a AND b = NOT(a NAND b)`,
   `a OR b = (NOT a) NAND (NOT b)`, `NOT a = a NAND a`.

Step 2 is where people stop and reach for a solution. It is also where the entire exercise
lives.
