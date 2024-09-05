import math
from io import BytesIO

import matplotlib as mpl
import matplotlib.pyplot as plt
from django.conf import settings
from matplotlib import font_manager
from matplotlib.patches import BoxStyle, FancyBboxPatch
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = settings.BASE_DIR / "exporter" / "assets"
FONT_SANS = "GT Eesti Pro Display"
FONT_MONO = "Ubuntu mono"
COLOR = {
    "light_black": "#212529",
    "dark_grey": "#4a4a4a",
    "grey": "#656565",
    "light_grey": "#dee2e6",
    "ok": "#b8c62f",
    "failed": "#d03736",
    "not_available": "#ebedf5",
    "blue": "#555cb3",
}

mpl.use("Agg")

for font in font_manager.findSystemFonts(fontpaths=str(ASSETS_DIR / "fonts")):
    font_manager.fontManager.addfont(font)


def build_fig(aspect_ratio):
    """
    Remember to call .close() in the figure.
    """
    plt.rcdefaults()
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6 * aspect_ratio)

    return fig, ax


def hide_spines(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)


def build_buffer(fig):
    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    return buffer


def box(data, aspect_ratio, ylabels, ycolors, white):
    total_count = sum(data)
    data_normalized = len(data) * [0.0] if total_count == 0 else [value / total_count for value in data]

    yticks = list(range(len(ylabels)))

    fig, ax = build_fig(aspect_ratio)

    ax.barh(y=yticks, width=data_normalized, height=0.7, color=ycolors)
    ax.set_xlim(right=1.0)
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, fontfamily=FONT_SANS, color=COLOR["dark_grey"])
    ax.tick_params(axis="both", which="both", length=0)
    ax.get_xaxis().set_ticks([])
    hide_spines(ax)

    new_patches = []
    for patch in reversed(ax.patches):
        bb = patch.get_bbox()
        color = patch.get_facecolor()
        p_bbox = FancyBboxPatch(
            (bb.xmin, bb.ymin),
            abs(max(0.01, bb.width)),
            abs(bb.height),
            boxstyle=BoxStyle("Round,pad=0.0,rounding_size=0.0"),
            ec="none",
            fc=color,
        )
        patch.remove()
        new_patches.append(p_bbox)
    for patch in new_patches:
        ax.add_patch(patch)

    for index, value in enumerate(data):
        percentage = 100 * value / max(total_count, 1)
        percentage_rounded = round(percentage)
        percentage_str = f"{percentage_rounded}%"
        if percentage_rounded == 100.0 and percentage_rounded != percentage:
            percentage_str = "<" + percentage_str
        elif percentage_rounded == 0.0 and percentage_rounded != percentage:
            percentage_str = ">" + percentage_str
        value_str = f"({value})"

        patch_index = len(data) - index - 1
        bbox = ax.patches[patch_index].get_bbox()
        font_color = "white" if white(patch_index, percentage) else COLOR["dark_grey"]
        percentage_x = bbox.xmin + 0.01 if percentage >= 7 else bbox.xmax + 0.01

        plt.text(
            percentage_x,
            bbox.ymin + bbox.height / 2,
            percentage_str,
            color=font_color,
            fontsize=12,
            fontfamily=FONT_MONO,
            fontweight="bold",
            verticalalignment="center",
        )

        value_x = max(percentage_x + 0.07, bbox.xmax + 0.01)
        plt.text(
            value_x,
            bbox.ymin + bbox.height / 2,
            value_str,
            color=COLOR["grey"],
            fontsize=12,
            fontfamily=FONT_MONO,
            verticalalignment="center",
        )

    return build_buffer(fig), aspect_ratio


def resource_result_box(data):
    return box(
        list(reversed(data)),
        3.0 / 15.0,
        ["Not applicable", "Failed", "Passed"],
        [COLOR["not_available"], COLOR["failed"], COLOR["ok"]],
        lambda patch_index, percentage: patch_index < 2 and percentage >= 7,
    )


def passed_result_box(data):
    return box(
        list(reversed(data)),
        2.0 / 15.0,
        ["Failed", "Passed"],
        [COLOR["failed"], COLOR["ok"]],
        lambda _, percentage: percentage >= 7,
    )


