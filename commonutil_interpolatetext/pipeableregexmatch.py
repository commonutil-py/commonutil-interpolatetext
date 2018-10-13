# -*- coding: utf-8 -*-
""" PipeableRegExMatch Interpolate Text template engine """

import logging

from commonutil_interpolatetext._base import _InterpolateBase

_log = logging.getLogger(__name__)


class InterpolatePipeableRegExMatch(_InterpolateBase):
	"""
	Interpolate with a RegEx match object and optionally a string map.

	Value transform by piping into callables.
	"""

	# pylint: disable=arguments-differ
	def _make_value_fetch_callable(self, match_obj, text_map=None):
		def f(rule_type, rule_value):
			source_key, pipe_callables = rule_value
			if rule_type == 1:
				v = str(match_obj.group(source_key))
			elif text_map:
				v = text_map[source_key]
			else:
				raise KeyError("cannot reach value for key: " + repr(source_key))
			if pipe_callables:
				for c in pipe_callables:
					v = c(v)
			return v

		return f

	@classmethod
	def _fetch_pipe_callable_args(cls, pipe_callable):
		try:
			args_func = getattr(pipe_callable, "get_args")
			return args_func()
		except AttributeError:
			pass
		return pipe_callable(None)

	@classmethod
	def _stringize_pipe_callable_cmd(cls, pipe_callable):
		c_args = cls._fetch_pipe_callable_args(pipe_callable)
		if not c_args:
			_log.error("have empty arguments on stringize pipe callable: %r", pipe_callable)
			return None
		return ",".join(c_args)

	@classmethod
	def _stringize_rule(cls, rule_type, rule_value):
		source_key, pipe_callables = rule_value
		rule_parts = [
				str(source_key),
		]
		if pipe_callables:
			for c in pipe_callables:
				try:
					p_cmd = cls._stringize_pipe_callable_cmd(c)
				except Exception:
					_log.exception("failed on stringize pipe callable: %r", c)
					p_cmd = None
				rule_parts.append(p_cmd)
		return ":".join(rule_parts)

	@classmethod
	def _parse_rule(cls, rule_text, pipe_callable_builder=None):
		aux = rule_text.split(":")
		source_key = aux[0]
		pipe_callables = []
		for pipe_cmd in aux[1:]:
			pipe_args = pipe_cmd.split(",")
			c = pipe_callable_builder(*pipe_args)
			pipe_callables.append(c)
		if not pipe_callables:
			pipe_callables = None
		try:
			return (1, (int(source_key), pipe_callables))
		except Exception:
			pass
		return (2, (source_key, pipe_callables))
