import math
import os
from collections import OrderedDict
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import BoxStyle, FancyBboxPatch
from PIL import Image, ImageDraw, ImageFont

font_dirs = [
    os.path.join("dqt", "assets", "fonts"),
]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

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


def resource_result_box(passed_count, failed_count, not_available_count, return_aspect_ratio=False):
    plt.figure()
    plt.rcdefaults()
    fig, ax = plt.subplots()
    aspect_ratio = 3.0 / 15.0
    fig.set_size_inches(6, 6 * aspect_ratio)

    data = [not_available_count, failed_count, passed_count]
    if sum(data) == 0:
        data_normalized = len(data) * [0.0]
    else:
        data_normalized = [(value / sum(data)) for value in data]
    ax.barh(
        y=[0, 1, 2], width=data_normalized, height=0.7, color=[COLOR["not_available"], COLOR["failed"], COLOR["ok"]]
    )
    ax.set_xlim(right=1.0)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(
        ["Not available", "Failed", "Passed"], fontfamily="GT Eesti Pro Display", color=COLOR["dark_grey"]
    )
    ax.tick_params(axis="both", which="both", length=0)
    ax.get_xaxis().set_ticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

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
        percentage = 100 * value / max(sum(data), 1)
        percentage_rounded = round(percentage)
        percentage_str = str(percentage_rounded) + "%"
        if percentage_rounded == 100.0 and percentage_rounded != percentage:
            percentage_str = "<" + percentage_str
        elif percentage_rounded == 0.0 and percentage_rounded != percentage:
            percentage_str = ">" + percentage_str
        value_str = "(" + str(value) + ")"

        patch_index = len(data) - index - 1
        bbox = ax.patches[patch_index].get_bbox()
        if patch_index < 2:
            if percentage >= 7:
                font_color = "white"
                percentage_x = bbox.xmin + 0.01
            else:
                font_color = COLOR["dark_grey"]
                percentage_x = bbox.xmax + 0.01
        else:
            font_color = COLOR["dark_grey"]
            if percentage >= 7:
                percentage_x = bbox.xmin + 0.01
            else:
                percentage_x = bbox.xmax + 0.01

        plt.text(
            percentage_x,
            bbox.ymin + bbox.height / 2,
            percentage_str,
            color=font_color,
            fontsize=12,
            fontfamily="Ubuntu mono",
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
            fontfamily="Ubuntu mono",
            verticalalignment="center",
        )

    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    if return_aspect_ratio:
        return buffer, aspect_ratio
    else:
        return buffer


def passed_result_box(passed_count, failed_count, return_aspect_ratio=False):
    plt.figure()
    plt.rcdefaults()
    fig, ax = plt.subplots()
    aspect_ratio = 2.0 / 15.0
    fig.set_size_inches(6, 6 * aspect_ratio)

    data = [failed_count, passed_count]
    if sum(data) == 0:
        data_normalized = len(data) * [0.0]
    else:
        data_normalized = [(value / sum(data)) for value in data]
    ax.barh(y=[0, 1], width=data_normalized, height=0.7, color=[COLOR["failed"], COLOR["ok"]])
    ax.set_xlim(right=1.0)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(
        ["Failed", "Passed"],
        fontfamily="GT Eesti Pro Display",
        color=COLOR["dark_grey"],
    )
    ax.tick_params(axis="both", which="both", length=0)
    ax.get_xaxis().set_ticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

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
        percentage = 100 * value / max(sum(data), 1)
        percentage_rounded = round(percentage)
        percentage_str = str(percentage_rounded) + "%"
        if percentage_rounded == 100.0 and percentage_rounded != percentage:
            percentage_str = "<" + percentage_str
        elif percentage_rounded == 0.0 and percentage_rounded != percentage:
            percentage_str = ">" + percentage_str
        value_str = "(" + str(value) + ")"

        patch_index = len(data) - index - 1
        bbox = ax.patches[patch_index].get_bbox()
        if percentage >= 7:
            font_color = "white"
            percentage_x = bbox.xmin + 0.01
        else:
            font_color = COLOR["dark_grey"]
            percentage_x = bbox.xmax + 0.01

        plt.text(
            percentage_x,
            bbox.ymin + bbox.height / 2,
            percentage_str,
            color=font_color,
            fontsize=12,
            fontfamily="Ubuntu mono",
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
            fontfamily="Ubuntu mono",
            verticalalignment="center",
        )

    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    if return_aspect_ratio:
        return buffer, aspect_ratio
    else:
        return buffer


