# -*- coding: utf-8 -*-
""" RegExMatch Interpolate Text template engine """

from commonutil_interpolatetext._base import _InterpolateBase


class InterpolateRegExMatch(_InterpolateBase):
	"""
	Interpolate with a RegEx match object and optionally a string map.
	"""

	# pylint: disable=arguments-differ
	def _make_value_fetch_callable(self, match_obj, text_map=None):
		def f(rule_type, rule_value):
			if rule_type == 1:
				return str(match_obj.group(rule_value))
			if text_map:
				return text_map[rule_value]
			raise KeyError("cannot reach value for key: " + repr(rule_value))

		return f

	@classmethod
	def _stringize_rule(cls, rule_type, rule_value):
		return str(rule_value)

	@classmethod
	def _parse_rule(cls, rule_text):
		try:
			return (1, int(rule_text))
		except Exception:
			pass
		return (2, rule_text)
