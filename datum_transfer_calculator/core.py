import numpy as np


def get_low_columns(low_water_data: list[float]) -> list[list[float]]:
    """Extracts the low columns from the low-water data."""
    start_index = 0
    end_index = 4
    low_columns = []
    for i in range(len(low_water_data)):
        if i % 4 == 0:
            low_columns.append(low_water_data[start_index:end_index])
            start_index += 4
            end_index += 4
    return low_columns


def get_high(high_water_data: list[float]) -> list[list[float]]:
    """Extracts the high columns from the high-water data."""
    indexes_to_remove = list(range(3, len(high_water_data), 4))

    # Create a boolean mask to filter out elements to be removed
    mask = np.ones(len(high_water_data), dtype=bool)
    mask[indexes_to_remove] = False

    # Apply the mask to get the desired elements
    high_water_data = high_water_data[mask]

    start_index = 0
    end_index = 3
    high_columns = []
    for i in range(len(high_water_data)):
        if i % 3 == 0:
            high_columns.append(high_water_data[start_index:end_index])
            start_index += 3
            end_index += 3

    return high_columns


def calculate_ranges_and_means(
    low_columns: list[list[float]], high_columns: list[list[float]]
) -> tuple[list[float], list[float]]:
    """Calculates the ranges and means from the high and low columns."""
    ranges = []
    means = []
    for i in range(15):
        a, c, e, g = low_columns[i]
        b, d, f = high_columns[i]
        mean_low_water = (a + 3 * c + 3 * e + g) / 8
        mean_high_water = (b + 2 * d + f) / 4
        ranges.append(mean_high_water - mean_low_water)
        means.append((mean_high_water + mean_low_water) / 2)

    return ranges, means


def calculate_sound_datum(
    low_ranges: list[float],
    low_means: list[float],
    high_ranges: list[float],
    high_means: list[float],
) -> list[float]:
    """Calculates the Sound datum"""
    result = []
    constant = 0.518
    for i in range(15):
        result.append(
            (
                low_means[i]
                - (high_means[i] - constant)
                - (constant * low_ranges[i] / high_ranges[i])
            )
        )
    return result
