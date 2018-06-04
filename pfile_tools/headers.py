# Part of the pfile-tools package
# Copyright (c) 2012, Board of Regents of the University of Wisconsin
# Written by Nathan Vack <njvack@wisc.edu>
#
# Contains the ctypes Structure for a GE P-file header.

from ctypes import *
import datetime


def REVISIONS():
    return {
        '16'    : R16PfileHeader,
        '20.006': R20_006PfileHeader,
        '20.007': R20_007PfileHeader,
        '24'    : R20_007PfileHeader,
        '26.002': R26_002PfileHeader,
    }


def format_short_float(f):
    """
    Formats 16.00 to 16 and 20.006000 to 20.006
    """
    return ("%.5f" % f).rstrip("0").rstrip(".")


def known_revisions():
    return [x for x in sorted(REVISIONS().keys())]


class Pfile(object):
    """
    The wrapper class for all manner of pfile header readin' structs.
    Really, only the one for now. Who knows, maybe ever?
    """

    def __init__(self, header, revision):
        self.header = header
        self.revision = revision
        for f in self.header._fields_:
            # Copy all the fields into this class.
            name = f[0]
            setattr(self, name, getattr(self.header, name))

    @property
    def exam_datetime(self):
        return datetime.datetime.utcfromtimestamp(self.exam_timestamp)

    @property
    def series_datetime(self):
        return datetime.datetime.utcfromtimestamp(self.series_timestamp)

    @classmethod
    def from_file(cls, infile, force_revision=None):
        filelike = infile
        if not hasattr('seek', filelike):
            filelike = open(filelike, 'rb')
        revision = force_revision or format_short_float(cls._major_revision(filelike))
        filelike.seek(0)
        rev_hash = REVISIONS()
        header_cls = rev_hash.get(revision)
        if header_cls is None:
            raise UnknownRevision("No header found for revision %s" % revision)
        header = header_cls()
        filelike.readinto(header)
        return cls(header, revision)

    @classmethod
    def _major_revision(cls, filelike):
        rnh = RevisionNum()
        filelike.seek(0)
        filelike.readinto(rnh)
        return rnh.revision


class UnknownRevision(RuntimeError):
    pass


class RevisionNum(LittleEndianStructure):

    _pack_ = 1

    _fields_ = [
        ('revision', c_float)]


