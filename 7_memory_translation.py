"""Task 7: Paging and segmentation translators."""

PAGE_SIZE = 1024

PAGE_TABLE = {
    0: 5,
    1: 2,
    2: 9,
    3: 1
}

# {segment: (base, limit)}
SEGMENT_TABLE = {
    0: (1000, 400),
    1: (2200, 300),
    2: (500, 150)
}


def translate_page(address):

    page_number, offset = divmod(
        address,
        PAGE_SIZE
    )

    if page_number not in PAGE_TABLE:

        return (
            f"Page fault: page {page_number} "
            f"is not present in PAGE_TABLE"
        )

    frame_number = PAGE_TABLE[
        page_number
    ]

    physical_address = (
        frame_number * PAGE_SIZE
        + offset
    )

    return physical_address


def translate_segment(
    segment,
    offset
):

    if segment not in SEGMENT_TABLE:

        return (
            f"Segmentation fault: segment "
            f"{segment} is not present"
        )

    base, limit = SEGMENT_TABLE[
        segment
    ]

    if offset >= limit:

        return (
            f"Segmentation fault: offset "
            f"{offset} >= limit {limit}"
        )

    return base + offset


if __name__ == "__main__":

    paged_addresses = [
        260,
        1500,
        3000,
        5000
    ]

    for address in paged_addresses:

        print(
            f"Paged {address} -> "
            f"{translate_page(address)}"
        )

    segmented_addresses = [
        (0, 150),
        (1, 350),
        (2, 100)
    ]

    for segment, offset in segmented_addresses:

        print(
            f"Segmented "
            f"({segment}, {offset}) -> "
            f"{translate_segment(segment, offset)}"
        )
