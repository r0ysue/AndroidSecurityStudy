#! /usr/bin/python2.7
# -*- coding: utf8 -*-

import sys
import struct
import array
filename = "_data_app_com.example.dexcode-1_base.apk0.dex_722044_0"
insfilename ="722044_ins.bin"
DEX_MAGIC = "dex\n"
DEX_OPT_MAGIC = "dey\n"
import base64
import re
methodTable={}


FMT10T = 0
FMT10X = 1
FMT11N = 2
FMT11X = 3
FMT12X = 4
FMT20T = 5
FMT21C = 6
FMT21H = 7
FMT21S = 8
FMT21T = 9
FMT22B = 10
FMT22C = 11
FMT22S = 12
FMT22T = 13
FMT22X = 14
FMT23X = 15
FMT30T = 16
FMT31C = 17
FMT31I = 18
FMT31T = 19
FMT32X = 20
FMT35C = 21
FMT3RC = 22
FMT51L = 23

list1 = ['fmt10t', 'fmt10x', 'fmt11n', 'fmt11x', 'fmt12x', 'fmt20t', 'fmt21c', 'fmt21h',
		 'fmt21s', 'fmt21t', 'fmt22b', 'fmt22c', 'fmt22s', 'fmt22t', 'fmt22x', 'fmt23x',
		 'fmt30t', 'fmt31c', 'fmt31i', 'fmt31t', 'fmt32x', 'fmt35c', 'fmt3rc', 'fmt51l']


def get_uleb128p1(content):
	n, value = get_uleb128(content)
	value -= 1
	return n, value


def get_uleb128(content):
	value = 0
	if len(content) < 5:
		for i in xrange(0, len(content)):
			tmp = ord(content[i]) & 0x7f
			value = tmp << (i * 7) | value
			if (ord(content[i]) & 0x80) != 0x80:
				break
	elif len(content) == 5:
		for i in xrange(0, 5):
			tmp = ord(content[i]) & 0x7f
			value = tmp << (i * 7) | value
			if (ord(content[i]) & 0x80) != 0x80:
				break
	elif len(content) > 5:
		for i in xrange(0, 5):
			tmp = ord(content[i]) & 0x7f
			value = tmp << (i * 7) | value
			if (ord(content[i]) & 0x80) != 0x80:
				break
	if i == 4 and (tmp & 0xf0) != 0:
		print "parse a error uleb128 number"
		return -1
	return i + 1, value

def get_leb128(content):
	value = 0

	mask = [0xffffff80, 0xffffc000, 0xffe00000, 0xf0000000, 0]
	bitmask = [0x40, 0x40, 0x40, 0x40, 0x8]
	value = 0
	i = 0
	if len(content) < 5:
		for i in xrange(0, len(content)):
			tmp = ord(content[i]) & 0x7f
			value = tmp << (i * 7) | value
			if (ord(content[i]) & 0x80) != 0x80:
				if bitmask[i] & tmp:
					value |= mask[i]
				break
	elif len(content) == 5:
		for i in xrange(0, 5):
			tmp = ord(content[i]) & 0x7f
			value = tmp << (i * 7) | value
			if (ord(content[i]) & 0x80) != 0x80:
				if bitmask[i] & tmp:
					value |= mask[i]
				break
	elif len(content) > 5:
		for i in xrange(0, 5):
			tmp = ord(content[i]) & 0x7f
			value = tmp << (i * 7) | value
			if (ord(content[i]) & 0x80) != 0x80:
				if bitmask[i] & tmp:
					value |= mask[i]
				break
	if i == 4 and (tmp & 0xf0) != 0:
		print "parse a error uleb128 number"
		return -1
	buffer = struct.pack("I", value)
	value, = struct.unpack("i", buffer)
	return i + 1, value
def parse_FMT10X(buffer, dex_object, pc_point, offset):
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1])


def parse_FMT10T(buffer, dex_object, pc_point, offset):
	val, = struct.unpack_from("b", buffer, 1)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "%04x" % (val + offset))


def parse_FMT11N(buffer, dex_object, pc_point, offset):
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % (ord(buffer[1]) & 0xf),
			"%d" % ((ord(buffer[1]) >> 4) & 0xf))


def parse_FMT11X(buffer, dex_object, pc_point, offset):
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]))


def parse_FMT12X(buffer, dex_object, pc_point, offset):
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % (ord(buffer[1]) & 0x0f),
			"v%d" % ((ord(buffer[1]) >> 4) & 0xf))


def parse_FMT20T(buffer, dex_object, pc_point, offset):
	v, = struct.unpack_from("h", buffer, 2)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "%04x" % (v + offset))


def parse_FMT21C(buffer, dex_object, pc_point, offset):
	val = ord(buffer[0])

	v, = struct.unpack_from("H", buffer, 2)
	arg1 = "@%d" % v
	if val == 0x1a:
		arg1 = "\"%s\"" % dex_object.getstringbyid(v)
	elif val in [0x1c, 0x1f, 0x22]:
		arg1 = "type@%s" % dex_object.gettypename(v)
	else:
		arg1 = "field@%s  //%s" % (dex_object.getfieldname(v), dex_object.getfieldfullname(v))
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), arg1)


def parse_FMT21H(buffer, dex_object, pc_point, offset):
	v, = struct.unpack_from("H", buffer, 2)
	if ord(buffer[1]) == 0x19:
		arg1 = "@%d000000000000" % v
	else:
		arg1 = "@%d0000" % v
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), arg1)


def parse_FMT21S(buffer, dex_object, pc_point, offset):
	v, = struct.unpack_from("H", buffer, 2)
	arg1 = "%d" % v
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), arg1)


def parse_FMT21T(buffer, dex_object, pc_point, offset):
	v, = struct.unpack_from("h", buffer, 2)
	arg1 = "%04x" % (v + offset)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), arg1)


def parse_FMT22B(buffer, dex_object, pc_point, offset):
	cc, bb, = struct.unpack_from("Bb", buffer, 2)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), "v%d" % bb, "%d" % cc)


def parse_FMT22C(buffer, dex_object, pc_point, offset):
	cccc, = struct.unpack_from("H", buffer, 2)
	if ord(buffer[0]) == 0x20 or ord(buffer[0]) == 0x23:
		prefix = "type@%s" % (dex_object.gettypename(cccc))
	else:
		prefix = "field@%s  //%s" % (dex_object.getfieldname(cccc), dex_object.getfieldfullname(cccc))

	bb = ord(buffer[1]) >> 4
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % (ord(buffer[1]) & 0xf),
			"v%d" % ((ord(buffer[1]) >> 4) & 0xf), "%s" % prefix)


def parse_FMT22S(buffer, dex_object, pc_point, offset):
	bb = ord(buffer[1]) >> 4
	cccc, = struct.unpack_from("h", buffer, 2)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % (ord(buffer[1]) & 0xf),
			"v%d" % ((ord(buffer[1]) >> 4) & 0xf), "%d" % cccc)


def parse_FMT22T(buffer, dex_object, pc_point, offset):
	bb = ord(buffer[1]) >> 4
	cccc, = struct.unpack_from("h", buffer, 2)

	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % (ord(buffer[1]) & 0xf),
			"v%d" % ((ord(buffer[1]) >> 4) & 0xf), "%04x" % (cccc + offset))


def parse_FMT22X(buffer, dex_object, pc_point, offset):
	v, = struct.unpack_from("h", buffer, 2)
	arg1 = "v%d" % v
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), arg1)


def parse_FMT23X(buffer, dex_object, pc_point, offset):
	cc, bb, = struct.unpack_from("Bb", buffer, 2)
	return (
	dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), "v%d" % bb, "v%d" % cc)


def parse_FMT30T(buffer, dex_object, pc_point, offset):
	aaaaaaaa, = struct.unpack_from("i", buffer, 2)
	return dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "+%x" % (aaaaaaaa + offset)


def parse_FMT31C(buffer, dex_object, pc_point, offset):
	bbbbbbbb, = struct.unpack_from("I", buffer, 2)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), "+%d" % bbbbbbbb)


def parse_FMT31I(buffer, dex_object, pc_point, offset):
	bbbbbbbb, = struct.unpack_from("I", buffer, 2)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), "%d" % bbbbbbbb)


def parse_FMT31T(buffer, dex_object, pc_point, offset):
	bbbbbbbb, = struct.unpack_from("i", buffer, 2)
	return (
	dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), "string@%d" % bbbbbbbb)


def parse_FMT32X(buffer, dex_object, pc_point, offset):
	aaaa, bbbb, = struct.unpack_from("hh", buffer, 2)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % aaaa, "v%d" % bbbb)


def parse_FMT35C(buffer, dex_object, pc_point, offset):
	A = ord(buffer[1]) >> 4
	G = ord(buffer[1]) & 0xf
	D = ord(buffer[4]) >> 4
	C = ord(buffer[4]) & 0xf
	F = ord(buffer[5]) >> 4
	E = ord(buffer[5]) & 0xf
	bbbb, = struct.unpack_from("H", buffer, 2)
	if ord(buffer[0]) == 0x24:
		prefix = "type@%s" % (dex_object.getstringbyid(bbbb))
	else:
		prefix = "meth@%s  //%s" % (dex_object.getmethodname(bbbb), dex_object.getmethodfullname(bbbb, True))
		pass
	if A == 5:
		return (
		dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % C, "v%d" % D, "v%d" % E, "v%d" % F,
		"v%d" % G, "%s" % (prefix))
	elif A == 4:
		return (
		dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % C, "v%d" % D, "v%d" % E, "v%d" % F,
		"%s" % (prefix))
	elif A == 3:
		return (
		dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % C, "v%d" % D, "v%d" % E, "%s" % (prefix))
	elif A == 2:
		return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % C, "v%d" % D, "%s" % (prefix))
	elif A == 1:
		return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % C, "%s" % (prefix))
	elif A == 0:
		return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "%s" % (prefix))
	else:
		return (dex_decode[ord(buffer[0])][4], "error .......")
	return (
	dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % C, "v%d" % D, "v%d" % E, "v%d" % F, "v%d" % G,
	"%s" % (prefix))


def parse_FMT3RC(buffer, dex_object, pc_point, offset):
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1])


def parse_FMT51L(buffer, dex_object, pc_point, offset):
	if len(buffer) < 10:
		return (1, "")
	bb = struct.unpack_from("q", buffer, 2)
	return (dex_decode[ord(buffer[0])][4], dex_decode[ord(buffer[0])][1], "v%d" % ord(buffer[1]), "%d" % bb)


func_point = [parse_FMT10T, parse_FMT10X, parse_FMT11N, parse_FMT11X, parse_FMT12X, parse_FMT20T, parse_FMT21C,
			  parse_FMT21H, parse_FMT21S, parse_FMT21T, parse_FMT22B, parse_FMT22C, parse_FMT22S, parse_FMT22T,
			  parse_FMT22X, parse_FMT23X, parse_FMT30T, parse_FMT31C, parse_FMT31I, parse_FMT31T, parse_FMT32X,
			  parse_FMT35C, parse_FMT3RC, parse_FMT51L]


def parse_instruction(buffer, offset, dex_object):
	n = len(buffer)
	start = 0

	while start < n:
		if n == 1736:
			print "start = %d" % start
		op = ord(buffer[start])
		if op == 0:
			type = ord(buffer[start + 1])
			if type == 1:
				size, = struct.unpack_from("H", buffer, 2 + start)
				start += (size * 2 + 4) * 2
				continue
			elif type == 2:
				size, = struct.unpack_from("H", buffer, 2 + start)
				start += (size * 4 + 2) * 2
				continue
			elif type == 3:
				width, = struct.unpack_from("H", buffer, 2 + start)
				size, = struct.unpack_from("I", buffer, 4 + start)
				# width,size,=struct.unpack_from("HI",buffer,2+start)
				start += (8 + ((size * width + 1) / 2) * 2)
				continue

		val = func_point[dex_decode[op][3]](buffer[start:], dex_object, offset + start, start / 2)
		str = ""
		m = 0
		for x in buffer[start:start + 2 * val[0]]:
			str += "%02x" % ord(x)
			m += 1
			if m % 2 == 0:
				str += " "

		print "%08x: %-36s |%04x:" % (offset + start, str, start / 2),
		m = 0
		for v in val[1:]:
			if m > 1:
				print ",",
			print v,
			m += 1
		print ""
		start += 2 * val[0]