class R16PfileHeader(LittleEndianStructure):

    _pack_ = 1

    _fields_ = [
        ('revision', c_float),
        ('pad_0', c_char * 12),
        ('scan_date_str', c_char * 10),
        ('scan_time_str', c_char * 8),
        ('pad_1', c_char * 30),
        ('pass_count', c_short),
        ('pad_2', c_char * 2),
        ('slice_count', c_ushort),
        ('echo_count', c_short),
        ('pad_3', c_char * 2),
        ('frame_count', c_short),
        ('pad_4', c_char * 4),
        ('frame_size', c_ushort),
        ('pad_5', c_char * 20),
        ('acq_x_res', c_ushort),
        ('acq_y_Res', c_short),
        ('recon_x_res', c_short),
        ('recon_y_res', c_short),
        ('image_size', c_short),
        ('recon_z_res', c_int),
        ('pad_6', c_char * 100),
        ('rh_user_0', c_float),
        ('rh_user_1', c_float),
        ('rh_user_2', c_float),
        ('rh_user_3', c_float),
        ('rh_user_4', c_float),
        ('rh_user_5', c_float),
        ('rh_user_6', c_float),
        ('rh_user_7', c_float),
        ('rh_user_8', c_float),
        ('rh_user_9', c_float),
        ('rh_user_10', c_float),
        ('rh_user_11', c_float),
        ('rh_user_12', c_float),
        ('rh_user_13', c_float),
        ('rh_user_14', c_float),
        ('rh_user_15', c_float),
        ('rh_user_16', c_float),
        ('rh_user_17', c_float),
        ('rh_user_18', c_float),
        ('rh_user_19', c_float),
        ('pad_7', c_char * 704),
        ('rh_user_20', c_float),
        ('rh_user_21', c_float),
        ('rh_user_22', c_float),
        ('rh_user_23', c_float),
        ('rh_user_24', c_float),
        ('rh_user_25', c_float),
        ('rh_user_26', c_float),
        ('rh_user_27', c_float),
        ('rh_user_28', c_float),
        ('rh_user_29', c_float),
        ('rh_user_30', c_float),
        ('rh_user_31', c_float),
        ('rh_user_32', c_float),
        ('rh_user_33', c_float),
        ('rh_user_34', c_float),
        ('rh_user_35', c_float),
        ('rh_user_36', c_float),
        ('rh_user_37', c_float),
        ('rh_user_38', c_float),
        ('rh_user_39', c_float),
        ('rh_user_40', c_float),
        ('rh_user_41', c_float),
        ('rh_user_42', c_float),
        ('rh_user_43', c_float),
        ('rh_user_44', c_float),
        ('rh_user_45', c_float),
        ('rh_user_46', c_float),
        ('rh_user_47', c_float),
        ('rh_user_48', c_float),
        ('pad_8', c_char * 528),
        ('bandwidth', c_float),
        ('pad_9', c_char * 12),
        ('data_size', c_ulong),
        ('ssp_save', c_ulong),
        ('uda_save', c_ulong),
        ('pad_10', c_char * 137214),
        ('aps_r1', c_int),
        ('aps_r2', c_int),
        ('aps_tg', c_int),
        ('aps_frequency', c_uint),
        ('scale_i', c_float),
        ('scale_q', c_float),
        ('pad_11', c_char * 276),
        ('x_shim', c_short),
        ('y_shim', c_short),
        ('z_shim', c_short),
        ('recon_enabled', c_short),
        ('pad_12', c_char * 1774),
        ('magnet_strength', c_int),
        ('patient_weight_g', c_int),
        ('exam_timestamp', c_int),
        ('pad_13', c_char * 52),
        ('exam_number', c_ushort),
        ('pad_14', c_char * 18),
        ('patient_age', c_short),
        ('pad_15', c_char * 2),
        ('patient_sex', c_short),
        ('pad_16', c_char * 2),
        ('patient_trauma', c_short),
        ('pad_17', c_char * 2),
        ('study_status', c_short),
        ('pad_18', c_char * 166),
        ('exam_description', c_char * 65),
        ('exam_type', c_char * 3),
        ('system_id', c_char * 9),
        ('pad_20', c_char * 14),
        ('hospital_name', c_char * 33),
        ('patient_id_2', c_char * 13),
        ('patient_name_2', c_char * 25),
        ('service_id', c_char * 16),
        ('pad_22', c_char * 124),
        ('patient_name', c_char * 65),
        ('patient_id', c_char * 65),
        ('req_num', c_char * 17),
        ('date_of_birth', c_char * 9),
        ('pad_23', c_char * 492),
        ('series_number', c_short),
        ('pad_26', c_char * 122),
        ('series_description', c_char * 65),
        ('pad_27', c_char * 21),
        ('protocol', c_char * 25),
        ('start_ras', c_char),
        ('end_ras', c_char),
        ('pad_28', c_char * 1541),
        ('x_field_of_view', c_float),
        ('y_field_of_view', c_float),
        ('scan_duration', c_float),
        ('z_thickness', c_float),
        ('pad_29', c_char * 36),
        ('op_user_0', c_float),
        ('op_user_1', c_float),
        ('op_user_2', c_float),
        ('op_user_3', c_float),
        ('op_user_4', c_float),
        ('op_user_5', c_float),
        ('op_user_6', c_float),
        ('op_user_7', c_float),
        ('op_user_8', c_float),
        ('op_user_9', c_float),
        ('op_user_10', c_float),
        ('op_user_11', c_float),
        ('op_user_12', c_float),
        ('op_user_13', c_float),
        ('op_user_14', c_float),
        ('op_user_15', c_float),
        ('op_user_16', c_float),
        ('op_user_17', c_float),
        ('op_user_18', c_float),
        ('op_user_19', c_float),
        ('op_user_20', c_float),
        ('op_user_21', c_float),
        ('op_user_22', c_float),
        ('pad_30', c_char * 8),
        ('op_user_23', c_float),
        ('op_user_24', c_float),
        ('pad_31', c_char * 60),
        ('op_user_25', c_float),
        ('op_user_26', c_float),
        ('op_user_27', c_float),
        ('op_user_28', c_float),
        ('op_user_29', c_float),
        ('op_user_30', c_float),
        ('op_user_31', c_float),
        ('op_user_32', c_float),
        ('op_user_33', c_float),
        ('op_user_34', c_float),
        ('op_user_35', c_float),
        ('op_user_36', c_float),
        ('op_user_37', c_float),
        ('op_user_38', c_float),
        ('op_user_39', c_float),
        ('op_user_40', c_float),
        ('op_user_41', c_float),
        ('op_user_42', c_float),
        ('op_user_43', c_float),
        ('op_user_44', c_float),
        ('op_user_45', c_float),
        ('op_user_46', c_float),
        ('op_user_47', c_float),
        ('op_user_48', c_float),
        ('pad_32', c_char * 60),
        ('x_dim', c_float),
        ('y_dim', c_float),
        ('x_size', c_float),
        ('y_size', c_float),
        ('r_center', c_float),
        ('a_center', c_float),
        ('s_center', c_float),
        ('r_norm', c_float),
        ('a_norm', c_float),
        ('s_norm', c_float),
        ('pad_33', c_char * 232),
        ('tr', c_int),
        ('ti', c_int),
        ('te', c_int),
        ('pad_34', c_char * 548),
        ('psd_name', c_char * 33),
        ('pad_36', c_char * 84),
        ('coil_name', c_char * 17),
        ('pad_37', c_char * 115),
        ('long_coil_name', c_char * 24)]


