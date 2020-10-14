
import seaborn as sns
import matplotlib.pyplot as plt
from collections import OrderedDict
from matplotlib.patches import FancyBboxPatch, BoxStyle
from matplotlib import font_manager
from io import BytesIO

font_dirs = ['dqt/tools/fonts', ]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)

COLOR = {
    'dark_grey': '#4a4a4a',
    'grey': '#656565',
    'ok': '#b8c62f',
    'failed': '#d03736',
    'not_available': '#ebedf5',
    'blue': '#555cb3',
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
        y=[0, 1, 2],
        width=data_normalized,
        height=0.7,
        color=[COLOR['not_available'], COLOR['failed'], COLOR['ok']]
    )
    ax.set_xlim(right=1.0)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(
        ['Not available', 'Failed', 'Passed'],
        fontfamily='GT Eesti Pro Display',
        color=COLOR['dark_grey']
    )
    ax.tick_params(axis='both', which='both', length=0)
    ax.get_xaxis().set_ticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    new_patches = []
    for patch in reversed(ax.patches):
        bb = patch.get_bbox()
        color = patch.get_facecolor()
        p_bbox = FancyBboxPatch(
            (bb.xmin, bb.ymin),
            abs(max(0.01, bb.width)), abs(bb.height),
            boxstyle=BoxStyle('Round,pad=0.0,rounding_size=0.0'),
            ec="none", fc=color,
        )
        patch.remove()
        new_patches.append(p_bbox)
    for patch in new_patches:
        ax.add_patch(patch)

    for index, value in enumerate(data):
        percentage = 100 * value / max(sum(data), 1)
        percentage_rounded = round(percentage)
        percentage_str = str(percentage_rounded) + '%'
        if percentage_rounded == 100.0 and percentage_rounded != percentage:
            percentage_str = '<' + percentage_str
        elif percentage_rounded == 0.0 and percentage_rounded != percentage:
            percentage_str = '>' + percentage_str
        value_str = '(' + str(value) + ')'

        patch_index = len(data) - index - 1
        bbox = ax.patches[patch_index].get_bbox()
        if patch_index < 2:
            if percentage >= 7:
                font_color = 'white'
                percentage_x = bbox.xmin + 0.01
            else:
                font_color = COLOR['dark_grey']
                percentage_x = bbox.xmax + 0.01
        else:
            font_color = COLOR['dark_grey']
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
            fontfamily='Ubuntu mono',
            fontweight='bold',
            verticalalignment='center'
        )

        value_x = max(percentage_x + 0.07, bbox.xmax + 0.01)
        plt.text(
            value_x,
            bbox.ymin + bbox.height / 2,
            value_str,
            color=COLOR['grey'],
            fontsize=12,
            fontfamily='Ubuntu mono',
            verticalalignment='center'
        )

    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close(fig)

    if return_aspect_ratio:
        return buffer, aspect_ratio
    else:
        return buffer


def field_result_box(passed_count, failed_count, return_aspect_ratio=False):
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
    ax.barh(
        y=[0, 1],
        width=data_normalized,
        height=0.7,
        color=[COLOR['failed'], COLOR['ok']]
    )
    ax.set_xlim(right=1.0)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(
        ['Failed', 'Passed'],
        fontfamily='GT Eesti Pro Display',
        color=COLOR['dark_grey'],
    )
    ax.tick_params(axis='both', which='both', length=0)
    ax.get_xaxis().set_ticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    new_patches = []
    for patch in reversed(ax.patches):
        bb = patch.get_bbox()
        color = patch.get_facecolor()
        p_bbox = FancyBboxPatch(
            (bb.xmin, bb.ymin),
            abs(max(0.01, bb.width)), abs(bb.height),
            boxstyle=BoxStyle('Round,pad=0.0,rounding_size=0.0'),
            ec="none", fc=color,
        )
        patch.remove()
        new_patches.append(p_bbox)
    for patch in new_patches:
        ax.add_patch(patch)

    for index, value in enumerate(data):
        percentage = 100 * value / max(sum(data), 1)
        percentage_rounded = round(percentage)
        percentage_str = str(percentage_rounded) + '%'
        if percentage_rounded == 100.0 and percentage_rounded != percentage:
            percentage_str = '<' + percentage_str
        elif percentage_rounded == 0.0 and percentage_rounded != percentage:
            percentage_str = '>' + percentage_str
        value_str = '(' + str(value) + ')'

        patch_index = len(data) - index - 1
        bbox = ax.patches[patch_index].get_bbox()
        if percentage >= 7:
            font_color = 'white'
            percentage_x = bbox.xmin + 0.01
        else:
            font_color = COLOR['dark_grey']
            percentage_x = bbox.xmax + 0.01

        plt.text(
            percentage_x,
            bbox.ymin + bbox.height / 2,
            percentage_str,
            color=font_color,
            fontsize=12,
            fontfamily='Ubuntu mono',
            fontweight='bold',
            verticalalignment='center'
        )

        value_x = max(percentage_x + 0.07, bbox.xmax + 0.01)
        plt.text(
            value_x,
            bbox.ymin + bbox.height / 2,
            value_str,
            color=COLOR['grey'],
            fontsize=12,
            fontfamily='Ubuntu mono',
            verticalalignment='center'
        )

    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close(fig)

    if return_aspect_ratio:
        return buffer, aspect_ratio
    else:
        return buffer


