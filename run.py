import os
import subprocess
import shutil
from logging import getLogger
logger = getLogger(__name__)


def get_filenames(target_dir):
    cmd = 'ls ' + target_dir
    out = subprocess.check_output(cmd.split()).decode('utf-8')
    f_names = out.split()
    # WARNING: os.listdir()は順番を保証しない
    # f_names = os.listdir(target_dir)  # ['00000001.png', '00000002.png', ...]
    f_names_wo_ext = ['.'.join(fn.split('.')[:-1]) for fn in f_names]  # ['00000001', '00000002', ...]
    f_exts = ['.' + str(fn.split('.')[-1]) for fn in f_names]  # ['.png', '.png', ...]
    return f_names, f_names_wo_ext, f_exts


def dir_sepconv(input_dir, output_dir, loss_func='lf', sepconv_sh='./sepconv.sh'):
    def get_dst_name(input1_name, input1_ext, input2_name, input2_ext=None, delimiter='z'):
        return input1_name+delimiter+input2_name+input1_ext

    def check_dir(path):
        if not os.path.exists(path):
            logger.debug('mkdir: ' + path)
            os.makedirs(path)

    logger.info('dir_sepconv: ' + input_dir + ' -> ' + output_dir)
    check_dir(output_dir)

    src_names, src_names_wo_ext, src_exts = get_filenames(input_dir)
    logger.info('sepconv_length: ' + str(len(src_names)))

    for idx in range(len(src_names)):
        if idx == 0:
            continue
        dst_name = get_dst_name(src_names_wo_ext[idx-1], src_exts[idx-1], src_names_wo_ext[idx], src_exts[idx])
        logger.debug(loss_function+'('+input_dir+'/'+src_names[idx-1]+', '+input_dir+'/'+src_names[idx]+') -> '
                     +output_dir+'/'+dst_name)
        exec_sepconv(input_dir+'/'+src_names[idx-1], input_dir+'/'+src_names[idx],
                     output_dir+'/'+dst_name, loss_func, sepconv_sh)

    if input_dir != output_dir:
        logger.info('copy: '+input_dir+' ->'+output_dir)
        copy_list = [(input_dir+'/'+name, output_dir+'/'+name) for name in src_names]
        logger.info('copy_length: '+str(len(copy_list)))
        [logger.debug('copy: ' + task[0] + ' -> ' + task[1]) for task in copy_list]
        [shutil.copy2(task[0], task[1]) for task in copy_list]

    return output_dir


def rename_seq(target_dir, digits=8, start=1):
    logger.info('rename: ' + target_dir)
    src_names, src_names_wo_ext, src_exts = get_filenames(target_dir)
    logger.info('rename_length: ' + str(len(src_names)))
    reversed_src_names = list(reversed(src_names))
    reversed_dst_names = []
    for idx in range(len(src_names))[::-1]:
        num = idx+start
        fmt_str = '{:0'+str(digits)+'g}'
        dst_name = fmt_str.format(num)+src_exts[idx]
        reversed_dst_names.append(dst_name)
    [logger.debug('rename: '+target_dir+'/'+src+' -> '+target_dir+'/'+dst)
     for src, dst in zip(reversed_src_names, reversed_dst_names)]
    [shutil.move(target_dir+'/'+src, target_dir+'/'+dst) for src, dst in zip(reversed_src_names, reversed_dst_names)]

    return target_dir


def exec_sepconv(input1, input2, output, loss_func, sepconv_sh):
    cmd_sepconv = [sepconv_sh, input1, input2, output, loss_func]
    # logging

    stdout = subprocess.DEVNULL
    if logger.getEffectiveLevel() == 10:  # DEBUG
        stdout = None
    # run cmd
    # logger.debug(' '.join(cmd_sepconv))
    subprocess.run(cmd_sepconv, stdout=stdout)


if __name__ == '__main__':
    import logging

    # ロギング設定
    LOG_FMT = "%(asctime)s - %(levelname)s - %(threadName)s - %(name)s - %(message)s"
    LOG_LEVEL = logging.INFO
    logging.basicConfig(format=LOG_FMT, level=LOG_LEVEL)

    # 処理対象設定
    input_directory = './input'
    output_directory = './output'
    loss_function = 'lf'  # 'lf' or 'l1'

    dir_sepconv(input_directory, output_directory, loss_function)
    rename_seq(output_directory, digits=8, start=1)
