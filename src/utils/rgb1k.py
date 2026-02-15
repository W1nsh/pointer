def rgb_to_1krgb(
		r: int | None = None,
		g: int | None = None,
		b: int | None = None,
	) -> dict[str, int]:
	if r is None or g is None or b is None:
		raise ValueError('''
			No arguments were passed (r, g, b)
		''')
	r_1k = round((r * 1000)/ 255)
	g_1k = round((g * 1000)/ 255)
	b_1k = round((b * 1000)/ 255)
	rgb1k = {
		'r': r_1k,
		'g': g_1k,
		'b': b_1k,
	}
	return rgb1k