def bar_result_box(counts_mapping, return_aspect_ratio=False):
    # figure initialization
    plt.figure()
    plt.rcdefaults()
    fig, ax = plt.subplots()
    aspect_ratio = float(len(counts_mapping)) / 15.0
    fig.set_size_inches(6, 6 * aspect_ratio)

    # data preprocessing
    counts_mapping_ordered = OrderedDict({
        key: counts_mapping[key]
        for key in reversed(list(counts_mapping.keys()))
    })
    data = list(counts_mapping_ordered.values())
    if sum(data) == 0:
        data_normalized = len(data) * [0.0]
    else:
        data_normalized = [(value / sum(data)) for value in data]
    ax.barh(
        y=list(range(len(counts_mapping_ordered))),
        width=data_normalized,
        height=0.7,
        color=len(counts_mapping_ordered) * [COLOR['blue']],
    )
    ax.set_xlim(right=1.0)
    ax.set_yticks(list(range(len(counts_mapping_ordered))))
    ax.set_yticklabels(
        counts_mapping_ordered.keys(),
        fontfamily='GT Eesti Pro Display',
        color=COLOR['dark_grey']
    )
    ax.tick_params(axis='both', which='both', length=0)
    ax.get_xaxis().set_ticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    new_patches = []
    for patch in reversed(ax.patches):
        bb = patch.get_bbox()
        color = patch.get_facecolor()
        p_bbox = FancyBboxPatch(
            (bb.xmin, bb.ymin),
            abs(max(0.01, bb.width)), abs(bb.height),
            boxstyle=BoxStyle('Round,pad=0.0,rounding_size=0.0'),
            ec='none', fc=color,
        )
        patch.remove()
        new_patches.append(p_bbox)
    for patch in new_patches:
        ax.add_patch(patch)

    for index, value in enumerate(data):
        percentage = 100 * value / max(sum(data), 1)
        percentage_rounded = round(percentage)
        percentage_str = str(percentage_rounded) + '%'
        if percentage_rounded == 100.0 and percentage_rounded != percentage:
            percentage_str = '<' + percentage_str
        elif percentage_rounded == 0.0 and percentage_rounded != percentage:
            percentage_str = '>' + percentage_str
        value_str = '(' + str(value) + ')'

        patch_index = len(data) - index - 1
        bbox = ax.patches[patch_index].get_bbox()
        if percentage >= 7:
            font_color = 'white'
            percentage_x = bbox.xmin + 0.01
        else:
            font_color = COLOR['dark_grey']
            percentage_x = bbox.xmax + 0.01

        plt.text(
            percentage_x,
            bbox.ymin + bbox.height / 2,
            percentage_str,
            color=font_color,
            fontsize=12,
            fontfamily='Ubuntu mono',
            fontweight='bold',
            verticalalignment='center'
        )

        value_x = max(percentage_x + 0.07, bbox.xmax + 0.01)
        plt.text(
            value_x,
            bbox.ymin + bbox.height / 2,
            value_str,
            color=COLOR['grey'],
            fontsize=12,
            fontfamily='Ubuntu mono',
            verticalalignment='center'
        )

    buffer = BytesIO()
    plt.savefig(buffer, dpi=500, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close(fig)

    if return_aspect_ratio:
        return buffer, aspect_ratio
    else:
        return buffer