def parseMyinstruction(buffer, offset, dex_object):
	n = len(buffer)
	start = 0

	while start < n:
		if n == 1736:
			print "start = %d" % start
		op = ord(buffer[start])
		if op == 0:
			type = ord(buffer[start + 1])
			if type == 1:
				size, = struct.unpack_from("H", buffer, 2 + start)
				start += (size * 2 + 4) * 2
				continue
			elif type == 2:
				size, = struct.unpack_from("H", buffer, 2 + start)
				start += (size * 4 + 2) * 2
				continue
			elif type == 3:
				width, = struct.unpack_from("H", buffer, 2 + start)
				size, = struct.unpack_from("I", buffer, 4 + start)
				# width,size,=struct.unpack_from("HI",buffer,2+start)
				start += (8 + ((size * width + 1) / 2) * 2)
				continue

		val = func_point[dex_decode[op][3]](buffer[start:], dex_object, offset + start, start / 2)
		str = ""
		m = 0
		for x in buffer[start:start + 2 * val[0]]:
			str += "%02x" % ord(x)
			m += 1
			if m % 2 == 0:
				str += " "

		print "%08x: %-36s |%04x:" % (offset + start, str, start / 2),
		m = 0
		for v in val[1:]:
			if m > 1:
				print ",",
			print v,
			m += 1
		print ""
		start += 2 * val[0]
dex_decode = {
	0: (0x00, 'nop', 'fmt10x', FMT10X, 1),
	1: (0x01, 'move', 'fmt12x', FMT12X, 1),
	2: (0x02, 'move/from16', 'fmt22x', FMT22X, 2),
	3: (0x03, 'move/16', 'fmt32x', FMT32X, 3),
	4: (0x04, 'move-wide', 'fmt12x', FMT12X, 1),
	5: (0x05, 'move-wide/from16', 'fmt22x', FMT22X, 2),
	6: (0x06, 'move-wide/16', 'fmt32x', FMT32X, 3),
	7: (0x07, 'move-object', 'fmt12x', FMT12X, 1),
	8: (0x08, 'move-object/from16', 'fmt22x', FMT22X, 2),
	9: (0x09, 'move-object/16', 'fmt32x', FMT32X, 3),
	10: (0x0a, 'move-result', 'fmt11x', FMT11X, 1),
	11: (0x0b, 'move-result-wide', 'fmt11x', FMT11X, 1),
	12: (0x0c, 'move-result-object', 'fmt11x', FMT11X, 1),
	13: (0x0d, 'move-exception', 'fmt11x', FMT11X, 1),
	14: (0x0e, 'return-void', 'fmt10x', FMT10X, 1),
	15: (0x0f, 'return', 'fmt11x', FMT11X, 1),
	16: (0x10, 'return-wide', 'fmt11x', FMT11X, 1),
	17: (0x11, 'return-object', 'fmt11x', FMT11X, 1),
	18: (0x12, 'const/4', 'fmt11n', FMT11N, 1),
	19: (0x13, 'const/16', 'fmt21s', FMT21S, 2),
	20: (0x14, 'const', 'fmt31i', FMT31I, 3),
	21: (0x15, 'const/high16', 'fmt21h', FMT21H, 2),
	22: (0x16, 'const-wide/16', 'fmt21s', FMT21S, 2),
	23: (0x17, 'const-wide/32', 'fmt31i', FMT31I, 3),
	24: (0x18, 'const-wide', 'fmt51l', FMT51L, 5),
	25: (0x19, 'const-wide/high16', 'fmt21h', FMT21H, 2),
	26: (0x1a, 'const-string', 'fmt21c', FMT21C, 2),
	27: (0x1b, 'const-string/jumbo', 'fmt31c', FMT31C, 3),
	28: (0x1c, 'const-class', 'fmt21c', FMT21C, 2),
	29: (0x1d, 'monitor-enter', 'fmt11x', FMT11X, 1),
	30: (0x1e, 'monitor-exit', 'fmt11x', FMT11X, 1),
	31: (0x1f, 'check-cast', 'fmt21c', FMT21C, 2),
	32: (0x20, 'instance-of', 'fmt22c', FMT22C, 2),
	33: (0x21, 'array-length', 'fmt12x', FMT12X, 1),
	34: (0x22, 'new-instance', 'fmt21c', FMT21C, 2),
	35: (0x23, 'new-array', 'fmt22c', FMT22C, 2),
	36: (0x24, 'filled-new-array', 'fmt35c', FMT35C, 3),
	37: (0x25, 'filled-new-array/range', 'fmt3rc', FMT3RC, 3),
	38: (0x26, 'fill-array-data', 'fmt31t', FMT31T, 3),
	39: (0x27, 'throw', 'fmt11x', FMT11X, 1),
	40: (0x28, 'goto', 'fmt10t', FMT10T, 1),
	41: (0x29, 'goto/16', 'fmt20t', FMT20T, 2),
	42: (0x2a, 'goto/32', 'fmt30t', FMT30T, 3),
	43: (0x2b, 'packed-switch', 'fmt31t', FMT31T, 3),
	44: (0x2c, 'sparse-switch', 'fmt31t', FMT31T, 3),
	45: (0x2d, 'cmpl-float', 'fmt23x', FMT23X, 2),
	46: (0x2e, 'cmpg-float', 'fmt23x', FMT23X, 2),
	47: (0x2f, 'cmpl-double', 'fmt23x', FMT23X, 2),
	48: (0x30, 'cmpg-double', 'fmt23x', FMT23X, 2),
	49: (0x31, 'cmp-long', 'fmt23x', FMT23X, 2),
	50: (0x32, 'if-eq', 'fmt22t', FMT22T, 2),
	51: (0x33, 'if-ne', 'fmt22t', FMT22T, 2),
	52: (0x34, 'if-lt', 'fmt22t', FMT22T, 2),
	53: (0x35, 'if-ge', 'fmt22t', FMT22T, 2),
	54: (0x36, 'if-gt', 'fmt22t', FMT22T, 2),
	55: (0x37, 'if-le', 'fmt22t', FMT22T, 2),
	56: (0x38, 'if-eqz', 'fmt21t', FMT21T, 2),
	57: (0x39, 'if-nez', 'fmt21t', FMT21T, 2),
	58: (0x3a, 'if-ltz', 'fmt21t', FMT21T, 2),
	59: (0x3b, 'if-gez', 'fmt21t', FMT21T, 2),
	60: (0x3c, 'if-gtz', 'fmt21t', FMT21T, 2),
	61: (0x3d, 'if-lez', 'fmt21t', FMT21T, 2),
	62: (0x3e, 'unused', 'fmt10x', FMT10X, 1),
	63: (0x3f, 'unused', 'fmt10x', FMT10X, 1),
	64: (0x40, 'unused', 'fmt10x', FMT10X, 1),
	65: (0x41, 'unused', 'fmt10x', FMT10X, 1),
	66: (0x42, 'unused', 'fmt10x', FMT10X, 1),
	67: (0x43, 'unused', 'fmt10x', FMT10X, 1),
	68: (0x44, 'aget', 'fmt23x', FMT23X, 2),
	69: (0x45, 'aget-wide', 'fmt23x', FMT23X, 2),
	70: (0x46, 'aget-object', 'fmt23x', FMT23X, 2),
	71: (0x47, 'aget-boolean', 'fmt23x', FMT23X, 2),
	72: (0x48, 'aget-byte', 'fmt23x', FMT23X, 2),
	73: (0x49, 'aget-char', 'fmt23x', FMT23X, 2),
	74: (0x4a, 'aget-short', 'fmt23x', FMT23X, 2),
	75: (0x4b, 'aput', 'fmt23x', FMT23X, 2),
	76: (0x4c, 'aput-wide', 'fmt23x', FMT23X, 2),
	77: (0x4d, 'aput-object', 'fmt23x', FMT23X, 2),
	78: (0x4e, 'aput-boolean', 'fmt23x', FMT23X, 2),
	79: (0x4f, 'aput-byte', 'fmt23x', FMT23X, 2),
	80: (0x50, 'aput-shar', 'fmt23x', FMT23X, 2),
	81: (0x51, 'aput-short', 'fmt23x', FMT23X, 2),
	82: (0x52, 'iget', 'fmt22c', FMT22C, 2),
	83: (0x53, 'iget-wide', 'fmt22c', FMT22C, 2),
	84: (0x54, 'iget-object', 'fmt22c', FMT22C, 2),
	85: (0x55, 'iget-boolean', 'fmt22c', FMT22C, 2),
	86: (0x56, 'iget-byte', 'fmt22c', FMT22C, 2),
	87: (0x57, 'iget-char', 'fmt22c', FMT22C, 2),
	88: (0x58, 'iget-short', 'fmt22c', FMT22C, 2),
	89: (0x59, 'iput', 'fmt22c', FMT22C, 2),
	90: (0x5a, 'iput-wide', 'fmt22c', FMT22C, 2),
	91: (0x5b, 'iput-object', 'fmt22c', FMT22C, 2),
	92: (0x5c, 'iput-boolean', 'fmt22c', FMT22C, 2),
	93: (0x5d, 'iput-byte', 'fmt22c', FMT22C, 2),
	94: (0x5e, 'iput-char', 'fmt22c', FMT22C, 2),
	95: (0x5f, 'iput-short', 'fmt22c', FMT22C, 2),
	96: (0x60, 'sget', 'fmt21c', FMT21C, 2),
	97: (0x61, 'sget-wide', 'fmt21c', FMT21C, 2),
	98: (0x62, 'sget-object', 'fmt21c', FMT21C, 2),
	99: (0x63, 'sget-boolean', 'fmt21c', FMT21C, 2),
	100: (0x64, 'sget-byte', 'fmt21c', FMT21C, 2),
	101: (0x65, 'sget-char', 'fmt21c', FMT21C, 2),
	102: (0x66, 'sget-short', 'fmt21c', FMT21C, 2),
	103: (0x67, 'sput', 'fmt21c', FMT21C, 2),
	104: (0x68, 'sput-wide', 'fmt21c', FMT21C, 2),
	105: (0x69, 'sput-object', 'fmt21c', FMT21C, 2),
	106: (0x6a, 'sput-boolean', 'fmt21c', FMT21C, 2),
	107: (0x6b, 'sput-byte', 'fmt21c', FMT21C, 2),
	108: (0x6c, 'sput-char', 'fmt21c', FMT21C, 2),
	109: (0x6d, 'sput-short', 'fmt21c', FMT21C, 2),
	110: (0x6e, 'invoke-virtual', 'fmt35c', FMT35C, 3),
	111: (0x6f, 'invoke-super', 'fmt35c', FMT35C, 3),
	112: (0x70, 'invoke-direct', 'fmt35c', FMT35C, 3),
	113: (0x71, 'invoke-static', 'fmt35c', FMT35C, 3),
	114: (0x72, 'invoke-insterface', 'fmt35c', FMT35C, 3),
	115: (0x73, 'unused', 'fmt10x', FMT10X, 1),
	116: (0x74, 'invoke-virtual/range', 'fmt3rc', FMT3RC, 3),
	117: (0x75, 'invoke-super/range', 'fmt3rc', FMT3RC, 3),
	118: (0x76, 'invoke-direct/range', 'fmt3rc', FMT3RC, 3),
	119: (0x77, 'invoke-static/range', 'fmt3rc', FMT3RC, 3),
	120: (0x78, 'invoke-interface/range', 'fmt3rc', FMT3RC, 3),
	121: (0x79, 'unused', 'fmt10x', FMT10X, 1),
	122: (0x7a, 'unused', 'fmt10x', FMT10X, 1),
	123: (0x7b, 'neg-int', 'fmt12x', FMT12X, 1),
	124: (0x7c, 'not-int', 'fmt12x', FMT12X, 1),
	125: (0x7d, 'neg-long', 'fmt12x', FMT12X, 1),
	126: (0x7e, 'not-long', 'fmt12x', FMT12X, 1),
	127: (0x7f, 'neg-float', 'fmt12x', FMT12X, 1),
	128: (0x80, 'neg-double', 'fmt12x', FMT12X, 1),
	129: (0x81, 'int-to-long', 'fmt12x', FMT12X, 1),
	130: (0x82, 'int-to-float', 'fmt12x', FMT12X, 1),
	131: (0x83, 'int-to-double', 'fmt12x', FMT12X, 1),
	132: (0x84, 'long-to-int', 'fmt12x', FMT12X, 1),
	133: (0x85, 'long-to-float', 'fmt12x', FMT12X, 1),
	134: (0x86, 'long-to-double', 'fmt12x', FMT12X, 1),
	135: (0x87, 'float-to-int', 'fmt12x', FMT12X, 1),
	136: (0x88, 'float-to-long', 'fmt12x', FMT12X, 1),
	137: (0x89, 'float-to-double', 'fmt12x', FMT12X, 1),
	138: (0x8a, 'double-to-int', 'fmt12x', FMT12X, 1),
	139: (0x8b, 'double-to-long', 'fmt12x', FMT12X, 1),
	140: (0x8c, 'double-to-float', 'fmt12x', FMT12X, 1),
	141: (0x8d, 'int-to-byte', 'fmt12x', FMT12X, 1),
	142: (0x8e, 'int-to-char', 'fmt12x', FMT12X, 1),
	143: (0x8f, 'int-to-short', 'fmt12x', FMT12X, 1),
	144: (0x90, 'add-int', 'fmt23x', FMT23X, 2),
	145: (0x91, 'sub-int', 'fmt23x', FMT23X, 2),
	146: (0x92, 'mul-int', 'fmt23x', FMT23X, 2),
	147: (0x93, 'div-int', 'fmt23x', FMT23X, 2),
	148: (0x94, 'rem-int', 'fmt23x', FMT23X, 2),
	149: (0x95, 'and-int', 'fmt23x', FMT23X, 2),
	150: (0x96, 'or-int', 'fmt23x', FMT23X, 2),
	151: (0x97, 'xor-int', 'fmt23x', FMT23X, 2),
	152: (0x98, 'shl-int', 'fmt23x', FMT23X, 2),
	153: (0x99, 'shr-int', 'fmt23x', FMT23X, 2),
	154: (0x9a, 'ushr-int', 'fmt23x', FMT23X, 2),
	155: (0x9b, 'add-long', 'fmt23x', FMT23X, 2),
	156: (0x9c, 'sub-long', 'fmt23x', FMT23X, 2),
	157: (0x9d, 'mul-long', 'fmt23x', FMT23X, 2),
	158: (0x9e, 'div-long', 'fmt23x', FMT23X, 2),
	159: (0x9f, 'rem-long', 'fmt23x', FMT23X, 2),
	160: (0xa0, 'and-long', 'fmt23x', FMT23X, 2),
	161: (0xa1, 'or-long', 'fmt23x', FMT23X, 2),
	162: (0xa2, 'xor-long', 'fmt23x', FMT23X, 2),
	163: (0xa3, 'shl-long', 'fmt23x', FMT23X, 2),
	164: (0xa4, 'shr-long', 'fmt23x', FMT23X, 2),
	165: (0xa5, 'ushr-long', 'fmt23x', FMT23X, 2),
	166: (0xa6, 'add-float', 'fmt23x', FMT23X, 2),
	167: (0xa7, 'sub-float', 'fmt23x', FMT23X, 2),
	168: (0xa8, 'mul-float', 'fmt23x', FMT23X, 2),
	169: (0xa9, 'div-float', 'fmt23x', FMT23X, 2),
	170: (0xaa, 'rem-float', 'fmt23x', FMT23X, 2),
	171: (0xab, 'add-double', 'fmt23x', FMT23X, 2),
	172: (0xac, 'sub-double', 'fmt23x', FMT23X, 2),
	173: (0xad, 'mul-double', 'fmt23x', FMT23X, 2),
	174: (0xae, 'div-double', 'fmt23x', FMT23X, 2),
	175: (0xaf, 'rem-double', 'fmt23x', FMT23X, 2),
	176: (0xb0, 'add-int/2addr', 'fmt12x', FMT12X, 1),
	177: (0xb1, 'sub-int/2addr', 'fmt12x', FMT12X, 1),
	178: (0xb2, 'mul-int/2addr', 'fmt12x', FMT12X, 1),
	179: (0xb3, 'div-int/2addr', 'fmt12x', FMT12X, 1),
	180: (0xb4, 'rem-int/2addr', 'fmt12x', FMT12X, 1),
	181: (0xb5, 'and-int/2addr', 'fmt12x', FMT12X, 1),
	182: (0xb6, 'or-int/2addr', 'fmt12x', FMT12X, 1),
	183: (0xb7, 'xor-int/2addr', 'fmt12x', FMT12X, 1),
	184: (0xb8, 'shl-int/2addr', 'fmt12x', FMT12X, 1),
	185: (0xb9, 'shr-int/2addr', 'fmt12x', FMT12X, 1),
	186: (0xba, 'ushr-int/2addr', 'fmt12x', FMT12X, 1),
	187: (0xbb, 'add-long/2addr', 'fmt12x', FMT12X, 1),
	188: (0xbc, 'sub-long/2addr', 'fmt12x', FMT12X, 1),
	189: (0xbd, 'mul-long/2addr', 'fmt12x', FMT12X, 1),
	190: (0xbe, 'div-long/2addr', 'fmt12x', FMT12X, 1),
	191: (0xbf, 'rem-long/2addr', 'fmt12x', FMT12X, 1),
	192: (0xc0, 'and-long/2addr', 'fmt12x', FMT12X, 1),
	193: (0xc1, 'or-long/2addr', 'fmt12x', FMT12X, 1),
	194: (0xc2, 'xor-long/2addr', 'fmt12x', FMT12X, 1),
	195: (0xc3, 'shl-long/2addr', 'fmt12x', FMT12X, 1),
	196: (0xc4, 'shr-long/2addr', 'fmt12x', FMT12X, 1),
	197: (0xc5, 'ushr-long/2addr', 'fmt12x', FMT12X, 1),
	198: (0xc6, 'add-float/2addr', 'fmt12x', FMT12X, 1),
	199: (0xc7, 'sub-float/2addr', 'fmt12x', FMT12X, 1),
	200: (0xc8, 'mul-float/2addr', 'fmt12x', FMT12X, 1),
	201: (0xc9, 'div-float/2addr', 'fmt12x', FMT12X, 1),
	202: (0xca, 'rem-float/2addr', 'fmt12x', FMT12X, 1),
	203: (0xcb, 'add-double/2addr', 'fmt12x', FMT12X, 1),
	204: (0xcc, 'sub-double/2addr', 'fmt12x', FMT12X, 1),
	205: (0xcd, 'mul-double/2addr', 'fmt12x', FMT12X, 1),
	206: (0xce, 'div-double/2addr', 'fmt12x', FMT12X, 1),
	207: (0xcf, 'rem-double/2addr', 'fmt12x', FMT12X, 1),
	208: (0xd0, 'add-int/lit16', 'fmt22s', FMT22S, 2),
	209: (0xd1, 'rsub-int', 'fmt22s', FMT22S, 2),
	210: (0xd2, 'mul-int/lit16', 'fmt22s', FMT22S, 2),
	211: (0xd3, 'div-int/lit16', 'fmt22s', FMT22S, 2),
	212: (0xd4, 'rem-int/lit16', 'fmt22s', FMT22S, 2),
	213: (0xd5, 'and-int/lit16', 'fmt22s', FMT22S, 2),
	214: (0xd6, 'or-int/lit16', 'fmt22s', FMT22S, 2),
	215: (0xd7, 'xor-int/lit16', 'fmt22s', FMT22S, 2),
	216: (0xd8, 'add-int/lit8', 'fmt22b', FMT22B, 2),
	217: (0xd9, 'rsub-int/lit8', 'fmt22b', FMT22B, 2),
	218: (0xda, 'mul-int/lit8', 'fmt22b', FMT22B, 2),
	219: (0xdb, 'div-int/lit8', 'fmt22b', FMT22B, 2),
	220: (0xdc, 'rem-int/lit8', 'fmt22b', FMT22B, 2),
	221: (0xdd, 'and-int/lit8', 'fmt22b', FMT22B, 2),
	222: (0xde, 'or-int/lit8', 'fmt22b', FMT22B, 2),
	223: (0xdf, 'xor-int/lit8', 'fmt22b', FMT22B, 2),
	224: (0xe0, 'shl-int/lit8', 'fmt22b', FMT22B, 2),
	225: (0xe1, 'shr-int/lit8', 'fmt22b', FMT22B, 2),
	226: (0xe2, 'ushr-int/lit8', 'fmt22b', FMT22B, 2),
	227: (0xe3, 'unused', 'fmt10x', FMT10X, 1),
	228: (0xe4, 'unused', 'fmt10x', FMT10X, 1),
	229: (0xe5, 'unused', 'fmt10x', FMT10X, 1),
	230: (0xe6, 'unused', 'fmt10x', FMT10X, 1),
	231: (0xe7, 'unused', 'fmt10x', FMT10X, 1),
	232: (0xe8, 'unused', 'fmt10x', FMT10X, 1),
	233: (0xe9, 'unused', 'fmt10x', FMT10X, 1),
	234: (0xea, 'unused', 'fmt10x', FMT10X, 1),
	235: (0xeb, 'unused', 'fmt10x', FMT10X, 1),
	236: (0xec, 'unused', 'fmt10x', FMT10X, 1),
	237: (0xed, 'unused', 'fmt10x', FMT10X, 1),
	238: (0xee, 'unused', 'fmt10x', FMT10X, 1),
	239: (0xef, 'unused', 'fmt10x', FMT10X, 1),
	240: (0xf0, 'unused', 'fmt10x', FMT10X, 1),
	241: (0xf1, 'unused', 'fmt10x', FMT10X, 1),
	242: (0xf2, 'unused', 'fmt10x', FMT10X, 1),
	243: (0xf3, 'unused', 'fmt10x', FMT10X, 1),
	244: (0xf4, 'unused', 'fmt10x', FMT10X, 1),
	245: (0xf5, 'unused', 'fmt10x', FMT10X, 1),
	246: (0xf6, 'unused', 'fmt10x', FMT10X, 1),
	247: (0xf7, 'unused', 'fmt10x', FMT10X, 1),
	248: (0xf8, 'unused', 'fmt10x', FMT10X, 1),
	249: (0xf9, 'unused', 'fmt10x', FMT10X, 1),
	250: (0xfa, 'unused', 'fmt10x', FMT10X, 1),
	251: (0xfb, 'unused', 'fmt10x', FMT10X, 1),
	252: (0xfc, 'unused', 'fmt10x', FMT10X, 1),
	253: (0xfd, 'unused', 'fmt10x', FMT10X, 1),
	254: (0xfe, 'unused', 'fmt10x', FMT10X, 1),
	255: (0xff, 'unused', 'fmt10x', FMT10X, 1),
}
class CodeItem:
	methodname=""
	inssize=0
	insarray=""
	idx=0
	def __init__(self,number,methodname, inssize,insarray):
		self.idx=number
		self.methodname = methodname
		self.inssize = inssize
		self.insarray=insarray
