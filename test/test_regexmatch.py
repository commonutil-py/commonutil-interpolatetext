# -*- coding: utf-8 -*-
""" Unit test for InterpolateText engines """

import unittest
import re

from commonutil_interpolatetext.regexmatch import InterpolateRegExMatch


class TestInterpolateRegExMatch_1_SafeOff(unittest.TestCase):
	"""
	Test with apply both RegEx match object and text map while turned
	safe_mode off.
	"""

	def setUp(self):
		self.inst = InterpolateRegExMatch.parse_template("abc${1}/d ${2}: <${KEY}> =${VAL}${3}", False)

	def tearDown(self):
		self.inst = None

	def test_data_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		t = {
				"KEY": "-key1-",
				"VAL": "=val1=",
		}
		result = self.inst.apply(m, t)
		self.assertEqual(result, "abc312/d zyxabc: <-key1-> ==val1=ZYXABC")

	def test_miss_regexgroup_1(self):
		with self.assertRaises(IndexError):
			trap = re.compile(">([0-9]+),([a-z]+).")
			m = trap.match(">312,zyxabc.")
			t = {
					"KEY": "-key1-",
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
					"VAL": "=val1=",
			}
			self.inst.apply(m, t)


class TestInterpolateRegExMatch_1_SafeOn(unittest.TestCase):
	"""
	Test with apply both RegEx match object and text map while turned
	safe_mode on.
	"""

	def setUp(self):
		self.inst = InterpolateRegExMatch.parse_template("abc${1}/d ${2}: <${KEY}> =${VAL}${3}", True)

	def tearDown(self):
		self.inst = None

	def test_data_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		t = {
				"KEY": "-key1-",
				"VAL": "=val1=",
		}
		result = self.inst.apply(m, t)
		self.assertEqual(result, "abc312/d zyxabc: <-key1-> ==val1=ZYXABC")

	def test_miss_regexgroup_1(self):
		trap = re.compile(">([0-9]+),([a-z]+).")
		m = trap.match(">312,zyxabc.")
		t = {
				"KEY": "-key1-",
				"VAL": "=val1=",
		}
		result = self.inst.apply(m, t)
		self.assertEqual(result, "abc312/d zyxabc: <-key1-> ==val1=${3}")

	def test_miss_textmap_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		result = self.inst.apply(m)
		self.assertEqual(result, "abc312/d zyxabc: <${KEY}> =${VAL}ZYXABC")

	def test_miss_textkey_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		t = {
				"VAL": "=val1=",
		}
		result = self.inst.apply(m, t)
		self.assertEqual(result, "abc312/d zyxabc: <${KEY}> ==val1=ZYXABC")


class TestInterpolateRegExMatch_2_SafeOff(unittest.TestCase):
	"""
	Test with apply RegEx match object only while turned safe_mode off.
	"""

	def setUp(self):
		self.inst = InterpolateRegExMatch.parse_template("abc${1}/d ${2}: <$> =${3}", False)

	def tearDown(self):
		self.inst = None

	def test_data_1(self):
		trap = re.compile(">([0-9]+),([a-z]+),([A-Z]+).")
		m = trap.match(">312,zyxabc,ZYXABC.")
		result = self.inst.apply(m)
		self.assertEqual(result, "abc312/d zyxabc: <$> =ZYXABC")

	def test_miss_regexgroup_1(self):
		with self.assertRaises(IndexError):
			trap = re.compile(">([0-9]+),([a-z]+).")
			m = trap.match(">312,zyxabc.")
			self.inst.apply(m)
