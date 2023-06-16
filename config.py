import argparse


def str2bool(v):
    """
    Converts string to bool type; enables command line 
    arguments in the format of '--arg1 true --arg2 false'
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_args_parser():
    parser = argparse.ArgumentParser('Result evaluation report generation for machine learning', add_help=False)
    # ------------------------------------------ Evaluation settings------------------------------------------------
    parser.add_argument('--cut_off_method', default='youden', type=str, help='the optimal cut-off value method.')

    # ------------------------------------------ information report_saved  ------------------------------------------------
    parser.add_argument('--report_title', default='', type=str, help='The title of report_saved')
    parser.add_argument('--report_describe',
                        default='Evaluation according the probability, prediction and true label',
                        type=str, help='Description about the report')
    parser.add_argument('--result_path', type=str, help='The path of image')
    parser.add_argument('--report_saved_dir', default='./output/report_saved', type=str,
                        help='The path of report_saved saved')
    parser.add_argument('--report_file_name', default='report.pdf', type=str, help='The name of saved pdf file')
    parser.add_argument('--report_keep_tmp', action='store_true', default=False)
    # If generate the figure, default = True
    parser.add_argument('--report_confusion_matrix', action='store_true', default=True)
    parser.add_argument('--report_roc_auc', action='store_true', default=True)
    parser.add_argument('--report_dca', action='store_true', default=True)


    parser.add_argument('--file_names', nargs='+', type=str, default=['1', '2', '3'])

    return parser
