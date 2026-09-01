"""Acceptance tests for LAB-P2-W10 — Multi-threaded TCP chat server (raw sockets).

Every test here is one line of an acceptance criterion from the track SPECs, and carries the
track marker it belongs to. Tracks are cumulative: `make verify TRACK=hard` runs all three.

`make verify` puts the implementation directory (starter/ or solution/) first on `sys.path`,
so these tests import by module name and never care which one they are grading.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------- basic
@pytest.mark.basic
def test_basic_echo_server_accepting_client_echoing_lines_back() -> None:
    """
    An echo server accepting one client, echoing lines back, and shutting down cleanly on
    Ctrl-C.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")

@pytest.mark.basic
def test_basic_matching_client() -> None:
    """
    A matching client.
    """
    pytest.fail("not implemented yet — see basic/SPEC.md")


# ---------------------------------------------------------------- standard
@pytest.mark.standard
def test_standard_multi_room_chat_over_raw_socket_framework() -> None:
    """
    Multi-room chat over raw `socket` (no framework): join, leave, list, broadcast, direct
    message.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_length_prefixed_framing_4_byte_big_endian() -> None:
    """
    **Length-prefixed framing** (4-byte big-endian length + payload). The test harness
    deliberately splits messages across TCP segments and coalesces others; your parser must
    not care.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_concurrent_clients_threads_selectors_slow_client_block() -> None:
    """
    Concurrent clients via threads or `selectors`; a slow client must not block the others.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_nicknames_collision_handling_join_leave_notices_room() -> None:
    """
    Nicknames with collision handling; join/leave notices to the room.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_graceful_disconnect_handling_including_half_open_case() -> None:
    """
    Graceful disconnect handling, including the half-open case (client killed with no FIN)
    detected by a heartbeat.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_protocol_md_message_types_wire_format_state() -> None:
    """
    `PROTOCOL.md` — message types, wire format, state machine, error codes.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")

@pytest.mark.standard
def test_standard_tshark_capture_committed_showing_message_split_across() -> None:
    """
    A `tshark` capture committed, showing a message split across two segments and
    reassembled.
    """
    pytest.fail("not implemented yet — see standard/SPEC.md")


# ---------------------------------------------------------------- hard
@pytest.mark.hard
def test_hard_1_000_concurrent_connections_sustained_report_memory() -> None:
    """
    1,000 concurrent connections sustained; report memory per connection and p99 message
    latency.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_back_pressure_client_stops_reading_grow_server() -> None:
    """
    Back-pressure: a client that stops reading must not grow the server's memory without
    bound — the server drops or disconnects it according to a documented policy.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_heartbeats_documented_timeout_detecting_half_open_case() -> None:
    """
    Heartbeats with a documented timeout, detecting the half-open case within it.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

@pytest.mark.hard
def test_hard_survives_tc_netem_loss_5_linux_message() -> None:
    """
    Survives `tc netem loss 5%` (Linux) with no message loss at the application layer.
    """
    pytest.fail("not implemented yet — see hard/SPEC.md")

