# -*- coding: utf-8 -*-
""" Interpolate Text template engine """

import re

_INTERPOLATE_TRAP = re.compile(r'\$\{([0-9A-Z]+)\}')


class InterpolateIndexedContent(object):
	def __init__(self, rule_object, *args, **kwds):
		super(InterpolateIndexedContent, self).__init__(*args, **kwds)
		self.rules = None
		self.content = None
		if isinstance(rule_object, tuple):
			self.rules = rule_object
		else:
			self.content = rule_object

	def apply_regex_match(self, match_obj, text_map=None):
		if not self.rules:
			return self.content
		f = []
		for rule_t, rule_v in self.rules:
			if rule_t == 0:
				f.append(rule_v)
			elif isinstance(rule_v, int):
				try:
					f.append(str(match_obj.group(rule_v)))
				except Exception:
					pass
			elif text_map and (rule_v in text_map):
				v = text_map[rule_v]
				if not isinstance(v, basestring):
					v = str(v)
				f.append(v)
		return ''.join(f)

	@classmethod
	def parse_template(cls, v):
		if not isinstance(v, basestring):
			v = str(v)
		result = []
		m = _INTERPOLATE_TRAP.search(v)
		lidx = 0
		while m:
			spns, spne = m.span(0)
			if spns > lidx:
				aux = (0, v[lidx:spns])
				result.append(aux)
			try:
				aux = (1, int(m.group(1)))
			except Exception:
				aux = (1, str(m.group(1)))
			result.append(aux)
			lidx = spne
			m = _INTERPOLATE_TRAP.search(v, lidx)
		if not result:
			return cls(v)
		aux = v[lidx:]
		if aux:
			aux = (0, aux)
			result.append(aux)
		return cls(tuple(result))