class DexMethod:
    methodname=""
    inssize=0
    offset=0
    idx=0
    def __init__(self,number,methodname, inssize,offset):
		self.idx=number
		self.methodname = methodname
		self.inssize = inssize
		self.offset=offset
def parseinsfile():
    global insfilename
    insfile=open(insfilename)
    content=insfile.read()
    insfile.close()
    #;{name:artMethod::dumpmethod DexFile_dumpDexFile'
    # dexfile name:classes.dex--
    # insfilepath:/data/data/com.wlqq/10668484_ins.bin--
    # code_item_len:40,
    # code_item_len:40,
    # ins:AgABAAIAAABLnY4ADAAAACIAFwNwEPoOAABuIP4OEAAMAR8BFwMRAQ==};
    insarray=re.findall(r"{name:(.*?),method_idx:(.*?),offset:(.*?),code_item_len:(.*?),ins:(.*?)}",content) #(.*?)最短匹配
    for eachins in insarray:
		methodname=eachins[0].replace(" ","")
		number=(int)(eachins[1])
		offset=(int)(eachins[2])
		inssize=int(eachins[3])
		ins=eachins[4]
		tempmethod=CodeItem(number,methodname,inssize,ins)
		methodTable[number]=tempmethod #添加method
class dex_encode_field:
	def __init__(self,idx,flags):
		self.m_field_idx_diff = idx
		self.m_access_flags = flags
	def printf(self,dex_object):
		name = dex_object.gettypenamebyid(self.m_field_idx_diff)
		#print "%-20s%08x %s"%("field_idx_diff",self.m_field_idx_diff,name)	
		flags = dex_object.get_access_flags(self.m_access_flags)
		#print "%-20s%08x %s"%("access_flags",self.m_access_flags,flags)			
		print "%s "%flags,
		dex_object.FieldId_list[self.m_field_idx_diff].printf_l(dex_object)