class R20_006PfileHeader(LittleEndianStructure):

    _pack_ = 1

    _fields_ = [
        ('revision', c_float),
        ('pad_0', c_char * 12),
        ('scan_date_str', c_char * 10),
        ('scan_time_str', c_char * 8),
        ('pad_1', c_char * 30),
        ('pass_count', c_short),
        ('pad_2', c_char * 2),
        ('slice_count', c_ushort),
        ('echo_count', c_short),
        ('pad_3', c_char * 2),
        ('frame_count', c_short),
        ('pad_4', c_char * 4),
        ('frame_size', c_ushort),
        ('pad_5', c_char * 20),
        ('acq_x_res', c_ushort),
        ('acq_y_Res', c_short),
        ('recon_x_res', c_short),
        ('recon_y_res', c_short),
        ('image_size', c_short),
        ('recon_z_res', c_int),
        ('pad_6', c_char * 100),
        ('rh_user_0', c_float),
        ('rh_user_1', c_float),
        ('rh_user_2', c_float),
        ('rh_user_3', c_float),
        ('rh_user_4', c_float),
        ('rh_user_5', c_float),
        ('rh_user_6', c_float),
        ('rh_user_7', c_float),
        ('rh_user_8', c_float),
        ('rh_user_9', c_float),
        ('rh_user_10', c_float),
        ('rh_user_11', c_float),
        ('rh_user_12', c_float),
        ('rh_user_13', c_float),
        ('rh_user_14', c_float),
        ('rh_user_15', c_float),
        ('rh_user_16', c_float),
        ('rh_user_17', c_float),
        ('rh_user_18', c_float),
        ('rh_user_19', c_float),
        ('pad_7', c_char * 704),
        ('rh_user_20', c_float),
        ('rh_user_21', c_float),
        ('rh_user_22', c_float),
        ('rh_user_23', c_float),
        ('rh_user_24', c_float),
        ('rh_user_25', c_float),
        ('rh_user_26', c_float),
        ('rh_user_27', c_float),
        ('rh_user_28', c_float),
        ('rh_user_29', c_float),
        ('rh_user_30', c_float),
        ('rh_user_31', c_float),
        ('rh_user_32', c_float),
        ('rh_user_33', c_float),
        ('rh_user_34', c_float),
        ('rh_user_35', c_float),
        ('rh_user_36', c_float),
        ('rh_user_37', c_float),
        ('rh_user_38', c_float),
        ('rh_user_39', c_float),
        ('rh_user_40', c_float),
        ('rh_user_41', c_float),
        ('rh_user_42', c_float),
        ('rh_user_43', c_float),
        ('rh_user_44', c_float),
        ('rh_user_45', c_float),
        ('rh_user_46', c_float),
        ('rh_user_47', c_float),
        ('rh_user_48', c_float),
        ('pad_8', c_char * 528),
        ('bandwidth', c_float),
        ('pad_9', c_char * 12),
        ('data_size', c_ulong),
        ('ssp_save', c_ulong),
        ('uda_save', c_ulong),
        ('pad_10', c_char * 139656),
        ('aps_r1', c_int),
        ('aps_r2', c_int),
        ('aps_tg', c_int),
        ('aps_frequency', c_uint),
        ('scale_i', c_float),
        ('scale_q', c_float),
        ('pad_11', c_char * 276),
        ('x_shim', c_short),
        ('y_shim', c_short),
        ('z_shim', c_short),
        ('recon_enabled', c_short),
        ('pad_12', c_char * 1744),
        ('magnet_strength', c_int),
        ('patient_weight_g', c_int),
        ('exam_timestamp', c_int),
        ('pad_13', c_char * 112),
        ('exam_number', c_ushort),
        ('pad_14', c_char * 18),
        ('patient_age', c_short),
        ('pad_15', c_char * 2),
        ('patient_sex', c_short),
        ('pad_16', c_char * 2),
        ('patient_trauma', c_short),
        ('pad_17', c_char * 2),
        ('study_status', c_short),
        ('pad_18', c_char * 70),
        ('history', c_char * 257),
        ('pad_19', c_char * 195),
        ('exam_description', c_char * 65),
        ('exam_type', c_char * 3),
        ('system_id', c_char * 9),
        ('pad_20', c_char * 14),
        ('hospital_name', c_char * 33),
        ('pad_21', c_char * 24),
        ('service_id', c_char * 16),
        ('pad_22', c_char * 100),
        ('patient_name', c_char * 65),
        ('patient_id', c_char * 65),
        ('req_num', c_char * 17),
        ('date_of_birth', c_char * 9),
        ('pad_23', c_char * 560),
        ('start_location', c_float),
        ('end_location', c_float),
        ('pad_24', c_char * 352),
        ('series_timestamp', c_int),
        ('pad_25', c_char * 206),
        ('series_number', c_short),
        ('pad_26', c_char * 138),
        ('series_description', c_char * 65),
        ('pad_27', c_char * 21),
        ('protocol', c_char * 25),
        ('start_ras', c_char),
        ('end_ras', c_char),
        ('pad_28', c_char * 1769),
        ('x_field_of_view', c_float),
        ('y_field_of_view', c_float),
        ('scan_duration', c_float),
        ('z_thickness', c_float),
        ('pad_29', c_char * 36),
        ('op_user_0', c_float),
        ('op_user_1', c_float),
        ('op_user_2', c_float),
        ('op_user_3', c_float),
        ('op_user_4', c_float),
        ('op_user_5', c_float),
        ('op_user_6', c_float),
        ('op_user_7', c_float),
        ('op_user_8', c_float),
        ('op_user_9', c_float),
        ('op_user_10', c_float),
        ('op_user_11', c_float),
        ('op_user_12', c_float),
        ('op_user_13', c_float),
        ('op_user_14', c_float),
        ('op_user_15', c_float),
        ('op_user_16', c_float),
        ('op_user_17', c_float),
        ('op_user_18', c_float),
        ('op_user_19', c_float),
        ('op_user_20', c_float),
        ('op_user_21', c_float),
        ('op_user_22', c_float),
        ('pad_30', c_char * 8),
        ('op_user_23', c_float),
        ('op_user_24', c_float),
        ('pad_31', c_char * 60),
        ('op_user_25', c_float),
        ('op_user_26', c_float),
        ('op_user_27', c_float),
        ('op_user_28', c_float),
        ('op_user_29', c_float),
        ('op_user_30', c_float),
        ('op_user_31', c_float),
        ('op_user_32', c_float),
        ('op_user_33', c_float),
        ('op_user_34', c_float),
        ('op_user_35', c_float),
        ('op_user_36', c_float),
        ('op_user_37', c_float),
        ('op_user_38', c_float),
        ('op_user_39', c_float),
        ('op_user_40', c_float),
        ('op_user_41', c_float),
        ('op_user_42', c_float),
        ('op_user_43', c_float),
        ('op_user_44', c_float),
        ('op_user_45', c_float),
        ('op_user_46', c_float),
        ('op_user_47', c_float),
        ('op_user_48', c_float),
        ('pad_32', c_char * 60),
        ('x_dim', c_float),
        ('y_dim', c_float),
        ('x_size', c_float),
        ('y_size', c_float),
        ('r_center', c_float),
        ('a_center', c_float),
        ('s_center', c_float),
        ('r_norm', c_float),
        ('a_norm', c_float),
        ('s_norm', c_float),
        ('pad_33', c_char * 336),
        ('tr', c_int),
        ('ti', c_int),
        ('te', c_int),
        ('pad_34', c_char * 432),
        ('frequency_direction', c_short),
        ('pad_35', c_char * 130),
        ('psd_name', c_char * 33),
        ('pad_36', c_char * 84),
        ('coil_name', c_char * 17),
        ('pad_37', c_char * 115),
        ('long_coil_name', c_char * 24),
        ('pad_38', c_char * 543)]

