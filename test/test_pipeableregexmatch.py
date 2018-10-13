# -*- coding: utf-8 -*-
""" Unit test for InterpolateText engines """

import unittest
import re

from commonutil_interpolatetext.pipeableregexmatch import InterpolatePipeableRegExMatch


class MockPipeCallable_Prefix(object):
	def __init__(self, args):
		self.args = args

	def get_args(self):
		result = [
				"prefix",
		]
		result.extend(self.args)
		return result

	def __call__(self, v):
		a = (v, ) + self.args
		return "/".join(a)


def mock_pipe_callable_builder_1(pipe_type, *args):
	if pipe_type == "join":

		def f(v):
			aux = args[0]
			if v is None:
				return ("join", aux)
			return aux.join(v)
	elif pipe_type == "reverse":

		def f(v):
			if v is None:
				return ("reverse", )
			return v[::-1]
	elif pipe_type == "prefix":
		return MockPipeCallable_Prefix(args)
	else:
		raise ValueError("given pipe_type not exist: " + pipe_type)
	return f


class TestInterpolatePipeableRegExMatch_1_SafeOff(unittest.TestCase):
	"""
	Test with apply both RegEx match object and text map while turned
	safe_mode off.
	"""

	def setUp(self):
		self.inst = InterpolatePipeableRegExMatch.parse_template(
				"abc${1}/d ${2:join,-}: <${KEY:reverse:join,*}> =${VAL}${3}", False, pipe_callable_builder=mock_pipe_callable_builder_1)

	def tearDown(self):
		self.inst = None

	def test_data_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		t = {
				"KEY": "qwerty",
				"VAL": "=val1=",
		}
		result = self.inst.apply(m, t)
		self.assertEqual(result, "abc312/d z-y-x-a-b-c: <y*t*r*e*w*q> ==val1=ZYXABC")

	def test_miss_regexgroup_1(self):
		with self.assertRaises(IndexError):
			trap = re.compile(">([0-9]+),([a-z]+).")
			m = trap.match(">312,zyxabc.")
			t = {
					"KEY": "qwerty",
					"VAL": "=val1=",
			}
			self.inst.apply(m, t)

	def test_miss_textmap_1(self):
		with self.assertRaises(KeyError):
			trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
			m = trap.match(">312,zyxabc,ZYXABC.")
			self.inst.apply(m)

	def test_miss_textkey_1(self):
		with self.assertRaises(KeyError):
			trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
			m = trap.match(">312,zyxabc,ZYXABC.")
			t = {
					"VAL": "qwerty",
			}
			self.inst.apply(m, t)


class TestInterpolatePipeableRegExMatch_1_SafeOn(unittest.TestCase):
	"""
	Test with apply both RegEx match object and text map while turned
	safe_mode on.
	"""

	def setUp(self):
		self.inst = InterpolatePipeableRegExMatch.parse_template(
				"abc${1}/d ${2:join,-}: <${KEY:reverse:join,*}> =${VAL:prefix,www,O_o,D*}${3}", True, pipe_callable_builder=mock_pipe_callable_builder_1)

	def tearDown(self):
		self.inst = None

	def test_data_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		t = {
				"KEY": "qwerty",
				"VAL": "=val1=",
		}
		result = self.inst.apply(m, t)
		self.assertEqual(result, "abc312/d z-y-x-a-b-c: <y*t*r*e*w*q> ==val1=/www/O_o/D*ZYXABC")

	def test_miss_regexgroup_1(self):
		trap = re.compile(">([0-9]+),([a-z]+).")
		m = trap.match(">312,zyxabc.")
		t = {
				"KEY": "qwerty",
				"VAL": "=val1=",
		}
		result = self.inst.apply(m, t)
		self.assertEqual(result, "abc312/d z-y-x-a-b-c: <y*t*r*e*w*q> ==val1=/www/O_o/D*${3}")

	def test_miss_textmap_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		result = self.inst.apply(m)
		self.assertEqual(result, "abc312/d z-y-x-a-b-c: <${KEY:reverse:join,*}> =${VAL:prefix,www,O_o,D*}ZYXABC")

	def test_miss_textkey_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		t = {
				"VAL": "=val1=",
		}
		result = self.inst.apply(m, t)
		self.assertEqual(result, "abc312/d z-y-x-a-b-c: <${KEY:reverse:join,*}> ==val1=/www/O_o/D*ZYXABC")


class TestInterpolatePipeableRegExMatch_2_SafeOff(unittest.TestCase):
	"""
	Test with apply RegEx match object only while turned safe_mode off.
	"""

	def setUp(self):
		self.inst = InterpolatePipeableRegExMatch.parse_template(
				"abc${1}/d ${2}: <$> =${3:join,#:prefix,www,O_o:reverse}", False, pipe_callable_builder=mock_pipe_callable_builder_1)

	def tearDown(self):
		self.inst = None

	def test_data_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		result = self.inst.apply(m)
		self.assertEqual(result, "abc312/d zyxabc: <$> =o_O/www/C#B#A#X#Y#Z")

	def test_miss_regexgroup_1(self):
		with self.assertRaises(IndexError):
			trap = re.compile(">([0-9]+),([a-z]+).")
			m = trap.match(">312,zyxabc.")
			self.inst.apply(m)
