import xlrd

N_LEFTY_PITCHERS = 6
N_RIGHTY_PITCHERS = 26
N_PITCHERS = N_LEFTY_PITCHERS + N_RIGHTY_PITCHERS

class BaseModel(object):
    def __init__(self):
        return

    class Meta:
        excel_map = {}

    @classmethod
    def as_model(cls, dct):
        if not isinstance(dct, dict):
            return dct

    @classmethod
    def from_list(cls, key_list, value_list):
        if not isinstance(value_list, list):
            return value_list

        kls = cls()
        for key, value in zip(key_list, value_list):
            kls.__dict__[kls.Meta.excel_map[key]] = value
        return kls

class HOFModel(BaseModel):
    @property
    def eligible_season(self):
        return self.id.split('-')[0]

    @property
    def primary_position(self):
        return self.id.split('-')[1]

    @property
    def first_mlb_season(self):
        return self.id.split('-')[2]

    @property
    def alpha_id(self):
        return self.id.split('-')[3]

    @classmethod
    def field_rating(value):
        return value / 100 if len(value) else None

    @classmethod
    def error_rating(value):
        return value % 100 if len(value) else None

class BatterModel(HOFModel):
    def __init__(self):
        self.vs_l_ops_plus = 0.0
        self.vs_r_ops_plus = 0.0

    class Meta:
        excel_map = {
            'ID' : 'id',
            'NAME' : 'name',
            'POS TO USE' : 'pos_to_use',
            'BATS' : 'bats',
            'C' : 'catcher',
            '1B' : 'first',
            '2B' : 'second',
            '3B' : 'third',
            'SS' : 'short',
            'LF' : 'left',
            'CF' : 'center',
            'RF' : 'right',
            'C ARM RATING' : 'c_arm_rating',
            'OF ARM RATING' : 'of_arm_rating',
            'STEAL RATING' : 'steal_rating',
            'BUNT RATING' : 'bunt_rating',
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

    def __repr__(self):
        return '{}: {}: {}: {}'.format(self.eligible_season, self.name, self.pos_to_use, self.ops_plus)

    @property
    def ops_plus(self):
        return int((N_LEFTY_PITCHERS*self.vs_l_ops_plus + N_RIGHTY_PITCHERS*self.vs_r_ops_plus) / N_PITCHERS)

    def is_rated_for_position(self, position=0):
        if position == 2:
            return self.catcher != None and len(self.catcher)
        elif position == 3:
            return self.first != None and len(self.first)
        elif position == 4:
            return self.second != None and len(self.second)
        elif position == 5:
            return self.third != None and len(self.third)
        elif position == 6:
            return self.short != None and len(self.short)
        elif position == 7:
            return self.left != None and len(self.left)
        elif position == 8:
            return self.center != None and len(self.center)
        elif position == 9:
            return self.right != None and len(self.right)

    @property
    def catcher_field_rating(self):
        return BatterModel.field_rating(self.catcher)

    @property
    def catcher_error_rating(self):
        return BatterModel.error_rating(self.catcher)

class HOFBatters(object):
    def __init__(self, sheet, season=None):
        key_row = sheet.row(0)
        key_list = [sheet.cell_value(0, col_index) for col_index in xrange(sheet.ncols)]

        self.batters = []
        for row in xrange(1, sheet.nrows):
            value_list = [sheet.cell_value(row, col_index) for col_index in xrange(sheet.ncols)]
            batter = BatterModel.from_list(key_list, value_list)
            self.batters.append(batter)

        if season is not None:
            self.batters = [b for b in self.batters if b.eligible_season == season]

        sum_vs_l_obp = sum_vs_r_obp = 0.0
        sum_vs_l_slg = sum_vs_r_slg = 0.0
        for batter in self.batters:
            sum_vs_l_obp += batter.vs_l_obp
            sum_vs_r_obp += batter.vs_r_obp
            sum_vs_l_slg += batter.vs_l_extra_base
            sum_vs_r_slg += batter.vs_r_extra_base
        self.vs_l_lg_obp = sum_vs_l_obp / len(self.batters)
        self.vs_r_lg_obp = sum_vs_r_obp / len(self.batters)
        self.vs_l_lg_slg = sum_vs_l_slg / len(self.batters)
        self.vs_r_lg_slg = sum_vs_r_slg / len(self.batters)

        for batter in self.batters:
            batter.vs_l_ops_plus = 100 * ((batter.vs_l_obp/self.vs_l_lg_obp) + (batter.vs_l_extra_base/self.vs_l_lg_slg) - 1)
            batter.vs_r_ops_plus = 100 * ((batter.vs_r_obp/self.vs_r_lg_obp) + (batter.vs_r_extra_base/self.vs_r_lg_slg) - 1)

    @property
    def n_left(self):
        return len([b for b in self.batters if b.bats == 'L'])

    @property
    def n_right(self):
        return len([b for b in self.batters if b.bats == 'R'])

    @property
    def n_switch(self):
        return len([b for b in self.batters if b.bats == 'S'])

class PitcherModel(HOFModel):
    def __init__(self):
        self.vs_l_ops_plus = 0.0
        self.vs_r_ops_plus = 0.0

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

    def __repr__(self):
        return '{}: {}: {}: {}'.format(self.eligible_season, self.throws, self.name, self.ops_plus)

    @property
    def ops_plus(self):
        return int((self.vs_l_ops_plus + self.vs_r_ops_plus) / 2.0)

    def field_rating(self):
        return PitcherModel.field_rating(self.field_rating)

    def error_rating(self):
        return PitcherModel.error_rating(self.field_rating)

class HOFPitchers(object):
    def __init__(self, sheet, season=None):
        key_row = sheet.row(0)
        key_list = [sheet.cell_value(0, col_index) for col_index in xrange(sheet.ncols)]

        self.pitchers = []
        for row in xrange(1, sheet.nrows):
            value_list = [sheet.cell_value(row, col_index) for col_index in xrange(sheet.ncols)]
            pitcher = PitcherModel.from_list(key_list, value_list)
            self.pitchers.append(pitcher)

        if season is not None:
            self.pitchers = [p for p in self.pitchers if p.eligible_season == season]

        sum_vs_l_obp = sum_vs_r_obp = 0.0
        sum_vs_l_slg = sum_vs_r_slg = 0.0
        for pitcher in self.pitchers:
            sum_vs_l_obp += pitcher.vs_l_obp
            sum_vs_r_obp += pitcher.vs_r_obp
            sum_vs_l_slg += pitcher.vs_l_extra_base
            sum_vs_r_slg += pitcher.vs_r_extra_base
        self.vs_l_lg_obp = sum_vs_l_obp / len(self.pitchers)
        self.vs_r_lg_obp = sum_vs_r_obp / len(self.pitchers)
        self.vs_l_lg_slg = sum_vs_l_slg / len(self.pitchers)
        self.vs_r_lg_slg = sum_vs_r_slg / len(self.pitchers)

        for pitcher in self.pitchers:
            pitcher.vs_l_ops_plus = 100 * ((pitcher.vs_l_obp/self.vs_l_lg_obp) + (pitcher.vs_l_extra_base/self.vs_l_lg_slg) - 1)
            pitcher.vs_r_ops_plus = 100 * ((pitcher.vs_r_obp/self.vs_r_lg_obp) + (pitcher.vs_r_extra_base/self.vs_r_lg_slg) - 1)

    @property
    def n_left(self):
        return len([p for p in self.pitchers if p.throws == 'L'])

    @property
    def n_right(self):
        return len([p for p in self.pitchers if p.throws == 'R'])