class R20_007PfileHeader(LittleEndianStructure):

    _pack_ = 1

    _fields_ = [
        ('revision', c_float),
        ('pad_0', c_char * 12),
        ('scan_date_str', c_char * 10),
        ('scan_time_str', c_char * 8),
        ('pad_0p', c_char * 14),
        ('dacq_ctrl', c_short),         # phase encoding gradient polarity
        ('pad_1', c_char * 14),
        ('pass_count', c_short),
        ('pad_2', c_char * 2),
        ('slice_count', c_ushort),
        ('echo_count', c_short),
        ('pad_3', c_char * 2),
        ('frame_count', c_short),
        ('pad_4', c_char * 4),
        ('frame_size', c_ushort),
        ('pad_5', c_char * 20),
        ('acq_x_res', c_ushort),
        ('acq_y_Res', c_short),
        ('recon_x_res', c_short),
        ('recon_y_res', c_short),
        ('image_size', c_short),
        ('recon_z_res', c_int),
        ('pad_6', c_char * 100),
        ('rh_user_0', c_float),
        ('rh_user_1', c_float),
        ('rh_user_2', c_float),
        ('rh_user_3', c_float),
        ('rh_user_4', c_float),
        ('rh_user_5', c_float),
        ('rh_user_6', c_float),
        ('rh_user_7', c_float),
        ('rh_user_8', c_float),
        ('rh_user_9', c_float),
        ('rh_user_10', c_float),
        ('rh_user_11', c_float),
        ('rh_user_12', c_float),
        ('rh_user_13', c_float),
        ('rh_user_14', c_float),
        ('rh_user_15', c_float),
        ('rh_user_16', c_float),
        ('rh_user_17', c_float),
        ('rh_user_18', c_float),
        ('rh_user_19', c_float),
        ('pad_7', c_char * 704),
        ('rh_user_20', c_float),
        ('rh_user_21', c_float),
        ('rh_user_22', c_float),
        ('rh_user_23', c_float),
        ('rh_user_24', c_float),
        ('rh_user_25', c_float),
        ('rh_user_26', c_float),
        ('rh_user_27', c_float),
        ('rh_user_28', c_float),
        ('rh_user_29', c_float),
        ('rh_user_30', c_float),
        ('rh_user_31', c_float),
        ('rh_user_32', c_float),
        ('rh_user_33', c_float),
        ('rh_user_34', c_float),
        ('rh_user_35', c_float),
        ('rh_user_36', c_float),
        ('rh_user_37', c_float),
        ('rh_user_38', c_float),
        ('rh_user_39', c_float),
        ('rh_user_40', c_float),
        ('rh_user_41', c_float),
        ('rh_user_42', c_float),
        ('rh_user_43', c_float),
        ('rh_user_44', c_float),
        ('rh_user_45', c_float),
        ('rh_user_46', c_float),
        ('rh_user_47', c_float),
        ('rh_user_48', c_float),
        ('pad_8', c_char * 528),
        ('bandwidth', c_float),
        ('pad_9', c_char * 12),
        ('data_size', c_ulong),
        ('ssp_save', c_ulong),
        ('uda_save', c_ulong),
        ('pad_9p', c_char * 980),
        ('num_difdirs', c_short),       # number of diffusion directions
        ('pad_10', c_char * 138674),
        ('aps_r1', c_int),
        ('aps_r2', c_int),
        ('aps_tg', c_int),
        ('aps_frequency', c_uint),
        ('scale_i', c_float),
        ('scale_q', c_float),
        ('pad_11', c_char * 276),
        ('x_shim', c_short),
        ('y_shim', c_short),
        ('z_shim', c_short),
        ('recon_enabled', c_short),
        ('pad_12', c_char * 1744),
        ('magnet_strength', c_int),
        ('patient_weight_g', c_int),
        ('exam_timestamp', c_int),
        ('pad_13', c_char * 112),
        ('exam_number', c_ushort),
        ('pad_14', c_char * 18),
        ('patient_age', c_short),
        ('pad_15', c_char * 2),
        ('patient_sex', c_short),
        ('pad_16', c_char * 2),
        ('patient_trauma', c_short),
        ('pad_17', c_char * 2),
        ('study_status', c_short),
        ('pad_18', c_char * 70),
        ('history', c_char * 257),
        ('referring_physicians_name', c_char * 65),
        ('radiologists_name', c_char * 65),
        ('operators_name', c_char * 65),
        ('exam_description', c_char * 65),
        ('exam_type', c_char * 3),
        ('system_id', c_char * 9),
        ('pad_20', c_char * 22),
        ('hospital_name', c_char * 33),
        ('pad_21', c_char * 24),
        ('service_id', c_char * 16),
        ('pad_22', c_char * 100),
        ('patient_name', c_char * 65),
        ('patient_id', c_char * 65),
        ('req_num', c_char * 17),
        ('date_of_birth', c_char * 9),
        ('pad_23', c_char * 552),
        ('start_location', c_float),
        ('end_location', c_float),
        ('pad_24', c_char * 352),
        ('series_timestamp', c_int),
        ('pad_25', c_char * 206),
        ('series_number', c_short),
        ('pad_26', c_char * 138),
        ('series_description', c_char * 65),
        ('pad_27', c_char * 21),
        ('protocol', c_char * 25),
        ('start_ras', c_char),
        ('end_ras', c_char),
        ('pad_28', c_char * 1769),
        ('x_field_of_view', c_float),
        ('y_field_of_view', c_float),
        ('scan_duration', c_float),
        ('z_thickness', c_float),
        ('pad_29', c_char * 36),
        ('op_user_0', c_float),
        ('op_user_1', c_float),
        ('op_user_2', c_float),
        ('op_user_3', c_float),
        ('op_user_4', c_float),
        ('op_user_5', c_float),
        ('op_user_6', c_float),
        ('op_user_7', c_float),
        ('op_user_8', c_float),
        ('op_user_9', c_float),
        ('op_user_10', c_float),
        ('op_user_11', c_float),
        ('op_user_12', c_float),
        ('op_user_13', c_float),
        ('op_user_14', c_float),
        ('op_user_15', c_float),
        ('op_user_16', c_float),
        ('op_user_17', c_float),
        ('op_user_18', c_float),
        ('op_user_19', c_float),
        ('op_user_20', c_float),
        ('op_user_21', c_float),
        ('op_user_22', c_float),
        ('pad_30', c_char * 8),
        ('op_user_23', c_float),
        ('op_user_24', c_float),
        ('pad_31', c_char * 60),
        ('op_user_25', c_float),
        ('op_user_26', c_float),
        ('op_user_27', c_float),
        ('op_user_28', c_float),
        ('op_user_29', c_float),
        ('op_user_30', c_float),
        ('op_user_31', c_float),
        ('op_user_32', c_float),
        ('op_user_33', c_float),
        ('op_user_34', c_float),
        ('op_user_35', c_float),
        ('op_user_36', c_float),
        ('op_user_37', c_float),
        ('op_user_38', c_float),
        ('op_user_39', c_float),
        ('op_user_40', c_float),
        ('op_user_41', c_float),
        ('op_user_42', c_float),
        ('op_user_43', c_float),
        ('op_user_44', c_float),
        ('op_user_45', c_float),
        ('op_user_46', c_float),
        ('op_user_47', c_float),
        ('op_user_48', c_float),
        ('pad_32', c_char * 60),
        ('x_dim', c_float),
        ('y_dim', c_float),
        ('x_size', c_float),
        ('y_size', c_float),
        ('r_center', c_float),
        ('a_center', c_float),
        ('s_center', c_float),
        ('r_norm', c_float),
        ('a_norm', c_float),
        ('s_norm', c_float),
        ('pad_33', c_char * 336),
        ('tr', c_int),
        ('ti', c_int),
        ('te', c_int),
        ('pad_33p', c_char * 374),
        ('num_slices', c_short),        # number of slices per TR
        ('pad_34', c_char * 56),
        ('frequency_direction', c_short),
        ('pad_35', c_char * 130),
        ('psd_name', c_char * 33),
        ('pad_36', c_char * 84),
        ('coil_name', c_char * 17),
        ('pad_37', c_char * 115),
        ('long_coil_name', c_char * 24),
        ('pad_38', c_char * 543)]


