def highlight_low_quantity(row):
    if row["🔢 Тоо ширхэг"] < 5:
        return ["background-color: #ffe5e5"] * len(row)
    else:
        return ["" for _ in row]