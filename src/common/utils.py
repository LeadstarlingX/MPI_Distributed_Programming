def generate_data(size):
    import numpy as np
    return np.random.randint(0, 11, size)

def verify_prefix_sum(original_data, prefix_sum_result):
    import numpy as np
    expected = np.cumsum(original_data)
    return np.allclose(expected, prefix_sum_result)
