from random import choice


cdef str _start = "___start___"
cdef str _end = "___end___"


def generate(list samples, int tries_count, int size):
    if not samples:
        return None

    cdef list frames = []
    cdef list start_frames = []
    cdef dict frame_map = {}
    cdef list words
    cdef list result
    cdef str str_result
    cdef str next_frame
    cdef str sample
    cdef int i

    for sample in samples:
        words = sample.split(" ")
        frames.append(_start)
        for word in words:
            frames.append(word)
        frames.append(_end)

    for i in range(len(frames)):
        if frames[i] != _end:
            try:
                frame_map[frames[i]].append(frames[i + 1])

            except KeyError:
                frame_map[frames[i]] = [frames[i + 1]]

            if frames[i] == _start:
                start_frames.append(frames[i + 1])

    for i in range(tries_count):
        result = [choice(start_frames)]

        for frame in result:
            next_frame = choice(frame_map[frame])
            if next_frame == _end:
                break

            else:
                result.append(next_frame)

        str_result = " ".join(result)

        if str_result not in samples:
            if size == 0: # any
                if len(result) <= 100:
                    return str_result

            if size == 1:  # small
                if 2 <= len(result) <= 3:
                    return str_result

            elif size == 2:  # medium
                if 4 <= len(result) <= 7:
                    return str_result

            elif size == 3:  # large
                if 8 <= len(result) <= 100:
                    return str_result

            else:
                raise ValueError("Size must be 0, 1, 2 or 3")

    return None
