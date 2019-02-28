# -*- coding: utf-8 -*-
""" Shared logic between Interpolate Text template engine """

import re
import logging

_log = logging.getLogger(__name__)

_INTERPOLATE_TRAP = re.compile(r'\$\{([^\{\}\$]+)\}')


class _InterpolateBase:
	def __init__(self, rule_object, safe_mode, *args, **kwds):
		super().__init__(*args, **kwds)
		self.rules = None
		self.content = None
		if isinstance(rule_object, tuple):
			self.rules = rule_object
		else:
			self.content = rule_object
		self.safe_mode = safe_mode

	def _make_value_fetch_callable(self, *args, **kwds):
		"""
		Get value fetch callable from arguments of apply()

		Args:
			*args, **kwds - Arguments from apply() method.

		Return:
			Callable with prototype (rule_type, rule_value) => result_value.
		"""
		raise NotImplementedError("derived class should implement _make_value_fetch_callable()")

	def _stringize_value(self, v):
		"""
		Convert given value to string.

		The implementation must implement safe fallback if `safe_mode` is True.

		Args:
			v - Value from fetch callable.

		Return:
			String form of given value.
		"""
		try:
			return str(v)
		except Exception:
			pass
		if not self.safe_mode:
			return repr(v)
		try:
			return repr(v)
		except Exception:
			pass
		return None

	def _fetch_value(self, rule_type, rule_value, fetch_callable):
		""" (internal)
		"""
		if self.safe_mode:
			try:
				return fetch_callable(rule_type, rule_value)
			except Exception:
				_log.exception("failed on fetching value for rule: (%r, %r)", rule_type, rule_value)
			rule_text = self._stringize_rule(rule_type, rule_value)
			return "${" + rule_text + "}"
		return fetch_callable(rule_type, rule_value)

	def apply(self, *args, **kwds):
		"""
		Apply value to interpolation text.

		Args:
			*args, **kwds - Depend on implementations.

		Return:
			Interpolated string.
		"""
		if not self.rules:
			return self.content
		g = self._make_value_fetch_callable(*args, **kwds)
		f = []
		for rule_t, rule_v in self.rules:
			if rule_t == 0:
				f.append(rule_v)
				continue
			v = self._fetch_value(rule_t, rule_v, g)
			if not v:
				continue
			if not isinstance(v, str):
				v = self._stringize_value(v)
				if not v:
					continue
			f.append(v)
		return ''.join(f)

	@classmethod
	def _stringize_rule(cls, rule_type, rule_value):
		"""
		Convert interpolate rule into string.

		Args:
			rule_type, rule_value - Rule object resulted from _parse_rule().

		Return:
			String representation of interpolate rule object.
		"""
		raise NotImplementedError("derived class should implement _stringize_rule()")

	@classmethod
	def _parse_rule(cls, rule_text, **kwds):
		"""
		Parse interpolate rule.

		Args:
			rule_text - Rule text in string.
			**kwds - Extra arguments for implementation.

		Return:
			A tuple in (rule_type, rule_value) form.
		"""
		raise NotImplementedError("derived class should implement _parse_rule()")

	@classmethod
	def parse_template(cls, template_text, safe_mode=False, **kwds):
		"""
		Parse template into interpolate instance.

		Args:
			template_text - Template string
			safe_mode=False - If safe_mode is True failed interpolation will replace with rule text instead of raising exception.
			**kwds - Extra parameters for implementation.

		Return:
			Interpolate instance.
		"""
		if not isinstance(template_text, str):
			template_text = str(template_text)
		result = []
		m = _INTERPOLATE_TRAP.search(template_text)
		lidx = 0
		while m:
			spns, spne = m.span(0)
			if spns > lidx:
				aux = (0, template_text[lidx:spns])
				result.append(aux)
			aux = cls._parse_rule(m.group(1), **kwds)
			result.append(aux)
			lidx = spne
			m = _INTERPOLATE_TRAP.search(template_text, lidx)
		if not result:
			return cls(template_text, safe_mode)
		aux = template_text[lidx:]
		if aux:
			aux = (0, aux)
			result.append(aux)
		return cls(tuple(result), safe_mode)
