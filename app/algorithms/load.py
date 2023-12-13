def load(load_items, unload_items, manifest):
    res = []

    for r, c in unload_items:
        res.append([r, c, -1, 0])

    return res