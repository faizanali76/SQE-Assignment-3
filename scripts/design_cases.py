"""Write the hand-selected test inputs to the external CSV resource."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cases = []


def add(function, value, options, expected, technique, purpose):
    index = sum(c['function'] == function for c in cases)
    owner = 'Faizan' if index < 10 else 'Usman'
    code = {'email': 'EM', 'length': 'LN', 'ipv4': 'V4', 'ipv6': 'V6'}[function]
    cases.append(dict(
        id=f"{'FA' if index < 10 else 'US'}-{code}-{index % 10 + 1:02}",
        allocation=owner, module='ip_address' if function.startswith('ipv') else function,
        function=function, value_json=json.dumps(value, ensure_ascii=False),
        options_json=json.dumps(options), expected=expected, technique=technique,
        purpose=purpose, smoke='yes' if index in (0, 1) else 'no',
    ))


for value, options, expected, technique, purpose in [
    ('student@example.com', {}, 'valid', 'ECP', 'Ordinary mailbox'),
    ('studentexample.com', {}, 'invalid', 'ECP', 'Missing at sign'),
    ('', {}, 'invalid', 'ECP', 'Empty input'),
    ('a@@example.com', {}, 'invalid', 'ECP', 'Repeated at sign'),
    ('@example.com', {}, 'invalid', 'ECP', 'Missing local part'),
    ('student@', {}, 'invalid', 'ECP', 'Missing domain'),
    ('a' * 63 + '@example.com', {}, 'valid', 'BVA', 'Local part 63 characters'),
    ('a' * 64 + '@example.com', {}, 'valid', 'BVA', 'Local part at 64-character limit'),
    ('a' * 65 + '@example.com', {}, 'invalid', 'BVA', 'Local part above 64-character limit'),
    ('first.last+lab@example.com', {}, 'valid', 'ECP', 'Dots and plus tag'),
    ('.student@example.com', {}, 'invalid', 'ECP', 'Leading local-part dot'),
    ('student.@example.com', {}, 'invalid', 'ECP', 'Trailing local-part dot'),
    ('first..last@example.com', {}, 'invalid', 'ECP', 'Consecutive local-part dots'),
    ('student name@example.com', {}, 'invalid', 'ECP', 'Unquoted space'),
    ('Student@EXAMPLE.COM', {}, 'valid', 'ECP', 'Mixed letter case'),
    ('student@localhost', {}, 'invalid', 'ECP', 'Simple host disabled'),
    ('student@localhost', {'simple_host': True}, 'valid', 'ECP', 'Simple host enabled'),
    ('student@[192.0.2.1]', {'ipv4_address': True}, 'valid', 'ECP', 'IPv4 literal enabled'),
    ('student@[::1]', {'ipv6_address': True}, 'valid', 'ECP', 'IPv6 literal enabled'),
    ('bad@@example.com', {'r_ve': True}, 'raises', 'ECP', 'Raise mode on invalid email'),
]:
    add('email', value, options, expected, technique, purpose)

for value, options, expected, technique, purpose in [
    ('abcd', {'min_val': 3, 'max_val': 5}, 'valid', 'ECP', 'Inside range'),
    ('ab', {'min_val': 3, 'max_val': 5}, 'invalid', 'BVA', 'One below minimum'),
    ('abc', {'min_val': 3, 'max_val': 5}, 'valid', 'BVA', 'At minimum'),
    ('abcde', {'min_val': 3, 'max_val': 5}, 'valid', 'BVA', 'At maximum'),
    ('abcdef', {'min_val': 3, 'max_val': 5}, 'invalid', 'BVA', 'One above maximum'),
    ('', {}, 'valid', 'BVA', 'Empty input with no limits'),
    ('', {'min_val': 1}, 'invalid', 'BVA', 'Empty below minimum one'),
    ('a', {'min_val': 1}, 'valid', 'BVA', 'One character at minimum'),
    ('', {'max_val': 0}, 'valid', 'BVA', 'Empty at explicit maximum zero'),
    ('a', {'max_val': 0}, 'invalid', 'BVA', 'One above explicit maximum zero'),
    ('abc', {'min_val': 3, 'max_val': 3}, 'valid', 'BVA', 'Equal minimum and maximum'),
    ('ab', {'min_val': 3, 'max_val': 3}, 'invalid', 'BVA', 'Below exact length'),
    ('abcd', {'min_val': 3, 'max_val': 3}, 'invalid', 'BVA', 'Above exact length'),
    ('abc', {'min_val': -1}, 'invalid', 'ECP', 'Negative minimum returns ValidationError'),
    ('abc', {'max_val': -1}, 'invalid', 'ECP', 'Negative maximum returns ValidationError'),
    ('abcd', {'min_val': 5, 'max_val': 3}, 'invalid', 'ECP', 'Reversed bounds'),
    ('پاکستان', {'min_val': 7, 'max_val': 7}, 'valid', 'BVA', 'Unicode length counts characters'),
    ('   ', {'min_val': 3, 'max_val': 3}, 'valid', 'ECP', 'Whitespace counts toward length'),
    (None, {}, 'invalid', 'ECP', 'None converted to validation failure'),
    ('ab', {'min_val': 3, 'r_ve': True}, 'raises', 'BVA', 'Raise mode below minimum'),
]:
    add('length', value, options, expected, technique, purpose)

for value, options, expected, technique, purpose in [
    ('192.0.2.1', {}, 'valid', 'ECP', 'Ordinary IPv4 address'),
    ('256.1.1.1', {}, 'invalid', 'BVA', 'Octet above 255'),
    ('0.0.0.0', {}, 'valid', 'BVA', 'All octets at lower limit'),
    ('255.255.255.255', {}, 'valid', 'BVA', 'All octets at upper limit'),
    ('254.1.1.1', {}, 'valid', 'BVA', 'Octet below upper limit'),
    ('-1.1.1.1', {}, 'invalid', 'BVA', 'Negative octet'),
    ('1.1.1', {'cidr': False}, 'invalid', 'ECP', 'Too few octets'),
    ('1.1.1.1.1', {}, 'invalid', 'ECP', 'Too many octets'),
    ('01.2.3.4', {}, 'invalid', 'ECP', 'Leading zero'),
    ('', {}, 'invalid', 'ECP', 'Empty input'),
    ('192.0.2.0/0', {}, 'valid', 'BVA', 'Prefix at zero'),
    ('192.0.2.1/32', {}, 'valid', 'BVA', 'Prefix at 32'),
    ('192.0.2.1/33', {}, 'invalid', 'BVA', 'Prefix above 32'),
    ('192.0.2.1/-1', {}, 'invalid', 'BVA', 'Prefix below zero'),
    ('192.0.2.1/24', {'cidr': False}, 'invalid', 'ECP', 'CIDR disabled'),
    ('192.0.2.1', {'strict': True}, 'invalid', 'ECP', 'Strict requires prefix'),
    ('192.0.2.0/24', {'host_bit': False}, 'valid', 'ECP', 'Network address without host bits'),
    ('192.0.2.1/24', {'host_bit': False}, 'invalid', 'ECP', 'Host bits rejected'),
    ('10.0.0.1', {'private': True}, 'valid', 'ECP', 'Private filter accepts private address'),
    ('256.1.1.1', {'r_ve': True}, 'raises', 'BVA', 'Raise mode above octet limit'),
]:
    add('ipv4', value, options, expected, technique, purpose)

for value, options, expected, technique, purpose in [
    ('2001:db8::1', {}, 'valid', 'ECP', 'Compressed IPv6'),
    ('2001:db8::gggg', {}, 'invalid', 'ECP', 'Non-hexadecimal segment'),
    ('::', {}, 'valid', 'BVA', 'All-zero address'),
    ('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', {}, 'valid', 'BVA', 'All segments at upper limit'),
    ('10000::', {}, 'invalid', 'BVA', 'Segment exceeds ffff'),
    ('::1', {}, 'valid', 'ECP', 'Loopback address'),
    ('1:2:3:4:5:6:7:8', {}, 'valid', 'BVA', 'Exactly eight segments'),
    ('1:2:3:4:5:6:7:8:9', {}, 'invalid', 'BVA', 'Nine segments'),
    ('1:2:3:4:5:6:7', {}, 'invalid', 'BVA', 'Seven segments without compression'),
    ('', {}, 'invalid', 'ECP', 'Empty input'),
    ('2001:db8::/0', {}, 'valid', 'BVA', 'Prefix at zero'),
    ('2001:db8::1/128', {}, 'valid', 'BVA', 'Prefix at 128'),
    ('2001:db8::1/129', {}, 'invalid', 'BVA', 'Prefix above 128'),
    ('2001:db8::1/-1', {}, 'invalid', 'BVA', 'Prefix below zero'),
    ('2001:db8::1/64', {'cidr': False}, 'invalid', 'ECP', 'CIDR disabled'),
    ('2001:db8::1', {'strict': True}, 'invalid', 'ECP', 'Strict requires prefix'),
    ('2001:db8::/64', {'host_bit': False}, 'valid', 'ECP', 'Network without host bits'),
    ('2001:db8::1/64', {'host_bit': False}, 'invalid', 'ECP', 'Host bits rejected'),
    ('::ffff:192.0.2.1', {}, 'valid', 'ECP', 'IPv4-mapped IPv6'),
    ('2001:db8::gggg', {'r_ve': True}, 'raises', 'ECP', 'Raise mode on invalid IPv6'),
]:
    add('ipv6', value, options, expected, technique, purpose)

if __name__ == '__main__':
    with (ROOT / 'data' / 'validation_cases.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(cases[0]))
        writer.writeheader()
        writer.writerows(cases)
    print(f'Wrote {len(cases)} cases')
