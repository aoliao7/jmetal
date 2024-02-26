import globalmanger as gm


def test(a):
    if a == 1:
        gm._init()
        gm.set_value("a", [1, 2, 3, 4])
        return a
    else:
        k = gm.get_value("a")
        return k[3]
