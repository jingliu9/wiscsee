from workflow import run_workflow
import os

import ssdbox
from utilities.utils import *
from commons import *
from config import MountOption as MOpt

class Experimenter(object):
    def __init__(self, para):
        if para.ftl == 'nkftl2':
            self.conf = ssdbox.nkftl2.Config()
        elif para.ftl == 'dftldes':
            self.conf = ssdbox.dftldes.Config()
        elif para.ftl == 'dftlext':
            self.conf = ssdbox.dftlext.Config()
        elif para.ftl == 'ftlcounter':
            self.conf = ssdbox.ftlcounter.Config()
        else:
            print para.ftl
            raise NotImplementedError()
        self.para = para
        self.conf['exp_parameters'] = self.para._asdict()

    def setup_environment(self):
        self.conf['device_path'] = self.para.device_path
        self.conf['dev_size_mb'] = self.para.lbabytes / MB
        self.conf["n_online_cpus"] = self.para.n_online_cpus

        self.conf['linux_ncq_depth'] = self.para.linux_ncq_depth

        set_vm_default()
        set_vm("dirty_bytes", self.para.dirty_bytes)

        self.conf['do_fstrim'] = False

        self.conf['trace_issue_and_complete'] = self.para.trace_issue_and_complete

        # filesystem
        self.conf['filesystem'] = self.para.filesystem

        self.conf['dump_ext4_after_workload'] = self.para.dump_ext4_after_workload

        self.conf['stop_sim_on_bytes'] = self.para.stop_sim_on_bytes

        if self.para.filesystem == 'ext4-nj':
            self.conf['filesystem'] = 'ext4'

    def setup_workload(self):
        raise NotImplementedError()

    def setup_fs(self):
        updates = {
            "f2fs":   {
                        'discard': MOpt(opt_name = 'discard',
                                        value = 'discard',
                                        include_name = False),
                        # 'background_gc': MOpt(opt_name = 'background_gc',
                                            # value = 'off',
                                            # include_name = True)
                                        },
            "ext4":   {
                        'discard': MOpt(opt_name = "discard",
                                         value = "discard",
                                         include_name = False),
                        'data': MOpt(opt_name = "data",
                                        value = self.para.ext4datamode,
                                        include_name = True) },
            "btrfs":  {
                        "discard": MOpt(opt_name = "discard",
                                         value = "discard",
                                         include_name = False),
                                         "ssd": MOpt(opt_name = 'ssd',
                                             value = 'ssd',
                                     include_name = False),
                        "autodefrag": MOpt(opt_name = 'autodefrag',
                                            value = 'autodefrag',
                                            include_name = False) },
            "xfs":    {
                'discard': MOpt(opt_name = 'discard',
                                        value = 'discard',
                                        include_name = False)
                },
            }

        if self.para.fs_discard is False:
            for fs, dic in updates.items():
                del dic['discard']


        self.conf['mnt_opts'].update(updates)

        if self.para.ext4hasjournal is True:
            enable_ext4_journal(self.conf)
        else:
            disable_ext4_journal(self.conf)

        if self.para.filesystem == 'ext4-nj':
            disable_ext4_journal(self.conf)

        self.conf['f2fs_gc_after_workload'] = self.para.f2fs_gc_after_workload
        self.conf['f2fs']['sysfs']['ipu_policy'] = self.para.f2fs_ipu_policy
        self.conf['f2fs']['sysfs']['min_fsync_blocks'] = self.para.f2fs_min_fsync_blocks

    def setup_flash(self):
        self.conf['SSDFramework']['ncq_depth'] = self.para.ssd_ncq_depth

        self.conf['flash_config']['page_size'] = 2048
        self.conf['flash_config']['n_pages_per_block'] = self.para.n_pages_per_block
        self.conf['flash_config']['n_blocks_per_plane'] = 2
        self.conf['flash_config']['n_planes_per_chip'] = 1
        self.conf['flash_config']['n_chips_per_package'] = 1
        self.conf['flash_config']['n_packages_per_channel'] = 1
        self.conf['flash_config']['n_channels_per_dev'] = self.para.n_channels_per_dev

        self.conf['do_not_check_gc_setting'] = self.para.not_check_gc_setting

        if self.para.ftl not in ('dftlext', 'ftlcounter'):
            self.conf.GC_high_threshold_ratio = self.para.gc_high_ratio
            self.conf.GC_low_threshold_ratio = self.para.gc_low_ratio

    def setup_ftl(self):
        self.conf['enable_blktrace'] = self.para.enable_blktrace
        self.conf['enable_simulation'] = self.para.enable_simulation
        self.conf['stripe_size'] = self.para.stripe_size
        self.conf['segment_bytes'] = self.para.segment_bytes
        self.conf['snapshot_interval'] = self.para.snapshot_interval
        self.conf['do_wear_leveling'] = self.para.do_wear_leveling
        self.conf['wear_leveling_check_interval'] = \
                self.para.wear_leveling_check_interval
        self.conf['wear_leveling_factor'] = self.para.wear_leveling_factor
        self.conf['wear_leveling_diff'] = self.para.wear_leveling_diff
        self.conf['only_get_traffic'] = self.para.only_get_traffic

        if self.para.ftl == 'dftldes':
            self.conf['simulator_class'] = 'SimulatorDESNew'
            self.conf['ftl_type'] = 'dftldes'
            self.conf['snapshot_valid_ratios'] = self.para.snapshot_valid_ratios
            self.conf['snapshot_erasure_count_dist'] = self.para.snapshot_erasure_count_dist
            self.conf['do_gc_after_workload'] = self.para.do_gc_after_workload
            self.conf.cache_mapped_data_bytes = self.para.cache_mapped_data_bytes
            self.conf['write_gc_log'] = self.para.write_gc_log

        elif self.para.ftl == 'nkftl2':
            self.conf['simulator_class'] = 'SimulatorDESNew'
            self.conf['ftl_type'] = 'nkftl2'
            self.conf['write_gc_log'] = self.para.write_gc_log

            self.conf['nkftl']['n_blocks_in_data_group'] = \
                self.para.segment_bytes / self.conf.block_bytes
            self.conf['nkftl']['max_blocks_in_log_group'] = \
                self.conf['nkftl']['n_blocks_in_data_group'] * self.para.log_group_factor
            print 'N:', self.conf['nkftl']['n_blocks_in_data_group']
            print 'K:', self.conf['nkftl']['max_blocks_in_log_group']
            self.conf['nkftl']['max_ratio_of_log_blocks'] = self.para.max_log_blocks_ratio
            self.conf['snapshot_valid_ratios'] = False
            self.conf['snapshot_erasure_count_dist'] = self.para.snapshot_erasure_count_dist
            self.conf['do_gc_after_workload'] = self.para.do_gc_after_workload


        elif self.para.ftl == 'dftlext':
            self.conf['simulator_class'] = 'SimulatorNonDESSpeed'
            self.conf['ftl_type'] = 'dftlext'
            self.conf.cache_mapped_data_bytes = self.para.cache_mapped_data_bytes

            # Force wear leveling off since it is not implemented in nkftl
            self.conf['do_wear_leveling'] = False

        elif self.para.ftl == 'ftlcounter':
            self.conf['simulator_class'] = 'SimulatorNonDESSpeed'
            self.conf['ftl_type'] = 'ftlcounter'
            self.conf.cache_mapped_data_bytes = self.para.cache_mapped_data_bytes
            self.conf['gen_ncq_depth_table'] = self.para.gen_ncq_depth_table
            self.conf['do_dump_lpn_sem'] = self.para.do_dump_lpn_sem

            # Force wear leveling off since it is not implemented in nkftl
            self.conf['do_wear_leveling'] = False

        else:
            raise NotImplementedError()

        logicsize_mb = self.conf['dev_size_mb']
        self.conf.set_flash_num_blocks_by_bytes(
                int(logicsize_mb * 2**20 * self.para.over_provisioning))

    def check_config(self):
        if self.conf['ftl_type'] == 'dftldes':
            assert isinstance(self.conf, ssdbox.dftldes.Config)
            assert self.conf['simulator_class'] == 'SimulatorDESNew'
        elif self.conf['ftl_type'] == 'nkftl2':
            assert isinstance(self.conf, ssdbox.nkftl2.Config)
            assert self.conf['simulator_class'] == 'SimulatorDESNew'
        elif self.conf['ftl_type'] == 'dftlext':
            assert isinstance(self.conf, ssdbox.dftlext.Config)
            assert self.conf['simulator_class'] == 'SimulatorNonDESSpeed'
        elif self.conf['ftl_type'] == 'ftlcounter':
            assert isinstance(self.conf, ssdbox.ftlcounter.Config)
            assert self.conf['simulator_class'] == 'SimulatorNonDESSpeed'
        else:
            RuntimeError("ftl type may not be supported here")

    def before_running(self):
        pass

    def after_running(self):
        pass

    def run(self):
        # dict_for_name = {k:v for k,v in self.para._asdict() if k in ('
        set_exp_metadata(self.conf, save_data = True,
                expname = self.para.expname,
                subexpname = 'subexp-' + str(hash(chain_items_as_filename(self.para))))
        runtime_update(self.conf)

        self.check_config()

        print self.conf

        run_workflow(self.conf)

    def main(self):
        self.setup_environment()
        self.setup_fs()
        self.setup_workload()
        self.setup_flash()
        self.setup_ftl()
        self.before_running()
        self.run()
        self.after_running()