def bar_result_box(counts_pairs, total_count=None, return_aspect_ratio=False):
    # figure initialization
    plt.figure()
    plt.rcdefaults()
    fig, ax = plt.subplots()
    aspect_ratio = float(len(counts_pairs)) / 15.0
    fig.set_size_inches(6, 6 * aspect_ratio)

    # data preprocessing
    counts_mapping_ordered = OrderedDict({key: value for key, value in reversed(counts_pairs)})
    data = list(counts_mapping_ordered.values())

    if total_count is None:
        total_count = sum(data)

    if total_count == 0:
        data_normalized = len(data) * [0.0]
    else:
        data_normalized = [(value / total_count) for value in data]

    # figure creation
    ax.barh(
        y=list(range(len(counts_mapping_ordered))),
        width=data_normalized,
        height=0.7,
        color=len(counts_mapping_ordered) * [COLOR["blue"]],
    )
    ax.set_xlim(right=1.0)
    ax.set_yticks(list(range(len(counts_mapping_ordered))))
    ax.set_yticklabels(counts_mapping_ordered.keys(), fontfamily="GT Eesti Pro Display", color=COLOR["dark_grey"])
    ax.tick_params(axis="both", which="both", length=0)
    ax.get_xaxis().set_ticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

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
        percentage_str = str(percentage_rounded) + "%"
        if percentage_rounded == 100.0 and percentage_rounded != percentage:
            percentage_str = "<" + percentage_str
        elif percentage_rounded == 0.0 and percentage_rounded != percentage:
            percentage_str = ">" + percentage_str
        value_str = "(" + str(value) + ")"

        patch_index = len(data) - index - 1
        bbox = ax.patches[patch_index].get_bbox()
        if percentage >= 7:
            font_color = "white"
            percentage_x = bbox.xmin + 0.01
        else:
            font_color = COLOR["dark_grey"]
            percentage_x = bbox.xmax + 0.01

        plt.text(
            percentage_x,
            bbox.ymin + bbox.height / 2,
            percentage_str,
            color=font_color,
            fontsize=12,
            fontfamily="Ubuntu mono",
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
            fontfamily="Ubuntu mono",
            verticalalignment="center",
        )

    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    if return_aspect_ratio:
        return buffer, aspect_ratio
    else:
        return buffer


