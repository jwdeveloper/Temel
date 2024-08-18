import time
import temel

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
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

    #temel.enable_debug(True, 'C:\\Users\\ja\\PycharmProjectsss\\Tement\\tests\\output')
    temel.load_templates('C:\\Users\\ja\\PycharmProjectsss\\Tement\\tests\\templates')

    start_time = time.time()
    output = temel.parse("test", data)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")

    with open('output.html', 'w') as f:
        f.write(output)
    print("Output has been saved to output.html")
