
series_titles = ["Maximum temperature (Degree C)", "Minimum temperature (Degree C)", "Rainfall amount (millimetres)", "Temperature range (Degree C)"]

calculation_options = [
    "Mean",
    "Variance",
    "Standard Deviation",
    "Range",
    "Interquartile Range (IQR)"
]

def mean(in_series):
    total = 0
    count = 0

    for value in in_series:
        if value is not None:   # skip missing values
            total += value
            count += 1

    if count == 0:
        return None

    return total / count

def variance(in_series):
    data = [x for x in in_series if x is not None]

    n = len(data)
    if n == 0:
        return None

    avg = mean(data)

    total = 0
    for value in data:
        total += (value - avg) ** 2

    return total / n

def standard_deviation(in_series):
   return variance(in_series) ** 0.5

def interquartile_range(in_series):
    # Remove None values
    data = [x for x in in_series if x is not None]

    if len(data) == 0:
        return None

    # Sort the data
    data.sort()

    # Median helper
    def median(values):
        n = len(values)
        mid = n // 2

        if n % 2 == 0:
            return (values[mid - 1] + values[mid]) / 2
        else:
            return values[mid]

    n = len(data)
    mid = n // 2

    # Split into halves
    if n % 2 == 0:
        lower_half = data[:mid]
        upper_half = data[mid:]
    else:
        lower_half = data[:mid]
        upper_half = data[mid + 1:]

    # Quartiles
    Q1 = median(lower_half)
    Q3 = median(upper_half)

    return Q3 - Q1

def temperature_range_series(max_series, min_series):
    result = []

    for index in range(len(max_series)):
        max_value = max_series[index]
        min_value = min_series[index]

        if max_value is None or min_value is None:
            result.append(None)
        else:
            result.append(max_value - min_value)

    return result
    

def filter_series(date_series, data_series, min_date=None, max_date=None):
    filtered = []

    for index in range(len(data_series)):
        date = date_series[index]
        value = data_series[index]

        if value is None:
            continue

        if min_date is not None:
            if date < min_date:
                continue

        if max_date is not None:
            if date > max_date:
                continue

        filtered.append(value)

    return filtered

def series_range(in_series):    
    data = [x for x in in_series if x is not None]

    if len(data) == 0:
        return None

    minimum = min(data)
    maximum = max(data)

    return maximum - minimum

def read_csv(file, default_value=None):
    data_table = {}
    with open(file) as f:
        lines = f.readlines()

    lines = [line.strip().split(',') for line in lines]

    for i in range(len(lines[0])):
        column_name = lines[0][i]

        column_data = []
        for line in lines[1:]:
            value = line[i]

            if value == "":
                column_data.append(default_value)
            else:
                try:
                    column_data.append(float(value))
                except ValueError:
                    column_data.append(value)  # keep as string (e.g. dates)

        data_table[column_name] = column_data

    return data_table

def get_date_range():
    print("\nEnter date range (YYYY-MM-DD) or press Enter to skip:")

    min_date = input("Start date: ")
    max_date = input("End date: ")

    if min_date == "":
        min_date = None

    if max_date == "":
        max_date = None

    return min_date, max_date

def get_user_choice(options):
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    choice = input("Enter the number of your choice: ")
    if choice.lower() == 'exit':
        return None
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
        print("Invalid choice. Please try again.")
        return get_user_choice(options)
    choice = int(choice) - 1
    return options[choice]

def menu(data_table):
    print("Select a data series:")
    choice = get_user_choice(series_titles)

    if choice is None:
        return
    
    if choice == "Temperature range (Degree C)":
        max_series = data_table["Maximum temperature (Degree C)"]
        min_series = data_table["Minimum temperature (Degree C)"]
        series = temperature_range_series(max_series, min_series)
    else:
        series = data_table[choice]
        
    dates = data_table["Date"]

    min_date, max_date = get_date_range()

    if min_date is not None or max_date is not None:
        series = filter_series(dates, series, min_date, max_date)

    if len(series) == 0:
        print("No data found in that date range.")
        return

    print("\nSelect a calculation:")
    calc_choice = get_user_choice(calculation_options)

    if calc_choice is None:
        return

    if calc_choice == "Mean":
        result = mean(series)
    elif calc_choice == "Variance":
        result = variance(series)
    elif calc_choice == "Standard Deviation":
        result = standard_deviation(series)
    elif calc_choice == "Range":
        result = series_range(series)
    elif calc_choice == "Interquartile Range (IQR)":
        result = interquartile_range(series)
    else:
        print("Invalid choice")
        return

    print(f"{calc_choice}: {result}")


if __name__ == "__main__":
    data = read_csv("weather_tidier.csv")
    menu(data)