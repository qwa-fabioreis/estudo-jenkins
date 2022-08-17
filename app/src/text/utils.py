def remove_white_space(d):
    empty = []
    for i in range(len(d['text'])):
        if d['text'][i] == '':
            empty.append(i)
    for index in sorted(empty, reverse=True):
        for l in d:
            d[l].pop(index)
    return d


def remove_white_space_from_list(d):
    empty = []
    for i in range(len(d['letter'])):
        if d['letter'][i] == '':
            empty.append(i)
    for index in sorted(empty, reverse=True):
        for l in d:
            d[l].pop(index)
    return d


def remove_punctuation(d):

    for i in range(len(d['text'])):
        d['text'][i] = d['text'][i].upper()

    return d


def remove_punctuation_from_list(d):

    for i in range(len(d)):
        d[i] = d[i].upper()

    return d


def remove_from_list_members(l, char_list):
    dd = {ord(c): None for c in char_list}
    return list(map(lambda x: x.translate(dd), l))


def contains(small, big):

    for i in range(len(big) - len(small) + 1):
        for j in range(len(small)):
            if big[i + j] != small[j]:
                break
        else:
            return i, i + len(small)
    return False


def extract_word_boxes(c, block, x_offset=0, y_offset=0, x_border=5, y_border=5, factor=1, begin=0):
    word_boxes = []

    for word_index in range(c[0]+begin, c[1]+begin):

        (x, y, w, h) = (
            int((block['left'][word_index])/factor) + x_offset - x_border,
            int((block['top'][word_index])/factor) + y_offset - y_border,
            int(block['width'][word_index]/factor) + x_border,
            int(block['height'][word_index]/factor) + y_border)
        word_boxes.append((x, y, w, h))

    return word_boxes
