import matplotlib.pyplot as plt
import seaborn as sns

def generate_plot(x, y, label: str, title: str, xlabel: str, ylabel: str):
    # Create a figure and axis
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

    # Saving the plot
    plot_path = 'media/wykres.png'
    plt.savefig(plot_path, bbox_inches='tight', facecolor=fig.get_facecolor(), 
                edgecolor='none')
    plt.close()
    return plot_path


def generate_pie(active, not_active):
    plt.figure(figsize=(8, 6))
    sizes = [active, not_active]
    labels = ['Active Tasks', 'Completed Tasks']
    colors = ['#3498db', '#4CAF50']  # Niebieski i biały
    plt.pie(sizes, explode=(0.1, 0), labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Utrzymanie koła
    # Ścieżka do pliku PNG
    plot_path = 'media/wykres_pie.png'
    # Zapis wykresu
    plt.savefig(plot_path)
    # Zamknięcie obiektu plt
    plt.close()
    return plot_path


