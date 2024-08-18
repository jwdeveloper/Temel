import time

from temel import parse, init

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()

    data = {
        'buttons': [
            {
                'name': 'Home'
            },
            {
                'name': 'Settings'
            },
            {
                'name': 'Profile'
            }]
    }
    start_time = time.time()  # Start timing
    output = parse("test", data)

    with open('output.html', 'w') as f:
        f.write(output)
    end_time = time.time()  # End timing
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")
    print("Output has been saved to output.html")
