
import xlrd

class BaseModel(object):
    def __init__(self, key_list):
        self.key_list = key_list

    class Meta:
        excel_map = {}

    @classmethod
    def as_model(cls, dct):
        if not isinstance(dct, dict):
            return dct

    @classmethod
    def from_list(cls, value_list):
        if not isinstance(value_list, list):
            return value_list

        kls = cls()
        for key, value in zip(key_list, value_list):
            kls.__dict__[excel_map[key]] = value
        return kls

class BatterModel(BaseModel):
    class Meta:
        excel_map = {
            'ID' : 'id',
            'NAME' : 'name',
            'POS TO USE' : 'pos_to_use',
            'BATS' : 'bats',
            'C' : 'c',
            '1B' : '1b',
            '2B' : '2b',
            '3B' : '3b',
            'SS' : 'ss',
            'LF' : 'lf',
            'CF' : 'cf',
            'RF' : 'rf',
            'C ARM RATING' : 'c_arm_rating',
            'OF ARM RATING' : 'of_arm_rating',
            'STEAL RATING' : 'steal_rating',
            'BUNT RATING' : 'bunt_ratin',
            'HIT & RUN RATING' : 'hit_and_run_rating',
            'RUN ABILITY' : 'run_ability',
            'RUN SUPPLEMENT-STEAL' : 'run_supplemental_steal',
            'BAL' : 'bal',
            'LEFT%' : 'left_pct',
            'POWER (L/R)' : 'power_lr',
            'INJURY FREQUENCY' : 'injury_freq',
            'vsL All Other' : 'vs_l_else',
            'vsL GB - DP' : 'vs_l_gb_dp',
            'vsL Strike Out' : 'vs_l_strike_out',
            'vsL HBP' : 'vs_l_hbp',
            'vsL Walk' : 'vs_l_walk',
            'vsL Single' : 'vs_l_single',
            'vsL Double' : 'vs_l_double',
            'vsL Triple' : 'vs_l_triple',
            'vsL Home Run' : 'vs_l_home_run',
            'vsL On Base' : 'vs_l_obp',
            'vsL Extra Base' : 'vs_l_extra_base',
            'vsL Man on 1st Adv' : 'vs_l_man_on_first_adv',
            'vsL Sac Fly' : 'vs_l_sac_fly',
            'vsL Clutch Rating' : 'vs_l_clutch_rating',
            'vsL Ballpark Diamonds' : 'vs_l_ballpark_diamonds',
            'vsR All Other' : 'vs_l_all_other',
            'vsR GB - DP' : 'rs_r_gb_dp',
            'vsR Strike Out' : 'vs_r_strike_out',
            'vsR HBP' : 'vs_r_hbp',
            'vsR Walk' : 'vs_r_walk',
            'vsR Single' : 'vs_r_single',
            'vsR Double' : 'vs_r_double',
            'vsR Triple' : 'vs_r_triple',
            'vsR Home Run' : 'vs_r_home_run',
            'vsR On Base' : 'vs_r_obp',
            'vsR Extra Base' : 'vs_r_extra_base',
            'vsR Man on 1st Adv' : 'vs_r_man_on_first_adv',
            'vsR Sac Fly' : 'vs_r_sac_fly',
            'vsR Clutch Rating' : 'vs_r_clutch_rating',
            'vsR Ballpark Diamonds' : 'vs_r_ballpark_diamons',
        }

class PitcherModel(BaseModel):
    class Meta:
        excel_map = {
            'ID' : 'id',
            'NAME' : 'name',
            'POS TO USE' : 'pos_to_use',
            'THROWS' : 'throws',
            'STARTER IP' : 'starter_ip',
            'RELIEF IP' : 'relief_ip',
            'CLOSER RATING' : 'closer_rating',
            'HOLD RATING' : 'hold_rating',
            'FIELD RATING' : 'field_rating',
            'STEAL RATING' : 'steal_rating',
            'BUNT RATING' : 'bunt_rating',
            'RUN ABILITY' : 'run_ability',
            'BATS' : 'bats',
            'BATTING CARD' : 'batting_card',
            'BAL' : 'bal',
            'LEFT%' : 'left_pct',
            'POWER' : 'power_',
            'vsL All Other' : 'vs_l_all_other',
            'vsL GB - DP' : 'vs_l_gb_dp',
            'vsL Strike Out' : 'vs_l_strike_out',
            'vsL Walk' : 'vs_l_walk',
            'vsL Single' : 'vs_l_single',
            'vsL Double' : 'vs_l_double',
            'vsL Triple' : 'vs_l_triple',
            'vsL Home Run' : 'vs_l_home_run',
            'vsL On Base' : 'vs_l_obp',
            'vsL Extra Base' : 'vs_l_extra_base',
            'vsL Man on 1st Adv' : 'vs_l_man_on_first_adv',
            'vsL Sac Fly' : 'vs_l_sac_fly',
            'vsL Ballpark Diamonds' : 'vs_l_ballpark_diamonds',
            'vsL Best Results' : 'vs_l_best_results',
            'vsL POW Bullets' : 'vs_l_pow_bullets',
            'vsR All Other' : 'vs_r_all_other',
            'vsR GB - DP' : 'vs_r_gb_dp',
            'vsR Strike Out' : 'vs_r_strike_out',
            'vsR Walk' : 'vs_r_walk',
            'vsR Single' : 'vs_r_single',
            'vsR Double' : 'vs_r_double',
            'vsR Triple' : 'vs_r_triple',
            'vsR Home Run' : 'vs_r_home_run',
            'vsR On Base' : 'vs_r_obp',
            'vsR Extra Base' : 'vs_r_extra_base',
            'vsR Man on 1st Adv' : 'vs_r_man_on_first_adv',
            'vsR Sac Fly' : 'vs_r_sac_fly',
            'vsR Ballpark Diamonds' : 'vs_r_ballpark_diamonds',
            'vsR Best Results' : 'vs_r_best_results',
            'vsR POW Bullets' : 'vs_r_pow_bullets',
        }