class method_code:
	def __init__(self,dex_object,offset):
		format = "H"
		self.registers_size, = struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.ins_size,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.outs_size,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.tries_size,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		format = "I"
		self.debug_info_off,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.insns_size,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.insns = offset
		offset += 2*self.insns_size
		if self.insns_size %2 ==1:
			offset+=2
		if self.tries_size == 0:
			self.tries = 0 
			self.handlers = 0
		else:
			self.tries = offset 
			self.handlers = offset + self.tries_size * struct.calcsize("I2H")
	def get_param_list(self,dex_object):
		if self.debug_info_off != 0:
			return parse_debug_info_method_parameter_list(dex_object,self.debug_info_off)
		return []
	def printf(self,dex_object,prefix=""):
		print "%s%-20s:%08x:%10d"%(prefix,"registers_size",self.registers_size,self.registers_size)
		print "%s%-20s:%08x:%10d"%(prefix,"insns_size",self.insns_size,self.insns_size)
		print "%s%-20s:%08x:%10d"%(prefix,"debug_info_off",self.debug_info_off,self.debug_info_off)
		print "%s%-20s:%08x:%10d"%(prefix,"ins_size",self.ins_size,self.ins_size)
		print "%s%-20s:%08x:%10d"%(prefix,"outs_size",self.outs_size,self.outs_size)
		print "%s%-20s:%08x:%10d"%(prefix,"tries_size",self.tries_size,self.tries_size)
		print "%s%-20s:%08x:%10d"%(prefix,"insns",self.insns,self.insns)
		print "%s%-20s:%08x:%10d"%(prefix,"tries",self.tries,self.tries)
		print "%s%-20s:%08x:%10d"%(prefix,"handlers",self.handlers,self.handlers)
		parse_instruction(dex_object.m_content[self.insns:self.insns+self.insns_size*2],self.insns,dex_object)
class tryitem:
	start_addr = 0
	ins_count = 0
	handlerlist_offset = 0
	handler_off = 0
	handlercount = 0
	handlerlist = []
	def __init__(self, dex_object, content, handlerlist_offset,offset):
		format = "H"
		tempoffset=0
		self.handlerlist=[]
		self.handlerlist_offset = handlerlist_offset
		self.start_addr, = struct.unpack_from("i", content, offset)
		offset += struct.calcsize("i")
		self.ins_count, = struct.unpack_from(format, content, offset)
		offset += struct.calcsize(format)
		self.handler_off, = struct.unpack_from(format, content, offset)
		i,self.handlercount = get_leb128(content[self.handler_off+self.handlerlist_offset:])
		if(self.handlercount<=0):
			self.handlercount=0-self.handlercount
		tempoffset=self.handlerlist_offset+self.handler_off+i
		if self.handlercount==0:
			#print "this is a finally handler"
			i,handler_address=get_uleb128(content[tempoffset:])
			temphandler=handler(0,"finally",handler_address)
			self.handlerlist.append(temphandler)
		else:
			#print "this is not a finally handler"
			for j in range(0,self.handlercount):
				i,handler_typeidx=get_uleb128(content[tempoffset:])
				tempoffset=tempoffset+i
				type_str=dex_object.gettypenamebyid(handler_typeidx)
				i,handler_address=get_uleb128(content[tempoffset:])
				tempoffset=tempoffset+i
				temphandler = handler(handler_typeidx, type_str, handler_address)
				self.handlerlist.append(temphandler)

class handler:
	type_idx = 0
	type_str=""
	ins_start = 0

	def __init__(self, type_idx, type_str, ins_start):
		self.type_idx=type_idx
		self.ins_start=ins_start
		self.type_str=type_str
class repired_method_code:
	dex_obj=None
	content = ""
	trylist = []
	def __init__(self, dex_obj,content):
		offset=0
		format = "H"
		self.dex_obj=dex_obj
		self.content=content
		self.registers_size, = struct.unpack_from(format, content, offset)
		offset += struct.calcsize(format)
		self.ins_size, = struct.unpack_from(format, content, offset)
		offset += struct.calcsize(format)
		self.outs_size, = struct.unpack_from(format, content, offset)
		offset += struct.calcsize(format)
		self.tries_size, = struct.unpack_from(format, content, offset)
		offset += struct.calcsize(format)
		format = "I"
		self.debug_info_off, = struct.unpack_from(format, content, offset)
		offset += struct.calcsize(format)
		self.insns_size, = struct.unpack_from(format, content, offset)
		offset += struct.calcsize(format)
		self.insns = offset
		offset += 2 * self.insns_size
		if self.insns_size % 2 == 1:
			offset += 2
		if self.tries_size == 0:
			self.tries = 0
			self.handlers = 0
		else:
			self.handlerlist_offset = offset + 8 * self.tries_size
			self.tries = offset
			for i in range(0, self.tries_size):
				temptryitem = tryitem(self.dex_obj,content, self.handlerlist_offset, offset + 8 * i)
				self.trylist.append(temptryitem)
			self.handlers = offset + self.tries_size * struct.calcsize("I2H")  #

	def printf(self, dex_object, prefix=""):
		print "%s%-20s:%08x:%10d" % (prefix, "registers_size", self.registers_size, self.registers_size)
		print "%s%-20s:%08x:%10d" % (prefix, "insns_size", self.insns_size, self.insns_size)
		print "%s%-20s:%08x:%10d" % (prefix, "debug_info_off", self.debug_info_off, self.debug_info_off)
		print "%s%-20s:%08x:%10d" % (prefix, "ins_size", self.ins_size, self.ins_size)
		print "%s%-20s:%08x:%10d" % (prefix, "outs_size", self.outs_size, self.outs_size)
		print "%s%-20s:%08x:%10d" % (prefix, "tries_size", self.tries_size, self.tries_size)
		if self.tries_size > 0:
			for i in range(0, self.tries_size):
				tryitem = self.trylist[i]
				print "%s%-20s:%08x:%10d" % (
					prefix, "try[" + str(i) + "] ins start:", tryitem.start_addr, tryitem.start_addr)
				print "%s%-20s:%08x:%10d" % (
					prefix, "try[" + str(i) + "] ins count:", tryitem.ins_count, tryitem.ins_count)
				for j in range(len(tryitem.handlerlist)):
					temphandler=tryitem.handlerlist[j]
					print "%s%-20s:%s" % (
						prefix, "try["+str(i)+"]:handler[" + str(j) + "] exception type:", temphandler.type_str)
					print "%s%-20s:%08x:%10d" % (
						prefix, "try["+str(i)+"]:handler[" + str(j) + "] ins start:", temphandler.ins_start, temphandler.ins_start)
		# print "%s%-20s:%08x:%10d" % (prefix, "insnsoffset", self.insns, self.insns)
		# print "%s%-20s:%08x:%10d" % (prefix, "triesoffset", self.tries, self.tries)
		parse_instruction(self.content[self.insns:self.insns + self.insns_size * 2], self.insns, dex_object)
class dex_encode_method:
	def __init__(self,idx,flags,code_off,dex_object):
		self.m_method_idx_diff = idx
		self.m_access_flags = flags
		self.m_code_off = code_off
		if code_off:
			self.m_code_item = method_code(dex_object,code_off)#dex_object.m_content[code_off:])
	def printf(self,dex_object):
		name = dex_object.gettypenamebyid(self.m_method_idx_diff)
		print "%-20s%08x %s"%("m_method_idx_diff",self.m_method_idx_diff,name)	
		flags = dex_object.get_access_flags(self.m_access_flags)
		print "%-20s%08x %s"%("access_flags",self.m_access_flags,flags)	
		print "%-20s%08x %d"%("code_off",self.m_code_off,self.m_code_off)	
		if self.m_code_off !=0:
			self.m_code_item.printf(dex_object)
	def printf_l(self,dex_object,is_virtual):
		flags = dex_object.get_access_flags(self.m_access_flags)
		if is_virtual:
			flags += " virtual"
		print "%48s"%flags,
		dex_object.MethodId_list[self.m_method_idx_diff].printf(dex_object)
		if self.m_code_off!=0:	
			self.m_code_item.printf(dex_object)
