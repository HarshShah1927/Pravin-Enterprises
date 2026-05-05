try:
	# import site-level admin config so Django picks up titles early
	from . import pravin_enterprises_admin  # noqa: F401
except Exception:
	pass

