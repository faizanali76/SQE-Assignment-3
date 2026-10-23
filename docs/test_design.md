# Test design notes

## Scope and oracle

The selected application is Validators 0.36.0 at commit `22786cc6e7283a0fa452c179797e447f798db9f0`. We test three modules and four public functions directly, without a wrapper application. Internal helpers and the rest of the library are outside the selected scope. Test inputs were selected for this assignment rather than copied from the upstream suite.

The normal public result is exactly `True` for valid data or a false-valued `ValidationError` object for invalid data. With `r_ve=True`, failure raises `ValidationError`. The tests check the result type, truth value and original function/input metadata. They clear `RAISE_VALIDATION_ERROR` for each case to keep the environment predictable.

## 1. Email module - email()

ECP valid partitions: ordinary mailboxes, plus tags, mixed case and optional host/address forms. Invalid partitions: missing or repeated `@`, missing domain or local part, unquoted spaces and misplaced dots. The `simple_host`, `ipv4_address` and `ipv6_address` options have explicit cases.

BVA targets local-part lengths 63, 64 and 65. The upstream implementation rejects a local part above 64 characters. Cases FA-EM-07 to FA-EM-09 cover the boundary. Domain-length and every RFC option combination are not exhaustive in this suite.

## 2. Length module - length()

For minimum 3 and maximum 5, the valid partition is lengths 3 through 5. The invalid partitions are below 3 and above 5. BVA uses lengths 2, 3, 4, 5 and 6. Equal limits use 2, 3 and 4 around an exact required length of 3.

Additional partitions cover omitted limits, an explicit zero maximum, negative bounds, reversed bounds, whitespace, Unicode and `None`. In the pinned version, `max_val=0` is a real limit: an empty string succeeds and a one-character string fails. Negative bounds become returned `ValidationError` objects through the decorator. The Urdu input has seven Unicode characters; length is not its UTF-8 byte count.

## 3. IP-address module - ipv4() and ipv6()

IPv4 ECP includes ordinary dotted addresses, wrong octet counts, leading zeroes, empty input, network addresses and host addresses. BVA includes octets -1, 0, 254, 255 and 256, plus prefixes -1, 0, 32 and 33.

IPv6 ECP includes compressed, loopback, mapped IPv4 and invalid hexadecimal addresses. BVA includes zero and ffff segment values, an overflowing 10000 segment, seven/eight/nine explicit segments, and prefixes -1, 0, 128 and 129.

Both functions test CIDR disabled, strict prefix requirements, host bits allowed/rejected, empty inputs and raise mode. IPv4 also tests the private-address filter. These tests validate syntax and the library's options; no network requests, DNS checks or address reachability are involved.

## Case counts and traceability

Each function has 20 separately collected cases: ten FA IDs and ten US IDs. This gives 80 cases overall. Email and length each have 20, while the IP module has 40 across its two functions. Each ID links the CSV row, pytest result and Excel row. Member labels are work/review allocations, not proof of authorship or participation.

All 80 cases read inputs from an external CSV, exceeding the required four external-data cases. The Excel register records the call step, JSON input and options, expected outcome, actual outcome and pass/fail result from the measured ordered run.

## Execution groups and order

The module markers are `email`, `length` and `ip`. Other groups are `smoke`, `boundary`, `ecp`, `negative`, `faizan` and `usman`. Markers support intersections with pytest's `-m` expression. Eight smoke cases give one valid and one invalid example for each function.

In serial execution the order is email (1), length (2), IPv4 (3), IPv6 (4), then CSV order within each group. In parallel mode xdist distributes independent tests across two processes. Parallel completion order is not deterministic and is not presented as ordered execution.

## Limitations

The suite samples meaningful partitions; it is not a complete RFC conformance or security audit. Statement coverage is reported only for the three selected modules. Passing results do not prove that all library behaviours are correct. The application contains no selected production class, so the assignment's class-method wording is applied to the selected public functions. If the instructor requires production classes specifically, that interpretation needs checking.
