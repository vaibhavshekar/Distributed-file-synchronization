import matplotlib.pyplot as plt

def plot_results(results):
    actions, times = zip(*results)
    plt.bar(actions, times, color='skyblue')
    plt.xlabel('Action',fontsize=20)
    plt.ylabel('Time Taken (seconds)',fontsize=20)
    plt.title('Performance Test Results',fontsize=20)
    plt.show()

def main():
    # Replace these results with actual test results
    results = [
        ('upload', 0.14),
        ('download', 0.15),
        ('view', 0.13),
        ('edit', 4.65),
    ]
    
    plot_results(results)

if __name__ == "__main__":
    main()
