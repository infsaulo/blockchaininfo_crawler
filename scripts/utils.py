def calculate_precision(relevant_entries, retrieved_entries):
    return len(set(relevant_entries) & set(retrieved_entries))/float(len(relevant_entries))

def calculate_average_precision(relevant_entries, retrieved_entries):
    average_precision = 0.0
    amount_entries = 0
    for slice_size in xrange(1, len(retrieved_entries)+1):
        amount_entries += 1
        average_precision += calculate_precision(relevant_entries[:slice_size],
                                                 retrieved_entries[:slice_size])

    return average_precision/amount_entries