class dex_class:
	def __init__(self,dex_object,classid):
		if classid >= dex_object.m_classDefSize:
			return ""
		offset = dex_object.m_classDefOffset + classid * struct.calcsize("8I")
		self.offset = offset
		format = "I"
		self.thisClass,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.modifiers,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.superClass,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.interfacesOff,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.sourceFileIdx,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.annotationsOff,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.classDataOff,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.staticValuesOff,=struct.unpack_from(format,dex_object.m_content,offset)
		offset += struct.calcsize(format)
		self.index = classid
		self.interfacesSize = 0
		if self.interfacesOff != 0:
			self.interfacesSize, = struct.unpack_from("I",dex_object.m_content,self.interfacesOff)
		if self.classDataOff != 0:
			offset = self.classDataOff
			count,self.numStaticFields = get_uleb128(dex_object.m_content[offset:])
			offset += count
			count,self.numInstanceFields = get_uleb128(dex_object.m_content[offset:])
			offset += count
			count,self.numDirectMethods = get_uleb128(dex_object.m_content[offset:])
			offset += count
			count,self.numVirtualMethods = get_uleb128(dex_object.m_content[offset:])	
		else:
			self.numStaticFields = 0
			self.numInstanceFields = 0
			self.numDirectMethods = 0
			self.numVirtualMethods = 0
	def format_classname(self,name):
		name = name[1:-1].replace("/","_")
		name = name.replace("$","_")
		return name
	def create_header_file_for_cplusplus(self,dex_object):
		typelist = []
		name = self.format_classname(dex_object.gettypename(self.thisClass))
		f = open(name+".h","w")
		str1 =  "class %s"%name
		supername = dex_object.gettypename(self.superClass)

		if dex_object.m_class_name_id.has_key(supername) :
			str1 += " : "
			supername = dex_object.gettypename(self.superClass)
			str1 += self.format_classname(supername)
		str1 += "\n{\n"
		offset = self.classDataOff
		n,tmp = get_uleb128(dex_object.m_content[offset:offset+5])
		offset += n
		n,tmp = get_uleb128(dex_object.m_content[offset:offset+5])
		offset += n
		n,tmp = get_uleb128(dex_object.m_content[offset:offset+5])
		offset += n
		n,tmp = get_uleb128(dex_object.m_content[offset:offset+5])
		offset += n
		field_idx=0
		prev_access = -1
		for i in xrange(0,self.numStaticFields):
			n,field_idx_diff = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			field_idx+=field_idx_diff

			n,modifiers = get_uleb128(dex_object.m_content[offset:offset+5])
			
			access_str,cur_access = dex_object.get_access_flags1(modifiers)		
			if cur_access != prev_access:
				str1 += access_str
				str1 += "\n"
				prev_access = cur_access
			str1 += "\tconst "
			str1 += dex_object.getfieldfullname1(field_idx)
			if field_idx not in typelist:
				typelist.append(field_idx)
			offset += n		
			if self.staticValuesOff:
				str1 += " = "
				staticoffset=get_static_offset(dex_object.m_content[self.staticValuesOff:],i)
				if staticoffset == -1:
					str1 += "0;\n"
					continue
				size,str2 = parse_encoded_value1(dex_object,dex_object.m_content[self.staticValuesOff+staticoffset:])
				str1 += str2
			str1 += ";\n"	
		field_idx=0
		str1+="////////////////////////////////////////////////////////\n"
		for i in xrange(0,self.numInstanceFields):
			n,field_idx_diff = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			field_idx+=field_idx_diff
			n,modifiers = get_uleb128(dex_object.m_content[offset:offset+5])
			access_str,cur_access = dex_object.get_access_flags1(modifiers)		
			if cur_access != prev_access:
				str1 += access_str
				str1 += "\n"
				prev_access = cur_access
			str1 += "\t"
			str1 += dex_object.getfieldfullname1(field_idx)
			if field_idx not in typelist:
				typelist.append(field_idx)
			str1 += ";\n"	
			offset += n			
		#print str1
		method_idx = 0
		prev_access = -1
		for i in xrange(0,self.numDirectMethods):	
			n,method_idx_diff = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			n,access_flags = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			n,code_off = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			method_idx += method_idx_diff
			access_str,cur_access = dex_object.get_access_flags1(access_flags)		
			if cur_access != prev_access:
				str1 += access_str
				str1 += "\n"
				prev_access = cur_access			
			str1 += "\t"
			parameter_list=[]
			if code_off != 0:
				parameter_list = method_code(dex_object,code_off).get_param_list(dex_object)
			str1 += dex_object.getmethodfullname1(method_idx,parameter_list,True)
			#print "%s           codeoff=%x"%(dex_object.getmethodname(method_idx),code_off)
			str1 += ";\n"
		method_idx = 0
		str1+="//////////////////////virtual method//////////////////////////////////\n"
		for i in xrange(0,self.numVirtualMethods):			
			n,method_idx_diff = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			n,access_flags = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			n,code_off = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			method_idx += method_idx_diff
			access_str,cur_access = dex_object.get_access_flags1(access_flags)		
			if cur_access != prev_access:
				str1 += access_str
				str1 += "\n"
				prev_access = cur_access			
			str1 +="\tvirtual "
			parameter_list=[]
			if code_off != 0:
				parameter_list = method_code(dex_object,code_off).get_param_list(dex_object)
			str1 += dex_object.getmethodfullname1(method_idx,parameter_list,True)							
			str1 += ";\n"
		str1 += "}"
		#print str1
		f.write(str1)
		f.close()
		return typelist
	def printf(self,dex_object):
		print "%-20s:%08x:%10d  %s"%("thisClass",self.thisClass,self.thisClass,dex_object.gettypename(self.thisClass))
		print "%-20s:%08x:%10d  %s"%("superClass",self.superClass,self.superClass,dex_object.gettypename(self.superClass))
		print "%-20s:%08x:%10d"%("modifiers",self.modifiers,self.modifiers)
		print "%-20s:%08x:%10d"%("offset",self.offset,self.offset)
		print "%-20s:%08x:%10d"%("annotationsOff",self.annotationsOff,self.annotationsOff)
		print "%-20s:%08x:%10d"%("numStaticFields",self.numStaticFields,self.numStaticFields)
		print "%-20s:%08x:%10d"%("numInstanceFields",self.numInstanceFields,self.numInstanceFields)
		print "%-20s:%08x:%10d"%("numDirectMethods",self.numDirectMethods,self.numDirectMethods)
		print "%-20s:%08x:%10d"%("numVirtualMethods",self.numVirtualMethods,self.numVirtualMethods)
		print "%-20s:%08x:%10d"%("classDataOff",self.classDataOff,self.classDataOff)
		print "%-20s:%08x:%10d"%("interfacesOff",self.interfacesOff,self.interfacesOff)
		print "%-20s:%08x:%10d"%("interfacesSize",self.interfacesSize,self.interfacesSize)
		offset = self.interfacesOff + struct.calcsize("I")
		for n in xrange(0,self.interfacesSize):
			typeid, = struct.unpack_from("H",dex_object.m_content,offset)
			offset += struct.calcsize("H")
			print "\t\t"+ dex_object.gettypename(typeid)

		print "%-20s:%08x:%10d"%("staticValuesOff",self.staticValuesOff,self.staticValuesOff)
		print "%-20s:%08x:%10d  %s"%("sourceFileIdx",self.sourceFileIdx,self.sourceFileIdx,dex_object.getstringbyid(self.sourceFileIdx))
		offset = self.classDataOff
		n,tmp = get_uleb128(dex_object.m_content[offset:offset+5])
		offset += n
		n,tmp = get_uleb128(dex_object.m_content[offset:offset+5])
		offset += n
		n,tmp = get_uleb128(dex_object.m_content[offset:offset+5])
		offset += n
		n,tmp = get_uleb128(dex_object.m_content[offset:offset+5])
		offset += n
		field_idx=0
		for i in xrange(0,self.numStaticFields):
			n,field_idx_diff = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			field_idx+=field_idx_diff
			print dex_object.getfieldfullname(field_idx),
			n,modifiers = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			if self.staticValuesOff:
				staticoffset=get_static_offset(dex_object.m_content[self.staticValuesOff:],i)
				if staticoffset == -1:
					print "0;"
					continue
				parse_encoded_value(dex_object,dex_object.m_content[self.staticValuesOff+staticoffset:])
			print ""

		field_idx=0
		for i in xrange(0,self.numInstanceFields):
			n,field_idx_diff = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			field_idx+=field_idx_diff
			print dex_object.getfieldfullname(field_idx)
			n,modifiers = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n		

		print "=========numDirectMethods[%d]=numVirtualMethods[%d]=numStaticMethods[0]========="%(self.numDirectMethods,self.numVirtualMethods)
		method_idx = 0
		for i in xrange(0,self.numDirectMethods):	
			n,method_idx_diff = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			n,access_flags = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			n,code_off = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			method_idx += method_idx_diff
			if code_off != 0:
				methodname=dex_object.getmethodfullname(method_idx,True).replace("::",".").replace(" ","")
				method=None
				try:
					method = methodTable[method_idx]
				except Exception as e:
					pass
				if method != None:
					print "\nDirectMethod:" + dex_object.getmethodfullname(method_idx, True) + "\n"
					try:
						print "before repire method+++++++++++++++++++++++++++++++++++\n"
						method_code(dex_object, code_off).printf(dex_object, "\t\t")
					except Exception as e:
						print e
					try:
						bytearray_str = base64.b64decode(method.insarray)
						print "after repire method++++++++++++++++++++++++++++++++++++\n"
						repired_method_code(dex_object, bytearray_str).printf(dex_object, "\t\t")
					except Exception as e:
						print e

		method_idx = 0
		for i in xrange(0,self.numVirtualMethods):			
			n,method_idx_diff = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			n,access_flags = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			n,code_off = get_uleb128(dex_object.m_content[offset:offset+5])
			offset += n
			method_idx += method_idx_diff
			if code_off != 0:
				methodname = dex_object.getmethodfullname(method_idx, True).replace("::", ".").replace(" ", "")
				method = None
				try:
					method = methodTable[method_idx]
				except Exception as e:
					pass
				if method != None:
					print "\nVirtualMethod:" + dex_object.getmethodfullname(method_idx, True) + "\n"
					try:
						print "before repire method+++++++++++++++++++++++++++++++++++\n"
						method_code(dex_object, code_off).printf(dex_object, "\t\t")
					except Exception as e:
						print e
					try:
						bytearray_str = base64.b64decode(method.insarray)
						print "after repire method++++++++++++++++++++++++++++++++++++\n"
						repired_method_code(dex_object, bytearray_str).printf(dex_object, "\t\t")
					except Exception as e:
						print e
		print "================================================================================"
		if self.annotationsOff != 0:
			offset = self.annotationsOff
			self.class_annotations_off,self.fields_size,self.annotated_methods_size,self.annotated_parameters_size,=struct.unpack_from("4I",dex_object.m_content,offset)
			#print "%-30s:%08x:%09d"%("class_annotations_off",self.class_annotations_off,self.class_annotations_off)
			#print "%-30s:%08x:%09d"%("fields_size",self.fields_size,self.fields_size)
			#print "%-30s:%08x:%09d"%("annotated_methods_size",self.annotated_methods_size,self.annotated_methods_size)
			#print "%-30s:%08x:%09d"%("annotated_parameters_size",self.annotated_parameters_size,self.annotated_parameters_size)
			offset =  self.annotationsOff + struct.calcsize("4I")
			
			if self.fields_size:
				for  i in xrange(0,self.fields_size):
					field_idx,annotations_off,=struct.unpack_from("2I",dex_object.m_content,offset)
					offset += struct.calcsize("2I")
					print dex_object.getfieldname(field_idx),
					parse_annotation_set_item(dex_object,annotations_off)
			
			if self.annotated_methods_size:
				print "=====annotated_methods_size=====    offset=[%x]===="%offset
				for  i in xrange(0,self.annotated_methods_size):
					method_idx,annotations_off,=struct.unpack_from("2I",dex_object.m_content,offset)
					offset += struct.calcsize("2I")
					print dex_object.getmethodname(method_idx),
					parse_annotation_set_item(dex_object,annotations_off)
			if self.annotated_parameters_size:
				for  i in xrange(0,self.annotated_parameters_size):
					method_idx,annotations_off,=struct.unpack_from("2I",dex_object.m_content,offset)
					offset+=struct.calcsize("2I")
					print dex_object.getmethodname(method_idx),
					parse_annotation_set_ref_list(dex_object,annotations_off)
			if self.class_annotations_off == 0:
				return
			print "self.class_annotations_off = %x"%self.class_annotations_off
			parse_annotation_set_item(dex_object,self.class_annotations_off)

	def repiredex(self, dex_object):
		# if dex_object.gettypename(self.thisClass)!="Landroid/Manifest$permission;":
		#	return
		print "%-20s:%08x:%10d  %s" % (
		"thisClass", self.thisClass, self.thisClass, dex_object.gettypename(self.thisClass))
		print "%-20s:%08x:%10d  %s" % (
		"superClass", self.superClass, self.superClass, dex_object.gettypename(self.superClass))
		print "%-20s:%08x:%10d" % ("modifiers", self.modifiers, self.modifiers)
		print "%-20s:%08x:%10d" % ("offset", self.offset, self.offset)
		print "%-20s:%08x:%10d" % ("annotationsOff", self.annotationsOff, self.annotationsOff)
		print "%-20s:%08x:%10d" % ("numStaticFields", self.numStaticFields, self.numStaticFields)
		print "%-20s:%08x:%10d" % ("numInstanceFields", self.numInstanceFields, self.numInstanceFields)
		print "%-20s:%08x:%10d" % ("numDirectMethods", self.numDirectMethods, self.numDirectMethods)
		print "%-20s:%08x:%10d" % ("numVirtualMethods", self.numVirtualMethods, self.numVirtualMethods)
		print "%-20s:%08x:%10d" % ("classDataOff", self.classDataOff, self.classDataOff)
		print "%-20s:%08x:%10d" % ("interfacesOff", self.interfacesOff, self.interfacesOff)
		print "%-20s:%08x:%10d" % ("interfacesSize", self.interfacesSize, self.interfacesSize)
		offset = self.interfacesOff + struct.calcsize("I")
		for n in xrange(0, self.interfacesSize):
			typeid, = struct.unpack_from("H", dex_object.m_content, offset)
			offset += struct.calcsize("H")
			print "\t\t" + dex_object.gettypename(typeid)

		print "%-20s:%08x:%10d" % ("staticValuesOff", self.staticValuesOff, self.staticValuesOff)
		print "%-20s:%08x:%10d  %s" % (
		"sourceFileIdx", self.sourceFileIdx, self.sourceFileIdx, dex_object.getstringbyid(self.sourceFileIdx))
		offset = self.classDataOff
		n, tmp = get_uleb128(dex_object.m_content[offset:offset + 5])
		offset += n
		n, tmp = get_uleb128(dex_object.m_content[offset:offset + 5])
		offset += n
		n, tmp = get_uleb128(dex_object.m_content[offset:offset + 5])
		offset += n
		n, tmp = get_uleb128(dex_object.m_content[offset:offset + 5])
		offset += n
		field_idx = 0
		for i in xrange(0, self.numStaticFields):
			n, field_idx_diff = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			field_idx += field_idx_diff
			print dex_object.getfieldfullname(field_idx),
			n, modifiers = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			if self.staticValuesOff:
				staticoffset = get_static_offset(dex_object.m_content[self.staticValuesOff:], i)
				if staticoffset == -1:
					print "0;"
					continue
				parse_encoded_value(dex_object, dex_object.m_content[self.staticValuesOff + staticoffset:])
			print ""

		field_idx = 0
		for i in xrange(0, self.numInstanceFields):
			n, field_idx_diff = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			field_idx += field_idx_diff
			print dex_object.getfieldfullname(field_idx)
			n, modifiers = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n

		print "=========numDirectMethods[%d]=numVirtualMethods[%d]=numStaticMethods[0]=========" % (
		self.numDirectMethods, self.numVirtualMethods)
		method_idx = 0
		for i in xrange(0, self.numDirectMethods):
			n, method_idx_diff = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			n, access_flags = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			n, code_off = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			method_idx += method_idx_diff
			print dex_object.getmethodfullname(method_idx, True)
			# print "%s           codeoff=%x"%(dex_object.getmethodname(method_idx),code_off)
			if code_off != 0:
				method_code(dex_object, code_off).printf(dex_object, "\t\t")
		method_idx = 0
		for i in xrange(0, self.numVirtualMethods):
			n, method_idx_diff = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			n, access_flags = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			n, code_off = get_uleb128(dex_object.m_content[offset:offset + 5])
			offset += n
			method_idx += method_idx_diff
			print dex_object.getmethodfullname(method_idx, True)
			# print "%s           codeoff=%x"%(dex_object.getmethodname(method_idx),code_off)
			if code_off != 0:
				method_code(dex_object, code_off).printf(dex_object, "\t\t")

		print "================================================================================"
		if self.annotationsOff != 0:
			offset = self.annotationsOff
			self.class_annotations_off, self.fields_size, self.annotated_methods_size, self.annotated_parameters_size, = struct.unpack_from(
				"4I", dex_object.m_content, offset)
			# print "%-30s:%08x:%09d"%("class_annotations_off",self.class_annotations_off,self.class_annotations_off)
			# print "%-30s:%08x:%09d"%("fields_size",self.fields_size,self.fields_size)
			# print "%-30s:%08x:%09d"%("annotated_methods_size",self.annotated_methods_size,self.annotated_methods_size)
			# print "%-30s:%08x:%09d"%("annotated_parameters_size",self.annotated_parameters_size,self.annotated_parameters_size)
			offset = self.annotationsOff + struct.calcsize("4I")

			if self.fields_size:
				for i in xrange(0, self.fields_size):
					field_idx, annotations_off, = struct.unpack_from("2I", dex_object.m_content, offset)
					offset += struct.calcsize("2I")
					print dex_object.getfieldname(field_idx),
					parse_annotation_set_item(dex_object, annotations_off)

			if self.annotated_methods_size:
				print "=====annotated_methods_size=====    offset=[%x]====" % offset
				for i in xrange(0, self.annotated_methods_size):
					method_idx, annotations_off, = struct.unpack_from("2I", dex_object.m_content, offset)
					offset += struct.calcsize("2I")
					print dex_object.getmethodname(method_idx),
					parse_annotation_set_item(dex_object, annotations_off)
			if self.annotated_parameters_size:
				for i in xrange(0, self.annotated_parameters_size):
					method_idx, annotations_off, = struct.unpack_from("2I", dex_object.m_content, offset)
					offset += struct.calcsize("2I")
					print dex_object.getmethodname(method_idx),
					parse_annotation_set_ref_list(dex_object, annotations_off)
			if self.class_annotations_off == 0:
				return
			print "self.class_annotations_off = %x" % self.class_annotations_off
			parse_annotation_set_item(dex_object, self.class_annotations_off)