def table_result_box(counts_pairs, total_count=None, return_aspect_ratio=False):
    # figure initialization
    plt.figure()
    plt.rcdefaults()
    fig, ax = plt.subplots()
    aspect_ratio = float(len(counts_pairs) + 1) / 15.0
    fig.set_size_inches(6, 6 * aspect_ratio)

    # data preprocessing
    counts_mapping_ordered = OrderedDict({key: value for key, value in counts_pairs})
    values = list(counts_mapping_ordered.keys())
    counts = list(counts_mapping_ordered.values())

    if total_count is None:
        total_count = sum(counts)

    if total_count == 0:
        shares = len(counts) * [0.0]
    else:
        shares = [(count / total_count) for count in counts]

    percentage_strs = []
    for share in shares:
        percentage = 100 * share
        percentage_rounded = round(percentage, 2)
        if percentage_rounded == 0.0 and percentage != 0.0:
            percentage_strs.append(">%.2f%%" % percentage_rounded)
        elif percentage_rounded == 100.0 and percentage != 100.0:
            percentage_strs.append("<%.2f%%" % percentage_rounded)
        else:
            percentage_strs.append("%.2f%%" % percentage_rounded)

    # figure creation
    table = ax.table(
        cellText=list(zip(values, percentage_strs, counts)),
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
            cell.set_text_props(
                fontsize=12, fontfamily="GT Eesti Pro Display", fontweight="bold", color=COLOR["dark_grey"]
            )
        elif col == 0:
            cell.set_text_props(
                fontsize=12, fontfamily="GT Eesti Pro Display", fontweight="normal", color=COLOR["dark_grey"]
            )
        else:
            cell.set_text_props(fontsize=12, fontfamily="Ubuntu mono", fontweight="normal", color=COLOR["dark_grey"])

        if row == len(counts_pairs):
            cell.visible_edges = ""

        cell.set_height(cell.get_height() * 1.5)
        cell.set_edgecolor(COLOR["light_grey"])

    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    if return_aspect_ratio:
        return buffer, aspect_ratio
    else:
        return buffer


def lifecycle_image(
    planning_count, tender_count, award_count, contract_count, implementation_count, return_aspect_ratio=False
):
    image = Image.open(os.path.join("dqt", "assets", "images", "lifecycle.png"))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(os.path.join("dqt", "assets", "fonts", "GT Eesti Pro Display Regular.ttf"), 45)

    draw.text(
        xy=(154, 283),
        text=str(planning_count),
        fill=COLOR["light_black"],
        font=font,
        anchor="ma",
    )
    draw.text(
        xy=(415, 283),
        text=str(tender_count),
        fill=COLOR["light_black"],
        font=font,
        anchor="ma",
    )
    draw.text(
        xy=(676, 283),
        text=str(award_count),
        fill=COLOR["light_black"],
        font=font,
        anchor="ma",
    )
    draw.text(
        xy=(937, 283),
        text=str(contract_count),
        fill=COLOR["light_black"],
        font=font,
        anchor="ma",
    )
    draw.text(
        xy=(1198, 283),
        text=str(implementation_count),
        fill=COLOR["light_black"],
        font=font,
        anchor="ma",
    )

    buffer = BytesIO()
    image.save(buffer, format="png")
    buffer.seek(0)

    if return_aspect_ratio:
        return buffer, (float(image.height) / float(image.width))
    else:
        return buffer


def histogram_result_box(counts_pairs, return_aspect_ratio=False):
    # figure initialization
    plt.figure()
    plt.rcdefaults()
    fig, ax = plt.subplots()
    aspect_ratio = 0.5
    fig.set_size_inches(6, 6 * aspect_ratio)

    # data preprocessing
    values = [value for value, count in counts_pairs]
    counts = [count for value, count in counts_pairs]

    # figure creation
    ax.bar(
        x=list(range(len(counts_pairs))),
        height=counts,
        color=len(counts_pairs) * [COLOR["blue"]],
    )

    ax.set_xticks(
        list(
            set(
                [
                    0,
                    len(counts_pairs) // 2,
                    len(counts_pairs) - 1,
                ]
            )
        )
    )
    if len(counts_pairs) == 1:
        xticklabels = [values[0]]
    elif len(counts_pairs) == 2:
        xticklabels = [values[0], values[-1]]
    else:
        xticklabels = [values[0], values[len(counts_pairs) // 2], values[-1]]
    ax.set_xticklabels(
        xticklabels,
        fontfamily="GT Eesti Pro Display",
        color=COLOR["light_black"],
    )

    max_count = max(counts)
    log_10 = int(math.log10(max_count))
    max_ytick = math.ceil(max_count / (10 ** log_10)) * (10 ** log_10)
    ax.set_ylim(top=max_ytick)

    yticklabels = [0, max_ytick]
    ax.set_yticks(yticklabels)
    ax.set_yticklabels(
        yticklabels,
        fontfamily="GT Eesti Pro Display",
        color=COLOR["light_black"],
    )

    ax.tick_params(axis="both", which="both", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format="png", bbox_inches="tight")
    buffer.seek(0)
    plt.close(fig)

    if return_aspect_ratio:
        return buffer, aspect_ratio
    else:
        return buffer
