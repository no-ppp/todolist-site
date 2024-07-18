import matplotlib.pyplot as plt
import numpy as np
import base64
import io


def convert_plot_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def generate_plot(x, y, label: str, title: str, xlabel: str, ylabel: str):
    # Create a figure and axis
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bar plot with custom colors
    bars = ax.bar(x, y, label=label, color='#4A90E2', edgecolor='black', linewidth=0.5)

    # Title and labels with custom font size and color
    ax.set_title(title, fontsize=30, pad=20, color='#4A90E2')
    ax.set_xlabel(xlabel, fontsize=16, labelpad=10, color='#4A90E2')
    ax.set_ylabel(ylabel, fontsize=16, labelpad=10, color='#4A90E2')

    # Customizing ticks
    ax.tick_params(axis='x', labelsize=16, colors='#4A90E2')
    ax.tick_params(axis='y', labelsize=16, colors='#4A90E2')

    # Adding a legend
    ax.legend(fontsize=16, loc='upper right', facecolor='white', edgecolor='black')

    # Customizing spines (borders)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#4A90E2')
    ax.spines['bottom'].set_color('#4A90E2')
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)

    # Adding grid
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.7)

    # Set the background color
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Adding bar values
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=12, color='#4A90E2')

    # converting the plot to base 64
    converted_plot = convert_plot_to_base64(fig)
    return converted_plot


def generate_pie(active, not_active):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8, 6))
    sizes = [active, not_active]
    labels = ['Active Tasks', 'Completed Tasks']
    colors = ['#3498db', '#4CAF50']  # White, Green
    plt.pie(sizes, explode=(0.1, 0), labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  
    #Converting the plot to Base64
    converted_plot = convert_plot_to_base64(plt)
    return converted_plot

def generate_pie_task(title_task_count, titles):
    plt.switch_backend('AGG')
    plt.figure(figsize=(8,6))
    len_titles = len(titles)
    colors = plt.cm.tab20(np.random.rand(len_titles))
    explode = [0.1] * len_titles
    plt.pie(title_task_count, explode=explode, labels=titles, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  
    #Converting the plot to Base64
    converted_plot = convert_plot_to_base64(plt)
    return converted_plot