def get_static_offset(content,index):
	offset = 0
	m,size =  get_uleb128(content[offset:offset+5])
	if index >= size:
		return -1
	offset += m
	for i in xrange(0,index):
		offset += get_encoded_value_size(content[offset:])
	return offset
def get_encoded_value_size(content):
	offset = 0
	arg_type, = struct.unpack_from("B",content,offset)
	offset+=struct.calcsize("B")
	value_arg = arg_type>>5
	value_type = arg_type &0x1f
	if value_type in [0x2,3,4,6,0x10,0x11,0x17,0x18,0x19,0x1a,0x1b]:
		offset += (value_arg+1)
	elif value_type == 0:
		offset += 1
	elif value_type == 0x1e or value_type == 0x1f:
		offset += 0
	elif value_type == 0x1d:
		offset += get_encoded_annotation_size(content[offset:])
	elif value_type == 0x1c:
		m,asize = get_uleb128(m_content[offset:offset+5])
		offset += m
		for q in xrange(0,asize):
			offset += get_encoded_value_size(content[offset:])
	else:
		print "***************error parse encode_value**************"
	return offset
class field_annotation:
	def __init__(self,content):
		self.field_idx,self.annotations_off, = struct.unpack_from("2I",content)
class annotations_directory_item:
	def __init__(self,content,dex_object):
		self.class_annotations_off,self.fields_size,self.annotated_methods_size,self.annotated_parameters_size , =struct.unpack_from("4I",content)
		self.m_fields_list = []
		self.m_methods_list = []
		self.m_parameters_list = []
		offset = struct.calcsize("4I")
		if self.fields_size:
			self.m_fields_list = array.array("L")
			self.m_fields_list.fromstring(content[offset:offset+8*self.fields_size])
		offset = offset+4*self.fields_size
		if self.annotated_methods_size:
			self.m_methods_list = array.array("L")
			self.m_methods_list.fromstring(content[offset:offset+8*self.annotated_methods_size])
		offset = offset + 4*self.annotated_methods_size
		for i in xrange(0,annotated_methods_size):
			self.m_parameters_list = array.array("L")
			self.m_parameters_list.fromstring(content[offset:offset+8*self.annotated_parameters_size])
		content = dex_object.m_content
		for i in xrange(0,self.fields_size):
			size = self.m_fields_list[i*2]						
			offset = self.m_fields_list[i*2+1]
			of = array.array("L")
			of.fromstring(content[offset:offset+4*size])
			for off in of:
				visibility = content[off]
				off += 1
				k,type_idx = get_uleb128(content[off:])
				off += k
				k,size = get_uleb128(content[off:])
				for m in xrange(0,size):
					off += k
					k,name_idx=get_uleb128(content[off:])
					off += k
					get_encoded_value(content[off:])
def parse_debug_info_method_parameter_list(dex_object,offset):
	parameter_list = []
	n ,current_line = get_uleb128(dex_object.m_content[offset:offset+5])
	offset += n
	n,parameters_size = get_uleb128(dex_object.m_content[offset:offset+5])
	offset += n
	for i in xrange(0,parameters_size):
		n,string_idx = get_uleb128p1(dex_object.m_content[offset:offset+5])
		if string_idx!=-1:
			parameter_list.append(dex_object.getstringbyid(string_idx))
		offset+=n
	return 	parameter_list
def parse_debug_info(lex_object,offset):
	print "===parse_debug_info====offset = %08x"%offset
	n ,current_line = get_uleb128(lex_object.m_content[offset:offset+5])
	offset += n
	n,parameters_size = get_uleb128(lex_object.m_content[offset:offset+5])
	offset += n
	for i in xrange(0,parameters_size):
		n,string_idx = get_uleb128p1(lex_object.m_content[offset:offset+5])
		if string_idx!=-1:
			print lex_object.getstringbyid(string_idx)
		offset+=n
	start = offset
	current_pc = 0
	print "===opcode====offset = %08x  line=%d pc=%d"%(offset,current_line,current_pc)


	totalsize = len(lex_object.m_content)
	while offset < totalsize:
		#bytecode = struct.unpack_from("B",lex_object.m_content,offset)
		bytecode = ord(lex_object.m_content[offset])
		offset += 1
		print "opcode[%02x]"%bytecode,
		if bytecode == 0:
			print ""
			break
		elif bytecode == 1:
			n,val = get_uleb128(lex_object.m_content[offset:offset+5])
			current_pc += val;
			offset += n
			print "line=%d  pc=%x"%(current_line,current_pc)
		elif bytecode == 2:
			n,val = get_leb128(lex_object.m_content[offset:offset+5])
			
			current_line += val       
			offset += n
			print "line=%d  pc=%x   val=%08x(%d)"%(current_line,current_pc,val,val)
		elif bytecode == 3:
			n,register_num = get_uleb128(lex_object.m_content[offset:offset+5])
			offset += n
			n,name_idx = get_uleb128p1(lex_object.m_content[offset:offset+5])
			offset += n
			n,type_idx = get_uleb128p1(lex_object.m_content[offset:offset+5])
			offset += n
			print "v%d %s %s  START_LOCAL"%(register_num,lex_object.gettypenamebyid(type_idx),lex_object.getstringbyid(name_idx))
		elif bytecode == 4:
			n,register_num = get_uleb128(lex_object.m_content[offset:offset+5])
			offset += n
			n,name_idx = get_uleb128p1(lex_object.m_content[offset:offset+5])
			offset += n
			n,type_idx = get_uleb128p1(lex_object.m_content[offset:offset+5])
			offset += n
			n,sig_idx = get_uleb128p1(lex_object.m_content[offset:offset+5])
			offset += n
			print "v%d %s %s   START_LOCAL_EXTENDED"%(register_num,lex_object.gettypenamebyid(type_idx),lex_object.getstringbyid(name_idx))
		elif bytecode == 5:
			n,register_num = get_uleb128(lex_object.m_content[offset:offset+5])
			offset += n
			print "v%d  END_LOCAL"%register_num
		elif bytecode == 6:
			n,register_num = get_uleb128(lex_object.m_content[offset:offset+5])
			offset += n
			print "v%d   register to restart"%register_num
		elif bytecode == 7:
			print "SET_PROLOGUE_END"
			pass
		elif bytecode == 8:
			print "SET_EPILOGUE_BEGIN"
			pass
		elif bytecode == 9:
			n,name_idx = get_uleb128(lex_object.m_content[offset:offset+5])
			print "%s"%lex_object.getstringbyid(name_idx)
			offset += n
		else:
			adjusted_opcode = bytecode - 0xa
			current_line +=  (adjusted_opcode % 15)-4
			current_pc += (adjusted_opcode / 15)
			#offset += 1
			print "line=%d  pc=%x  adjusted_opcode=%d  pc+ %d  line+%d"%(current_line,current_pc,adjusted_opcode,(adjusted_opcode/15),(adjusted_opcode%15)-4)
	print "===parse_debug_info====offset = %08x$"%offset
def get_encoded_value(content):
	VALUE_SHORT = 0x2
	VALUE_CHAR = 0x3
	VALUE_INT = 0x4
	VALUE_LONG = 0x6
	VALUE_FLOAT = 0x10
	VALUE_DOUBLE = 0x11
	VALUE_STRING = 0x17
	VALUE_TYPE = 0x18
	VALUE_FIELD = 0x19
	VALUE_METHOD = 0x1a
	VALUE_ENUM = 0x1b
	VALUE_ARRAY = 0x1c
	VALUE_ANNOTATION = 0x1d
	VALUE_NULL = 0x1e
	VALUE_BOOLEAN = 0x1f
	type_enum = [0x0,0x2,0x3,0x4,0x6,0x10,0x11,0x17,0x18,0x19,0x1a,0x1b,0x1c,0x1d,0x1e,0x1f]
	size_type = ord(content[0])
	usebyte = 1
	
	size = size_type >> 5
	type = size_type & 0x1f
	if type not in size_type:
		print "encoded value error!"
	if type == 0 and size == 0:
		value,=struct.unpack_from("b",content,1)
		usebyte += 1

	elif type == VALUE_SHORT:
		if size == 0:
			value,=struct.unpack_from("b",content,1)
		elif size == 1:
			value,=struct.unpack_from("h",content,1)
		else:
			print "encoded value error! type=short type=%d size=%d"%(type,size)
		usebyte+=size+1
	elif type == VALUE_CHAR:
		if size == 0:
			value, = struct.unpack_from("B",content,1)
		elif size == 1:
			value, = struct.unpack_from("H",content,1)
		else:
			print "encoded value error! type=char type=%d size=%d"%(type,size)
		usebyte+=size+1
	elif type == VALUE_INT:
		if size == 0:
			value,=struct.unpack_from("b",content,1)
		elif size == 1:
			value,=struct.unpack_from("h",content,1)
		elif size == 2:
			value = 0
		elif size == 3:
			value,=struct.unpack_from("i",content,1)
		else:
			print "encoded value error! type=int type=%d size=%d"%(type,size)
		usebyte+=size+1
	
	elif type == VALUE_LONG:
		if size > 7:
			print "encoded value error! type=long type=%d size=%d"%(type,size)
		value=content[1:1+size+1]
		usebyte+=size+1
	elif type == VALUE_FLOAT:
		if size > 3:
			print "encoded value error! type=float type=%d size=%d"%(type,size)
		value=content[1:1+size+1]
		usebyte+=size+1
	elif type == VALUE_DOUBLE:
		if size > 7:
			print "encoded value error! type=double type=%d size=%d"%(type,size)
		value = content[1:1+size+1]
		usebyte+=size+1
		
	elif type == VALUE_STRING:
		if size > 3:
			print "encoded value error! type=double type=%d size=%d"%(type,size)
		value = content[1:1+size+1]
		usebyte+=size+1
	elif type == VALUE_TYPE:
		if size > 3:
			print "encoded value error! type=type type=%d size=%d"%(type,size)
		value = content[1:1+size+1]
		usebyte+=size+1
		
	elif type == VALUE_FIELD:
		if size > 3:
			print "encoded value error! type=field type=%d size=%d"%(type,size)
		value = content[1:1+size+1]
		usebyte+=size+1
	elif type == VALUE_METHOD:
		if size > 3:
			print "encoded value error! type=medhod type=%d size=%d"%(type,size)
		value = content[1:1+size+1]
		usebyte+=size+1
	elif type == VALUE_ENUM:
		if size > 3:
			print "encoded value error! type=enum type=%d size=%d"%(type,size)
		value = content[1:1+size+1]
		usebyte+=size+1
	elif type == VALUE_ARRAY:
		if size != 0:
			print "encoded value error! type=encoded_array type=%d size=%d"%(type,size)
		k,value=get_encoded_array(content[1:1+size+1])
		usebyte+=k
	elif type == VALUE_ANNOTATION:
		if size != 0:
			print "encoded value error! type=encoded_annotation type=%d size=%d"%(type,size)
		k,type_idx = get_uleb128(content[1:])
		k1,s = get_uleb128(content[1+k:])
		k1 = 1+k+k1
		for n in xrange(0,s):
			k2,name_index = get_uleb128(content[k1:])
			k1+=k2
			k3,value = get_encoded_value(content[k1:])
			k1+=k3
		usebyte+=k1
	elif type == VALUE_NULL:
		if size != 0:
			print "encoded value error! type=NULL  type=%d size=%d"%(type,size)
		value="NULL"
	elif type == VALUE_BOOLEAN:
		value = size
	return usebyte,value