def get_shared_para_dict(expname, lbabytes):
    para_dict = {
            'ftl'            : ['dftldes'],
            'device_path'    : ['/dev/sdc1'],
            # 'filesystem'     : ['f2fs', 'ext4', 'ext4-nj', 'btrfs', 'xfs'],
            'filesystem'     : ['ext4'],
            'ext4datamode'   : ['ordered'],
            'ext4hasjournal' : [True],
            'expname'        : [expname],
            'dirty_bytes'    : [4*GB],
            'linux_ncq_depth': [31],
            'ssd_ncq_depth'  : [1],
            'cache_mapped_data_bytes' :[lbabytes],
            'lbabytes'       : [lbabytes],
            'n_pages_per_block': [64],
            'stripe_size'    : [1],
            'enable_blktrace': [True],
            'enable_simulation': [True],
            'f2fs_gc_after_workload': [False],
            'segment_bytes'  : [2*MB],
            'max_log_blocks_ratio': [100],
            'n_online_cpus'  : ['all'],
            'over_provisioning': [32], # 1.28 is a good number
            'gc_high_ratio'    : [0.9],
            'gc_low_ratio'     : [0.0],
            'not_check_gc_setting': [True],
            'snapshot_interval': [0.1*SEC],
            'write_gc_log'     : [True],
            'f2fs_ipu_policy'  : [F2FS_IPU_FSYNC],
            'f2fs_min_fsync_blocks':[8],
            'dump_ext4_after_workload': [True],
            'wear_leveling_check_interval': [10*SEC],
            'do_wear_leveling' : [False],
            'wear_leveling_factor': [2],
            'wear_leveling_diff': [10],
            'snapshot_valid_ratios': [True],
            'snapshot_erasure_count_dist': [True],
            'n_channels_per_dev'  : [16],
            'do_gc_after_workload': [False],
            'trace_issue_and_complete': [False],
            'fs_discard': [True],
            'only_get_traffic': [True],
            'age_workload_class': ['NoOp'],
            'aging_appconfs': [None],
            'testname': [None],
            'stop_sim_on_bytes': ['inf'],
            'log_group_factor': [1000],
            'gen_ncq_depth_table': [True],
            'do_dump_lpn_sem': [True],
            'rm_blkparse_events': [False],
            }
    return para_dict



