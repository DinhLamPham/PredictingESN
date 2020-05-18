def multi_decode_with_top_rankasdfsdfsadf(_inputSeq, _topRank):
    indices = list(range(len(_inputSeq)))
    indices.sort(key=lambda y: _inputSeq[y], reverse=True)

    return indices[:_topRank]


encode = [7, 9, 10, 1, 3, 6]
result = multi_decode_with_top_rankasdfsdfsadf(encode, 0)
print(result)