class R26_002PfileHeader(LittleEndianStructure):

    _pack_ = 1

    _fields_ = [
        ('revision', c_float),
        ('pad_0', c_char * 88),
        ('scan_date_str', c_char * 10),
        ('scan_time_str', c_char * 8),
        ('pad_0p', c_char * 14),
        ('dacq_ctrl', c_short),         # phase encoding gradient polarity
        ('pad_1', c_char * 14),
        ('pass_count', c_short),
        ('pad_2', c_char * 2),
        ('slice_count', c_ushort),
        ('echo_count', c_short),
        ('pad_3', c_char * 2),
        ('frame_count', c_short),
        ('pad_4', c_char * 4),
        ('frame_size', c_ushort),
        ('pad_5', c_char * 20),
        ('acq_x_res', c_ushort),
        ('acq_y_Res', c_short),
        ('recon_x_res', c_short),
        ('recon_y_res', c_short),
        ('image_size', c_short),
        ('recon_z_res', c_int),
        ('pad_6', c_char * 88),         # 100
        ('rh_user_0', c_float),
        ('rh_user_1', c_float),
        ('rh_user_2', c_float),
        ('rh_user_3', c_float),
        ('rh_user_4', c_float),
        ('rh_user_5', c_float),
        ('rh_user_6', c_float),
        ('rh_user_7', c_float),
        ('rh_user_8', c_float),
        ('rh_user_9', c_float),
        ('rh_user_10', c_float),
        ('rh_user_11', c_float),
        ('rh_user_12', c_float),
        ('rh_user_13', c_float),
        ('rh_user_14', c_float),
        ('rh_user_15', c_float),
        ('rh_user_16', c_float),
        ('rh_user_17', c_float),
        ('rh_user_18', c_float),
        ('rh_user_19', c_float),
        ('pad_7', c_char * 576),        # 704
        ('rh_user_20', c_float),
        ('rh_user_21', c_float),
        ('rh_user_22', c_float),
        ('rh_user_23', c_float),
        ('rh_user_24', c_float),
        ('rh_user_25', c_float),
        ('rh_user_26', c_float),
        ('rh_user_27', c_float),
        ('rh_user_28', c_float),
        ('rh_user_29', c_float),
        ('rh_user_30', c_float),
        ('rh_user_31', c_float),
        ('rh_user_32', c_float),
        ('rh_user_33', c_float),
        ('rh_user_34', c_float),
        ('rh_user_35', c_float),
        ('rh_user_36', c_float),
        ('rh_user_37', c_float),
        ('rh_user_38', c_float),
        ('rh_user_39', c_float),
        ('rh_user_40', c_float),
        ('rh_user_41', c_float),
        ('rh_user_42', c_float),
        ('rh_user_43', c_float),
        ('rh_user_44', c_float),
        ('rh_user_45', c_float),
        ('rh_user_46', c_float),
        ('rh_user_47', c_float),
        ('rh_user_48', c_float),
        ('pad_8', c_char * 480),        # 528
        ('bandwidth', c_float),
        ('pad_9', c_char * 4),          # 12
        ('data_size', c_ulong),
        ('ssp_save', c_ulong),
        ('uda_save', c_ulong),
        ('pad_9p', c_char * 36),
        ('num_difdirs', c_short),       # number of diffusion directions
        ('pad_10', c_char * 188890),    # (139618 + 50764)
        ('aps_r1', c_int),
        ('aps_r2', c_int),
        ('aps_tg', c_int),
        ('aps_frequency', c_uint),
        ('scale_i', c_float),
        ('scale_q', c_float),
        ('pad_11', c_char * 276),
        ('x_shim', c_short),
        ('y_shim', c_short),
        ('z_shim', c_short),
        ('recon_enabled', c_short),
        ('pad_12', c_char * 3432),      # 1744
        ('magnet_strength', c_int),
        ('patient_weight_g', c_int),
        ('exam_timestamp', c_int),
        ('pad_13', c_char * 112),
        ('exam_number', c_ushort),
        ('pad_14', c_char * 18),
        ('patient_age', c_short),
        ('pad_15', c_char * 2),
        ('patient_sex', c_short),
        ('pad_16', c_char * 2),
        ('patient_trauma', c_short),
        ('pad_17', c_char * 2),
        ('study_status', c_short),
        ('pad_18', c_char * 70),
        ('history', c_char * 257),
        ('referring_physicians_name', c_char * 65),
        ('radiologists_name', c_char * 65),
        ('operators_name', c_char * 65),
        ('exam_description', c_char * 65),
        ('exam_type', c_char * 3),
        ('system_id', c_char * 9),
        ('pad_20', c_char * 22),
        ('hospital_name', c_char * 33),
        ('pad_21', c_char * 24),
        ('service_id', c_char * 16),
        ('pad_22', c_char * 100),
        ('patient_name', c_char * 65),
        ('patient_id', c_char * 65),
        ('req_num', c_char * 17),
        ('date_of_birth', c_char * 9),
        ('pad_23', c_char * 552),
        ('start_location', c_float),
        ('end_location', c_float),
        ('pad_24', c_char * 352),
        ('series_timestamp', c_int),
        ('pad_25', c_char * 100),       # 206
        ('series_number', c_int),       # c_short
        ('pad_26', c_char * 242),       # 138
        ('series_description', c_char * 65),
        ('pad_27', c_char * 21),
        ('protocol', c_char * 25),
        ('start_ras', c_char),
        ('end_ras', c_char),
        ('pad_28', c_char * 1769),
        ('x_field_of_view', c_float),
        ('y_field_of_view', c_float),
        ('scan_duration', c_float),
        ('z_thickness', c_float),
        ('pad_29', c_char * 36),
        ('op_user_0', c_float),
        ('op_user_1', c_float),
        ('op_user_2', c_float),
        ('op_user_3', c_float),
        ('op_user_4', c_float),
        ('op_user_5', c_float),
        ('op_user_6', c_float),
        ('op_user_7', c_float),
        ('op_user_8', c_float),
        ('op_user_9', c_float),
        ('op_user_10', c_float),
        ('op_user_11', c_float),
        ('op_user_12', c_float),
        ('op_user_13', c_float),
        ('op_user_14', c_float),
        ('op_user_15', c_float),
        ('op_user_16', c_float),
        ('op_user_17', c_float),
        ('op_user_18', c_float),
        ('op_user_19', c_float),
        ('op_user_20', c_float),
        ('op_user_21', c_float),
        ('op_user_22', c_float),
        ('pad_30', c_char * 8),
        ('op_user_23', c_float),
        ('op_user_24', c_float),
        ('pad_31', c_char * 60),
        ('op_user_25', c_float),
        ('op_user_26', c_float),
        ('op_user_27', c_float),
        ('op_user_28', c_float),
        ('op_user_29', c_float),
        ('op_user_30', c_float),
        ('op_user_31', c_float),
        ('op_user_32', c_float),
        ('op_user_33', c_float),
        ('op_user_34', c_float),
        ('op_user_35', c_float),
        ('op_user_36', c_float),
        ('op_user_37', c_float),
        ('op_user_38', c_float),
        ('op_user_39', c_float),
        ('op_user_40', c_float),
        ('op_user_41', c_float),
        ('op_user_42', c_float),
        ('op_user_43', c_float),
        ('op_user_44', c_float),
        ('op_user_45', c_float),
        ('op_user_46', c_float),
        ('op_user_47', c_float),
        ('op_user_48', c_float),
        ('pad_32', c_char * 60),
        ('x_dim', c_float),
        ('y_dim', c_float),
        ('x_size', c_float),
        ('y_size', c_float),
        ('r_center', c_float),
        ('a_center', c_float),
        ('s_center', c_float),
        ('r_norm', c_float),
        ('a_norm', c_float),
        ('s_norm', c_float),
        ('pad_33', c_char * 336),
        ('tr', c_int),
        ('ti', c_int),
        ('te', c_int),
        ('pad_33p', c_char * 374),
        ('num_slices', c_short),        # number of slices per TR
        ('pad_34', c_char * 56),
        ('frequency_direction', c_short),
        ('pad_35', c_char * 130),
        ('psd_name', c_char * 33),
        ('pad_36', c_char * 84),
        ('coil_name', c_char * 17),
        ('pad_37', c_char * 115),
        ('long_coil_name', c_char * 24),
        ('pad_38', c_char * 543)]
