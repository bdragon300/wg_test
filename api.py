from app import app, memcache
import flask


@app.route('/fibonachi', methods=('GET', ))
def fibonachi():
    required_args = ['from', 'to']
    try:
        f, t = [int(flask.request.args[x]) for x in required_args]
    except (KeyError, TypeError):
        flask.abort(400)

    if f > t or t < 0 or f < 0:
        flask.abort(400)

    res = []
    offset = 10
    fk = f - f % offset
    tk = t - t % offset + offset
    start = fk
    ref1, ref2 = None, None  # The last 2 numbers in previous block in order to calculate ones in current block

    # Try to figure out whether previous block exists
    # If not, check whole sequence from 0
    if start > 0:
        prev_cached = memcache.client.get(str(start - offset))
        if prev_cached:
            ref1, ref2 = [int(x) for x in prev_cached.decode().split(',')][-2:]
        else:
            start = 0

    for k in range(start, tk, offset):
        cached = memcache.client.get(str(k))
        seq = None

        if not cached:
            seq = list(get_fibonacci(ref1, ref2, offset))
            ref1, ref2 = seq[-2:]
            memcache.client.set(str(k), ','.join(str(x) for x in seq))
        else:
            seq = [int(x) for x in cached.decode().split(',')]
            ref1, ref2 = seq[-2:]

        # print(seq)
        if k >= fk:
            res.extend(seq or [int(x) for x in cached.decode().split(',')])

    res = [int(x) for x in res[f % offset:-offset + (t % offset)]]
    return flask.jsonify(res)


def get_fibonacci(ref1, ref2, count):
    """
        Return Fibonacci sequence of numbers starting next after ref2. I.e. the first item will be ref1+ref2
        If both ref1 and ref2 are None then returns the seqence from start: 0, 1, 1, 2,...
    """
    p, q = ref1, ref2
    c = count

    if ref1 is None and ref2 is None:
        p, q = 0, 1
        yield p
        yield q
        c -= 2
    elif p > q:
        raise ValueError('ref1 more than ref2')

    while c > 0:
        s = p + q
        p = q
        q = s
        yield s
        c -= 1