def get_encoded_array(content):
	offset,size = get_uleb128(content)
	userbyte = offset
	for i in xrange(0,size):
		off,value = get_encoded_value(content[offset:])
		offset += off
		userbyte += off
	return userbyte,value
def get_encoded_array_by_index(content,index):
	offset,size = get_uleb128(content)
	userbyte = offset
	for i in xrange(0,size):
		off,value = get_encoded_value(content[offset:])
		offset += off
		userbyte+=off
		if index == i:
			return userbyte,value
	return offset
class annotations_directory_item:
	def __init__(self,content):
		self.m_class_annotations_off,self.m_fields_size,self.m_annotated_methods_size,self.m_annotated_parameters_size,=struct.unpack_from("4I",content)
		pass
def shorty_decode(name):
	val = {"V":"void",
		"Z":"boolean",
		"B":"byte",
		"S":"short",
		"C":"char",
		"I":"int",
		"J":"long",
		"F":"float",
		"D":"double",
		"L":"L"
		}
	value = ""

	if name[-1] == ';':
		if name[0] == 'L':
			return name[1:-1].replace("/",".")
		if name[0]=='[':
			if name[1] == 'L':
				return name[2:-1].replace("/",".")+"[]"
			else:
				return name[1:-1].replace("/",".")+"[]"
	i = 0
	for ch in name:
		if val.has_key(ch):
			if i != 0:
				value += " | "
			value += val[ch]
			i += 1
	if '[' in name:
		value += "[]"
	return value
def get_encoded_value_size(content):
	offset = 0
	arg_type, = struct.unpack_from("B",content,offset)
	offset+=struct.calcsize("B")
	value_arg = arg_type>>5
	value_type = arg_type &0x1f
	if value_type in [0x2,3,4,6,0x10,0x11,0x17,0x18,0x19,0x1a,0x1b]:
		offset += (value_arg+1)
	elif value_type == 0:
		offset += 1
	elif value_type == 0x1e or value_type == 0x1f:
		offset += 0
	elif value_type == 0x1d:
		offset += get_encoded_annotation_size(content[offset:])
	elif value_type == 0x1c:
		m,asize = get_uleb128(m_content[offset:5+offset])
		offset += m
		for q in xrange(0,asize):
			offset += get_encoded_value_size(content[offset:])
	else:
		print "***************error parse encode_value**************"
	return offset
def get_encoded_annotation_size(content):
	offset = 0
	n ,type_idx = get_uleb128(content[offset:5+offset])
	offset += n
	n ,size = get_uleb128(content[offset:5+offset])
	offset += n
	for i in xrange(0,n):
		n ,name_idx = get_uleb128(content[offset:5+offset])
		offset += n
		offset += get_encoded_value_size(content[offset:])
	return offset
def parse_encoded_value(lex_object,content,is_root=False):
	offset = 0
	arg_type, = struct.unpack_from("B",content,offset)
	offset+=struct.calcsize("B")
	value_arg = arg_type>>5
	value_type = arg_type &0x1f
	if value_type in [0x2,3,4,6,0x10,0x11,0x17,0x18,0x19,0x1a,0x1b]:
		sum = 0
		for q in xrange(0,value_arg+1):
			mm = ord(content[offset+q])
			mm <<= 8*q
			sum|=mm
			#sum += ord(content[offset+q])
		if value_type == 0x17:
			print "string@%d"%sum,
			print lex_object.getstringbyid(sum),
		elif value_type == 0x18:
			print "type@%d"%sum,
			print lex_object.gettypename(sum),
		elif value_type == 0x19:
			print "field@%d"%sum,
			print lex_object.getfieldname(sum),
		elif value_type == 0x1a:
			print "method@%d"%sum,
			print lex_object.getmethodname(sum),
		else:
			str = ""
			for q in xrange(0,value_arg+1):
				str += "%02x "%(ord(content[offset+q]))
			print str,
		offset += (value_arg+1)
	elif value_type == 0:
		print "%02x"%ord(content[offset]),
		offset += 1

	elif value_type == 0x1e :
		print "NULL",
	elif value_type == 0x1f:
		if value_arg == 0:
			print "False",
		else:
			print "True",
		offset += 0
	elif value_type == 0x1d:
		offset += parse_encoded_annotation(lex_object,content[offset:])
	elif value_type == 0x1c:
		m,asize = get_uleb128(content[offset:5])
		offset += m
		print "[%d]"%asize,
		for q in xrange(0,asize):
			offset += parse_encoded_value(lex_object,content[offset:],False)
	else:
		print "***************error parse encode_value**************"
	return offset
def parse_encoded_value1(lex_object,content,is_root=False):
	str1 = ""
	offset = 0
	arg_type, = struct.unpack_from("B",content,offset)
	offset+=struct.calcsize("B")
	value_arg = arg_type>>5
	value_type = arg_type &0x1f
	if value_type in [0x2,3,4,6,0x10,0x11,0x17,0x18,0x19,0x1a,0x1b]:
		sum = 0
		for q in xrange(0,value_arg+1):
			mm = ord(content[offset+q])
			mm <<= 8*q
			sum|=mm
			#sum += ord(content[offset+q])
		if value_type == 0x17:
			str1 += "\""
			str1 += lex_object.getstringbyid(sum)
			str1 += "\""
		elif value_type == 0x18:
			print "type@%d"%sum,
			str1 += lex_object.gettypename(sum),
		elif value_type == 0x19:
			print "field@%d"%sum,
			str1 += lex_object.getfieldname(sum),
		elif value_type == 0x1a:
			print "method@%d"%sum,
			str1 += lex_object.getmethodname(sum),
		else:
			str2 = ""
			for q in xrange(0,value_arg+1):
				str2 += "%02x "%(ord(content[offset+q]))
			str1+= str2
		offset += (value_arg+1)
	elif value_type == 0:
		str1 += "%02x"%ord(content[offset])
		offset += 1

	elif value_type == 0x1e :
		str1 += "NULL"
	elif value_type == 0x1f:
		if value_arg == 0:
			str1 += "false"
		else:
			str1 += "true"
		offset += 0
	elif value_type == 0x1d:
		size ,text = parse_encoded_annotation1(lex_object,content[offset:])
		offset += size
		str1 += text
	elif value_type == 0x1c:
		m,asize = get_uleb128(content[offset:5])
		offset += m
		str1 += "[%d]"%asize
		for q in xrange(0,asize):
			size,text = parse_encoded_value1(lex_object,content[offset:],False)
			offset += size
			str1 += text
	else:
		str1 += "***************error parse encode_value**************"
	return offset,str1
def parse_encoded_value4441(lex_object,content,is_root=False):
	offset = 0
	arg_type, = struct.unpack_from("B",content,offset)
	offset+=struct.calcsize("B")
	value_arg = arg_type>>5
	value_type = arg_type &0x1f
	if value_type in [0x2,3,4,6,0x10,0x11,0x17,0x18,0x19,0x1a,0x1b]:
		str = ""
		for q in xrange(0,value_arg+1):
			str += "%02x "%(ord(content[offset+q]))
		print str,
		offset += (value_arg+1)
	elif value_type == 0:
		print "%02x"%ord(content[offset]),
		offset += 1

	elif value_type == 0x1e :
		print "NULL",
	elif value_type == 0x1f:
		if value_arg == 0:
			print "False",
		else:
			print "True",
		offset += 0
	elif value_type == 0x1d:
		offset += parse_encoded_annotation(lex_object,content[offset:])
	elif value_type == 0x1c:
		m,asize = get_uleb128(content[offset:5+offset])
		offset += m
		print "[%d]"%asize,
		for q in xrange(0,asize):
			offset += parse_encoded_value(lex_object,content[offset:],False)
	else:
		print "***************error parse encode_value**************"
	return offset
def parse_encoded_annotation1(lex_object,content,is_root=False):
	str1 = ""
	offset = 0
	n ,type_idx = get_uleb128(content[offset:5+offset])
	offset += n
	n ,size = get_uleb128(content[offset:5+offset])
	offset += n
	if is_root:
		str1 += lex_object.gettypenamebyid(type_idx)
	for i in xrange(0,size):
		n ,name_idx = get_uleb128(content[offset:5+offset])
		if i == 0 and is_root:
			str1 += lex_object.getstringbyid(name_idx)
		offset += n
		size,text = parse_encoded_value1(lex_object,content[offset:],is_root)
		offset += size
		str1 += text
	return offset, str1
def parse_encoded_annotation(lex_object,content,is_root=False):
	offset = 0
	n ,type_idx = get_uleb128(content[offset:5+offset])
	offset += n
	n ,size = get_uleb128(content[offset:5+offset])
	offset += n
	if is_root:
		print lex_object.gettypenamebyid(type_idx),
	for i in xrange(0,size):
		n ,name_idx = get_uleb128(content[offset:5+offset])
		if i == 0 and is_root:
			print lex_object.getstringbyid(name_idx),
		offset += n
		offset += parse_encoded_value(lex_object,content[offset:],is_root)
	return offset
def parse_annotation_set_item(lex_object,offset,is_root=False):
	try:
		size, = struct.unpack_from("I",lex_object.m_content,offset)
		offset += struct.calcsize("I")
		for i in xrange(0,size):
			off,=struct.unpack_from("I",lex_object.m_content,offset)
			visibility, = struct.unpack_from("B",lex_object.m_content,off)
			if visibility == 0:
				print "VISIBILITY_BUILD",
			elif visibility == 1:
				print "VISIBILITY_RUNTIME",
			elif visibility == 2:
				print "VISIBILITY_SYSTEM",
			else:
				print "visibility is unknow %02x"%visibility
			off += struct.calcsize("B")
			parse_encoded_annotation(lex_object,lex_object.m_content[off:],True)
			offset += struct.calcsize("I")
			print ""
	except Exception as e:
		print e
def parse_annotation_set_ref_list(lex_object,offset,is_root=False):
	size, = struct.unpack_from("I",lex_object.m_content,offset)
	offset += struct.calcsize("I")
	for i in xrange(0,size):
		off,=struct.unpack_from("I",lex_object.m_content,offset)
		parse_annotation_set_item(lex_object,off,True)
		offset += struct.calcsize("I")
def get_encoded_field(content):
	n , val1 = get_uleb128(content)
	n1 , val2 = get_uleb128(content[n:])
	return n + n1, val1, val2
def get_encoded_method(content):
	n , val1 = get_uleb128(content)
	n1 , val2 = get_uleb128(content[n:])
	n2 , val3 = get_uleb128(content[n+n1:])
	return n + n1 + n2, val1, val2, val3