def bar_result_box(counts_pairs):
    ylabels, data = list(zip(*reversed(counts_pairs), strict=True))

    return box(
        data,
        float(len(counts_pairs)) / 15.0,
        ylabels,
        len(ylabels) * [COLOR["blue"]],
        lambda _, percentage: percentage >= 7,
    )


def table_result_box(counts_pairs, total_count=None):
    values, counts = list(zip(*counts_pairs, strict=True))
    aspect_ratio = float(len(counts_pairs) + 1) / 15.0

    if total_count is None:
        total_count = sum(counts)

    shares = len(counts) * [0.0] if total_count == 0 else [(count / total_count) for count in counts]

    percentage_strs = []
    for share in shares:
        percentage = 100 * share
        percentage_rounded = round(percentage, 2)
        if percentage_rounded == 0.0 and percentage != 0.0:
            percentage_strs.append(f">{percentage_rounded:.2f}%")
        elif percentage_rounded == 100.0 and percentage != 100.0:
            percentage_strs.append(f"<{percentage_rounded:.2f}%")
        else:
            percentage_strs.append(f"{percentage_rounded:.2f}%")

    fig, ax = build_fig(aspect_ratio)
    table = ax.table(
        cellText=list(zip(values, percentage_strs, counts, strict=True)),
        colLabels=["Value", "Share", "Occurrences"],
        cellLoc="left",
        colLoc="left",
        edges="B",
        loc="center",
    )
    plt.axis("off")
    plt.grid("off")
    for position, cell in table.get_celld().items():
        row, col = position
        if row == 0:
            cell.set_text_props(fontsize=12, fontfamily=FONT_SANS, fontweight="bold", color=COLOR["dark_grey"])
        elif col == 0:
            cell.set_text_props(fontsize=12, fontfamily=FONT_SANS, fontweight="normal", color=COLOR["dark_grey"])
        else:
            cell.set_text_props(fontsize=12, fontfamily=FONT_MONO, fontweight="normal", color=COLOR["dark_grey"])

        if row == len(counts_pairs):
            cell.visible_edges = ""

        cell.set_height(cell.get_height() * 1.5)
        cell.set_edgecolor(COLOR["light_grey"])

    return build_buffer(fig), aspect_ratio


def lifecycle_image(planning_count, tender_count, award_count, contract_count, implementation_count):
    image = Image.open(str(ASSETS_DIR / "images" / "lifecycle.png"))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(ASSETS_DIR / "fonts" / "GT Eesti Pro Display Regular.ttf"), 45)

    for text, xy in (
        (planning_count, (154, 283)),
        (tender_count, (415, 283)),
        (award_count, (676, 283)),
        (contract_count, (937, 283)),
        (implementation_count, (1198, 283)),
    ):
        draw.text(
            xy=xy,
            text=str(text),
            fill=COLOR["light_black"],
            font=font,
            anchor="ma",
        )

    buffer = BytesIO()
    image.save(buffer, format="png")
    buffer.seek(0)

    return buffer, (float(image.height) / float(image.width))


def histogram_result_box(counts_pairs):
    values, counts = list(zip(*counts_pairs, strict=True))
    aspect_ratio = 0.5

    fig, ax = build_fig(aspect_ratio)

    ax.bar(x=list(range(len(counts_pairs))), height=counts, color=len(counts_pairs) * [COLOR["blue"]])

    ax.set_xticks(list({0, len(counts_pairs) // 2, len(counts_pairs) - 1}))
    if len(counts_pairs) == 1:
        xticklabels = [values[0]]
    elif len(counts_pairs) == 2:
        xticklabels = [values[0], values[-1]]
    else:
        xticklabels = [values[0], values[len(counts_pairs) // 2], values[-1]]
    ax.set_xticklabels(xticklabels, fontfamily=FONT_SANS, color=COLOR["light_black"])

    max_count = max(counts)
    log_10 = int(math.log10(max_count))
    max_ytick = math.ceil(max_count / (10**log_10)) * (10**log_10)
    ax.set_ylim(top=max_ytick)

    yticklabels = [0, max_ytick]
    ax.set_yticks(yticklabels)
    ax.set_yticklabels(yticklabels, fontfamily=FONT_SANS, color=COLOR["light_black"])

    ax.tick_params(axis="both", which="both", length=0)
    hide_spines(ax)

    return build_buffer(fig), aspect_ratio
