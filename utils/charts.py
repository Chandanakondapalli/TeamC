import matplotlib.pyplot as plt


# -------------------------------------------------------
# Professional Chart Template
# -------------------------------------------------------

def create_chart(title="", figsize=(7, 5)):

    fig, ax = plt.subplots(figsize=figsize)

    # White chart background
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Remove unnecessary borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Light borders
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    # Grid
    ax.grid(
        axis="y",
        linestyle="--",
        linewidth=0.7,
        alpha=0.30,
        color="#94A3B8"
    )

    # Fonts
    ax.tick_params(
        axis="both",
        labelsize=10,
        colors="#475569"
    )

    # Chart title
    if title:
        ax.set_title(
            title,
            fontsize=16,
            fontweight="bold",
            color="#1E293B",
            pad=15
        )

    plt.tight_layout()

    return fig, ax