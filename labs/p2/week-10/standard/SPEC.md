# `standard` — LAB-P2-W10

**For:** you ship code for a living, or you have finished `basic`. You get a spec and a test
suite. You write the implementation from an empty file.

**Time box:** 6-7 h

## Acceptance criteria

- Multi-room chat over raw `socket` (no framework): join, leave, list, broadcast, direct message.
- **Length-prefixed framing** (4-byte big-endian length + payload). The test harness deliberately
  splits messages across TCP segments and coalesces others; your parser must not care.
- Concurrent clients via threads or `selectors`; a slow client must not block the others.
- Nicknames with collision handling; join/leave notices to the room.
- Graceful disconnect handling, including the half-open case (client killed with no FIN) detected
  by a heartbeat.
- `PROTOCOL.md` — message types, wire format, state machine, error codes.
- A `tshark` capture committed, showing a message split across two segments and reassembled.

## Acceptance

```bash
make verify TRACK=standard
```

## Design notes

`recv()` returning fewer bytes than you asked for is not an error, and it is the bug in almost
every hand-written socket server. Write `recv_exactly(n)` first, test it against a fixture that
returns one byte at a time, and build everything on top of it.

## What the tests will not tell you

The tests check behaviour. They do not check whether your code is worth reviewing. Before you
call this done, read your own diff as if someone else wrote it.
