import argparse
import shutil
import sys

import pandas as pd

from config import get_args_parser
from pathlib import Path
from natsort import os_sorted, index_natsorted
from reportlab.platypus import Table, SimpleDocTemplate, Spacer, PageBreak
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib import colors  # 颜色模块
# self_defined
from report_generation import Graphs
from deepplot import ModelResultsEvaluation

pd.set_option('display.precision', 4)


def single_file_evaluation(path, args, sub_title=None):
    # Produce base information
    print(path)
    estimator = ModelResultsEvaluation(path)
    estimator.threshold_correction(method='youden')

    # Get evaluation metrics table
    dis_df = estimator.get_distribution()
    eval_df = estimator.evaluation_table()
    print(eval_df)

    all_data = estimator._all_data
    if 'pid' in all_data.columns:
        sorted_indices = index_natsorted(all_data['pid'])
        all_data = all_data.iloc[sorted_indices]

    # Produce figure

    # ----------------------pdf report_saved----------------------------
    # 创建内容对应的空列表
    content = list()
    if sub_title:
        content.append(Graphs.draw_title(sub_title))
    if args.report_describe:
        content.append(Graphs.draw_text(args.report_describe))

    # 添加段落文字
    content.append(Graphs.draw_text('The data file path:', color='green'))
    # content.append(Graphs.draw_text(args.result_path))

    # Image base info table
    content.append(Graphs.draw_little_title('Dataset distribution'))
    dis_df = dis_df.astype('str')
    dis_table = tuple([dis_df.columns.to_list()] + dis_df.values.tolist())
    content.append(Graphs.draw_table(*dis_table, col_width=80))

    # evaluation table
    content.append(Graphs.draw_little_title('Evaluation metrics for the results'))
    eval_df = eval_df.round(4)
    eval_df = eval_df.astype('str')
    eval_table = tuple([eval_df.columns.to_list()] + eval_df.values.tolist())
    content.append(Graphs.draw_table(*eval_table, col_width=70))

    # prediction and labels
    content.append(PageBreak())
    content.append(Graphs.draw_little_title('The probability, prediction and label of the dataset'))
    all_data = all_data.round(4)
    all_data = all_data.astype('str')
    data_table = tuple([all_data.columns.to_list()] + all_data.values.tolist())
    content.append(Graphs.draw_table(*data_table, col_width=80))
    # 添加图片
    # content.append(Spacer(1, 20))
    # content.append(Graphs.draw_text('Single image in middle one:', color='green'))
    # content.extend(Graphs.draw_img(str(saved_dir / 'single_img.png'), width=8))

    # 添加图片
    # content.append(Spacer(1, 20))
    # content.append(Graphs.draw_text('All slices:', color='green'))
    # content.extend(Graphs.draw_img(str(saved_dir / 'multi_img.png'), width=16))

    # Metadata base info table
    # content.append(Graphs.draw_little_title('Metadata of the dicom series'))
    # meta_info_table = tuple([meta_info_df.columns.to_list()] + meta_info_df.values.tolist())
    # content.append(Graphs.draw_table(*meta_info_table, col_width=[120, 360]))

    content.append(PageBreak())
    return content


def multi_files_evaluation(path, args):
    # 创建内容对应的空列表
    content = list()
    files = [file for file in path.iterdir() if file.is_file()]
    for n, x in enumerate(files):
        part_content = single_file_evaluation(x, args, x.name.split('.')[0])
        content.extend(part_content)
    return content


def main(args):
    print(args)

    result_path = Path(args.result_path)
    if not result_path.exists():
        print('The path of input file is not exist, please check it!')
        sys.exit()

    saved_dir = Path(args.report_saved_dir)
    # mkdir a template directory
    Path('./tmp').mkdir(parents=True, exist_ok=True)

    # Judge single or multi results, single->a file, mutil->a dir
    if result_path.is_dir():
        content = multi_files_evaluation(result_path, args)
    else:
        content = single_file_evaluation(result_path, args)

    # 生成pdf文件
    doc = SimpleDocTemplate(str(saved_dir / args.report_file_name), pagesize=letter)
    doc.build(content)

    # Delete the template files in the process
    shutil.rmtree('./tmp')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Evaluation report', parents=[get_args_parser()])
    args = parser.parse_args()
    if args.report_saved_dir:
        Path(args.report_saved_dir).mkdir(parents=True, exist_ok=True)
    main(args)
