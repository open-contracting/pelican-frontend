
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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
    'not_available': '#ebedf5'
}


def resource_result_box(passed_count, failed_count, not_available_count):
    plt.figure()
    plt.rcdefaults()
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 2)

    data = [not_available_count, failed_count, passed_count]
    ax.barh(
        y=[0, 1, 2],
        width=data,
        height=0.6,
        color=[COLOR['not_available'], COLOR['failed'], COLOR['ok']]
    )
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(
        ['Not available', 'Failed', 'Passed'],
        fontfamily='GT Eesti Pro Display',
        color=COLOR['dark_grey']
    )
    ax.tick_params(axis='both', which='both',length=0)
    ax.get_xaxis().set_ticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    new_patches = []
    for patch in reversed(ax.patches):
        bb = patch.get_bbox()
        color=patch.get_facecolor()
        p_bbox = FancyBboxPatch(
            (bb.xmin, bb.ymin),
            abs(bb.width), abs(bb.height),
            boxstyle="Round,pad=0.0,rounding_size=0.55",
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
            if percentage > 5:
                font_color = 'white' 
            else:
                font_color = COLOR['dark_grey']
        else:
            font_color = COLOR['dark_grey']

        plt.text(
            bbox.xmin + 0.01 * sum(data),
            bbox.ymin + bbox.height / 2,
            percentage_str,
            color=font_color,
            fontsize=12,
            fontfamily='Ubuntu mono',
            fontweight='bold',
            verticalalignment='center'
        )

        plt.text(
            max(bbox.xmin + 0.08 * sum(data), bbox.xmax + 0.01 * sum(data)),
            bbox.ymin + bbox.height / 2,
            value_str,
            color=COLOR['grey'],
            fontsize=12,
            fontfamily='Ubuntu mono',
            verticalalignment='center'
        )

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    return buffer


def field_result_box(passed_count, failed_count):
    plt.figure()
    plt.rcdefaults()
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 2)

    data = [failed_count, passed_count]
    ax.barh(
        y=[0, 1],
        width=data,
        height=0.6,
        color=[COLOR['failed'], COLOR['ok']]
    )
    ax.set_yticks([0, 1])
    ax.set_yticklabels(
        ['Failed', 'Passed'],
        fontfamily='GT Eesti Pro Display',
        color=COLOR['dark_grey'],
    )
    ax.tick_params(axis='both', which='both',length=0)
    ax.get_xaxis().set_ticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    new_patches = []
    for patch in reversed(ax.patches):
        bb = patch.get_bbox()
        color=patch.get_facecolor()
        p_bbox = FancyBboxPatch(
            (bb.xmin, bb.ymin),
            abs(bb.width), abs(bb.height),
            boxstyle="Round,pad=0.0,rounding_size=0.55",
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
        if percentage > 5:
            font_color = 'white' 
        else:
            font_color = COLOR['dark_grey']

        plt.text(
            bbox.xmin + 0.01 * sum(data),
            bbox.ymin + bbox.height / 2,
            percentage_str,
            color=font_color,
            fontsize=12,
            fontfamily='Ubuntu mono',
            fontweight='bold',
            verticalalignment='center'
        )

        plt.text(
            max(bbox.xmin + 0.08 * sum(data), bbox.xmax + 0.01 * sum(data)),
            bbox.ymin + bbox.height / 2,
            value_str,
            color=COLOR['grey'],
            fontsize=12,
            fontfamily='Ubuntu mono',
            verticalalignment='center'
        )

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    return buffer