class dex_parser:
	
	def __init__(self,filename):
		global DEX_MAGIC
		global DEX_OPT_MAGIC
		self.m_javaobject_id = 0
		self.m_filename = filename
		self.m_fd = open(filename,"rb")
		self.m_content = self.m_fd.read()
		self.m_fd.close()
		self.m_dex_optheader = None
		self.m_class_name_id = {}
		self.string_table = []
		if self.m_content[0:4] == DEX_OPT_MAGIC:
			self.init_optheader(self.m_content)
			self.init_header(self.m_content,0x40)
		elif self.m_content[0:4] == DEX_MAGIC:
			self.init_header(self.m_content,0)

		bOffset = self.m_stringIdsOff
		if self.m_stringIdsSize > 0:
			for i in xrange(0,self.m_stringIdsSize):
				offset, = struct.unpack_from("I",self.m_content,bOffset + i * 4)
				if i == 0:
					start = offset
				else:			
					skip, length = get_uleb128(self.m_content[start:start+5])
					self.string_table.append(self.m_content[start+skip:offset-1])
					start = offset
			for i in xrange(start,len(self.m_content)):
				if self.m_content[i]==chr(0):
					self.string_table.append(self.m_content[start+1:i])
					break
		for i in xrange(0,self.m_classDefSize):
			str1 = self.getclassname(i)
			self.m_class_name_id[str1] = i
		for i in xrange(0,self.m_classDefSize):
			str1 = self.getclassname(i)
			dex_class(self,i).printf(self)
			pass
			#self.getclass(i)
	def create_all_header(self):
		for i in xrange(0,self.m_classDefSize):
			str1 = self.getclassname(i)
			self.create_cpp_header(str1)	
	def create_cpp_header(self,classname="Landroid/app/Activity;"):
		if self.m_class_name_id.has_key(classname):
			classid= self.m_class_name_id[classname]
			field_list = dex_class(self,classid).create_header_file_for_cplusplus(self)
		pass
	def getstringbyid(self,stridx):
		if stridx >= self.m_stringIdsSize:
			return ""
		return self.string_table[stridx]
	
	def getmethodname(self,methodid):
		if methodid >= self.m_methodIdsSize:
			return ""
		offset = self.m_methodIdsOffset + methodid * struct.calcsize("HHI")
		class_idx,proto_idx,name_idx, = struct.unpack_from("HHI",self.m_content,offset)
		return self.string_table[name_idx]
	def getmethodfullname(self,methodid,hidden_classname=False):
		if methodid >= self.m_methodIdsSize:
			return ""
		offset = self.m_methodIdsOffset + methodid * struct.calcsize("HHI")
		class_idx,proto_idx,name_idx, = struct.unpack_from("HHI",self.m_content,offset)
		classname = self.gettypename(class_idx)
		classname = shorty_decode(classname)
		funcname = self.getstringbyid(name_idx)
		if not hidden_classname:
			classname = ""
		return self.getprotofullname(proto_idx,classname,funcname)
	def getmethodfullname1(self,methodid,parameter_list=[],hidden_classname=False):
		if methodid >= self.m_methodIdsSize:
			return ""
		offset = self.m_methodIdsOffset + methodid * struct.calcsize("HHI")
		class_idx,proto_idx,name_idx, = struct.unpack_from("HHI",self.m_content,offset)
		classname = self.gettypename(class_idx)
		classname = shorty_decode(classname)
		funcname = self.getstringbyid(name_idx)
		if not hidden_classname:
			classname = ""
		return self.getprotofullname1(proto_idx,classname,parameter_list,funcname)
	def getfieldname(self,fieldid):
		if fieldid >= self.m_fieldIdsSize:
			return ""
		offset = self.m_fieldIdsOffset + fieldid * struct.calcsize("HHI")
		class_idx,type_idx,name_idx, = struct.unpack_from("HHI",self.m_content,offset)
		return self.string_table[name_idx]
	def getfieldfullname1(self,fieldid):
		if fieldid >= self.m_fieldIdsSize:
			return ""
		offset = self.m_fieldIdsOffset + fieldid * struct.calcsize("HHI")
		class_idx,type_idx,name_idx, = struct.unpack_from("HHI",self.m_content,offset)		
		name = self.gettypename(type_idx)
		name = shorty_decode(name)
		index = name.rfind(".")
		fname = self.getstringbyid(name_idx)
		return "%s %s"%(name[index+1:],fname)	
	def getfieldfullname2(self,fieldid):
		if fieldid >= self.m_fieldIdsSize:
			return ""
		offset = self.m_fieldIdsOffset + fieldid * struct.calcsize("HHI")
		class_idx,type_idx,name_idx, = struct.unpack_from("HHI",self.m_content,offset)		
		typename = self.gettypename(type_idx)
		typename = shorty_decode(typename)
		fieldname = self.getstringbyid(name_idx)
		return typename,fieldname		
	def getfieldfullname(self,fieldid):
		if fieldid >= self.m_fieldIdsSize:
			return ""
		offset = self.m_fieldIdsOffset + fieldid * struct.calcsize("HHI")
		class_idx,type_idx,name_idx, = struct.unpack_from("HHI",self.m_content,offset)		
		name = self.gettypename(type_idx)
		name = shorty_decode(name)
		fname = self.getstringbyid(name_idx)
		return "%s %s"%(name,fname)
	def getfieldtypename(self,fieldid):
		if fieldid >= self.m_fieldIdsSize:
			return ""
		offset = self.m_fieldIdsOffset + fieldid * struct.calcsize("HHI")
		class_idx,type_idx,name_idx, = struct.unpack_from("HHI",self.m_content,offset)		
		name = self.gettypename(type_idx)
		if name[-1] != ";":
			name = shorty_decode(name) 
		return name

	def gettypename(self,typeid):
		if typeid >= self.m_typeIdsSize:
			return ""
		offset = self.m_typeIdsOffset + typeid * struct.calcsize("I")
		descriptor_idx, = struct.unpack_from("I",self.m_content,offset)
		return self.string_table[descriptor_idx]
	
	def getprotoname(self,protoid):
		if protoid >= self.m_protoIdsSize:
			return ""
		offset = self.m_protoIdsOffset + protoid * struct.calcsize("3I")
		shorty_idx,return_type_idx,parameters_off, = struct.unpack_from("3I",self.m_content,offset)
		return self.string_table[shorty_idx]
	def getprotofullname(self,protoid,classname,func_name):
		if protoid >= self.m_protoIdsSize:
			return ""
		offset = self.m_protoIdsOffset + protoid * struct.calcsize("3I")
		shorty_idx,return_type_idx,parameters_off, = struct.unpack_from("3I",self.m_content,offset)
		retname = self.gettypename(return_type_idx)
		retname = shorty_decode(retname)
		retstr =  retname+" " 
		if len(classname)==0:
			retstr += "%s("%func_name
		else:
			retstr +=  "%s::%s("%(classname,func_name)
		if parameters_off != 0:
			offset = parameters_off
			size, = struct.unpack_from("I",self.m_content,offset)
			offset += struct.calcsize("I")
			n = 0
			for i in xrange(0,size):
				type_idx, = struct.unpack_from("H",self.m_content,offset)
				offset += struct.calcsize("H")
				arg = self.gettypename(type_idx)
				arg = shorty_decode(arg)
				if n != 0:
					retstr += ","
				retstr+=arg
				n += 1
		retstr += ")"
		return retstr
	def getprotofullname1(self,protoid,classname,parameter_list,func_name):
		index = classname.rfind(".")
		classname = classname[index+1:]
		if protoid >= self.m_protoIdsSize:
			return ""
		offset = self.m_protoIdsOffset + protoid * struct.calcsize("3I")
		shorty_idx,return_type_idx,parameters_off, = struct.unpack_from("3I",self.m_content,offset)
		retname = self.gettypename(return_type_idx)
		retname = shorty_decode(retname)
		index = retname.rfind(".")
		retname = retname[index+1:]
		retstr =  retname+" " 
		#if len(classname)==0:
		retstr += "%s("%func_name
		#else:
		#	retstr +=  "%s::%s("%(classname,func_name)
		param_count = len(parameter_list)
		if parameters_off != 0:
			offset = parameters_off
			size, = struct.unpack_from("I",self.m_content,offset)
			offset += struct.calcsize("I")
			n = 0
			for i in xrange(0,size):
				type_idx, = struct.unpack_from("H",self.m_content,offset)
				offset += struct.calcsize("H")
				arg = self.gettypename(type_idx)
				arg = shorty_decode(arg)
				if n != 0:
					retstr += ","
				index = arg.rfind(".")
				arg = arg[index+1:]
				retstr+=arg
				if i < param_count:
					retstr += " "
					retstr += parameter_list[i]
				n += 1
		retstr += ")"
		return retstr	
	def getclassmethod_count(self,classid):
		if classid >= self.m_classDefSize:
			return ""
		offset = self.m_classDefOffset + classid * struct.calcsize("8I")
		class_idx,access_flags,superclass_idx,interfaces_off,source_file_idx,annotations_off,class_data_off,static_values_off,= struct.unpack_from("8I",self.m_content,offset)
		if class_data_off:
			offset = class_data_off
			n,static_fields_size = get_uleb128(self.m_content[offset:])
			offset += n
			n,instance_fields_size = get_uleb128(self.m_content[offset:])
			offset += n
			n,direct_methods_size = get_uleb128(self.m_content[offset:])
			offset += n
			n,virtual_methods_size = get_uleb128(self.m_content[offset:])
			offset += n
			return static_fields_size + instance_fields_size
		return 0
	def getclassmethod(classid,method_idx):
		count = 0
		if classid >= self.m_classDefSize:
			return ""
		offset = self.m_classDefOffset + classid * struct.calcsize("8I")
		class_idx,access_flags,superclass_idx,interfaces_off,source_file_idx,annotations_off,class_data_off,static_values_off,= struct.unpack_from("8I",self.m_content,offset)
		if class_data_off:
			offset = class_data_off
			n,static_fields_size = get_uleb128(self.m_content[offset:])
			offset += n
			n,instance_fields_size = get_uleb128(self.m_content[offset:])
			offset += n
			n,direct_methods_size = get_uleb128(self.m_content[offset:])
			offset += n
			n,virtual_methods_size = get_uleb128(self.m_content[offset:])
			offset += n
			count = direct_methods_size + virtual_methods_size
		if method_idx >= count:
			return ""
		ncount = static_fields_size + instance_fields_size
		ncount *= 2
		for i in xrange(0,ncount):
			n,tmp = get_uleb128(self.m_content[offset:])
			offset += n
		ncount *= 3
		for i in xrange(0,ncount):
			n,tmp = get_uleb128(self.m_content[offset:])
			offset += n
		n,method_idx_diff= get_uleb128(self.m_content[offset:])
		offset += n
		n,access_flags = get_uleb128(self.m_content[offset:])
		offset += n
		n,code_off = get_uleb128(self.m_content[offset:])
		

	def getclassname(self,classid):
		if classid >= self.m_classDefSize:
			return ""
		offset = self.m_classDefOffset + classid * struct.calcsize("8I")
		class_idx,access_flags,superclass_idx,interfaces_off,source_file_idx,annotations_off,class_data_off,static_values_off,= struct.unpack_from("8I",self.m_content,offset)
		return self.gettypename(class_idx)
	
	def init_optheader(self,content):
		offset = 0
		format = "4s"
		self.m_magic, = struct.unpack_from(format,content,offset)
		format = "I"
		offset += struct.calcsize(format)
		self.m_version, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_dexOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_dexLength, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_depsOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_depsLength, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_optOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_optLength, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_flags, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_checksum, = struct.unpack_from(format,content,offset)

	def init_header(self,content,offset):
		
		format = "4s"
		self.m_magic, = struct.unpack_from(format,content,offset)
		format = "I"
		offset += struct.calcsize(format)
		self.m_version, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_checksum, = struct.unpack_from(format,content,offset)
		format = "20s"
		offset += struct.calcsize(format)
		self.m_signature, = struct.unpack_from(format,content,offset)
		format = "I"
		offset += struct.calcsize(format)
		self.m_fileSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_headerSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_endianTag, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_linkSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_linkOff, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_mapOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_stringIdsSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_stringIdsOff, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_typeIdsSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_typeIdsOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_protoIdsSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_protoIdsOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_fieldIdsSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_fieldIdsOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_methodIdsSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_methodIdsOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_classDefSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_classDefOffset, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_dataSize, = struct.unpack_from(format,content,offset)
		offset += struct.calcsize(format)
		self.m_dataOff, = struct.unpack_from(format,content,offset)
	def gettypenamebyid(self,typeid):
		if typeid >= self.m_typeIdsSize:
			return ""
		offset = self.m_typeIdsOffset + typeid * struct.calcsize("I")
		descriptor_idx, = struct.unpack_from("I",self.m_content,offset)
		return self.string_table[descriptor_idx]
	def get_access_flags(self,flags):
		val = {1:"public",
			2:"private",
			4:"protected",
			8:"static",
			0x10:"final",
			0x20:"synchronized",
			0x40:"volatile",
			0x80:"bridge",
			0x100:"native",
			0x200:"interface",
			0x400:"abstract",
			0x800:"strict",
			0x1000:"synthetic",
			0x2000:"annotation",
			0x4000:"enum",
			0x8000:"unused",
			0x10000:"constructor",
			0x20000:"declared_synchronized"
		}
		value = ""
		i = 0
		for key in val:
			if key & flags:
				if i != 0:
					value += " "
				value += val[key]
				i+=1
		if i == 0:
			value += "public "
		
		return value
	def get_access_flags1(self,flags):
		val = {1:"public",
			2:"private",
			4:"protected"
		}
		value = ""
		i = 0
		for key in val:
			if key & flags:
				if i != 0:
					value += " "
				value += val[key]
				i+=1
		if i == 0:
			value += "public"
			flags = 1
		
		return value+":",flags
import getopt
def init():
	global filename
	global insfilename
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:d:i:", ["dumpdexfile=", "insfile="])
	except getopt.GetoptError:
		print 'Fart.py -d <dumpdexfile> -i <insfile>'
		sys.exit(2)
	if len(opts)<=0:
		print 'Fart.py -d <dumpdexfile> -i <insfile>'
		sys.exit()
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'Fart.py -d <dumpdexfile> -i <insfile>'
			sys.exit()
		if opt in ("-d", "--dumpdexfile"):
			filename = arg
		elif opt in ("-i", "--insfile"):
			insfilename = arg
	print 'dumpdex file:', filename
	print 'ins file:', insfilename
def main():
	dex = dex_parser(filename)
if __name__ == "__main__":
	init()
	methodTable.clear()
	parseinsfile()
	print "methodTable length:" + str(len(methodTable))
	main()
