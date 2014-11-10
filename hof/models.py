import xlrd

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
        self.left_weight = 0.5
        self.right_weight = 0.5

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
        return int(self.left_weight*self.vs_l_ops_plus + self.right_weight*self.vs_r_ops_plus)

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
    def __init__(self, sheet, seasons=None):
        key_row = sheet.row(0)
        key_list = [sheet.cell_value(0, col_index) for col_index in xrange(sheet.ncols)]

        self.batters = []
        for row in xrange(1, sheet.nrows):
            value_list = [sheet.cell_value(row, col_index) for col_index in xrange(sheet.ncols)]
            batter = BatterModel.from_list(key_list, value_list)
            self.batters.append(batter)

        if seasons is not None and len(seasons):
            self.batters = [b for b in self.batters if b.eligible_season in seasons]

    def initialize(self, n_left, n_right):
        self.n_pitchers_left = float(n_left)
        self.n_pitchers_right = float(n_right)
        self.n_pitchers = self.n_pitchers_left + self.n_pitchers_right

        sum_vs_l_obp = sum_vs_r_obp = 0.0
        sum_vs_l_slg = sum_vs_r_slg = 0.0
        for batter in self.batters:
            batter.left_weight = self.n_pitchers_left/self.n_pitchers
            batter.right_weight = self.n_pitchers_right/self.n_pitchers

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
            'POWER' : 'power',
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
    def __init__(self, sheet, seasons=None):
        key_row = sheet.row(0)
        key_list = [sheet.cell_value(0, col_index) for col_index in xrange(sheet.ncols)]

        self.pitchers = []
        for row in xrange(1, sheet.nrows):
            value_list = [sheet.cell_value(row, col_index) for col_index in xrange(sheet.ncols)]
            pitcher = PitcherModel.from_list(key_list, value_list)
            self.pitchers.append(pitcher)

        if seasons is not None and len(seasons):
            self.pitchers = [p for p in self.pitchers if p.eligible_season in seasons]

    def _generate_average_pitcher(self, throws):
        average_pitcher = PitcherModel()
        average_pitcher.__dict__['id'] = throws
        average_pitcher.__dict__['name'] = 'Average {}'.format(throws)
        average_pitcher.__dict__['throws'] = throws

        all_pitchers = [p for p in self.pitchers if p.throws == throws]
        rep_pitcher = all_pitchers[0]
        for key in vars(rep_pitcher):
            if key.startswith("vs_"):
                for pitcher in all_pitchers:
                    if key in average_pitcher.__dict__:
                        average_pitcher.__dict__[key] += pitcher.__dict__[key]
                    else:
                        average_pitcher.__dict__[key] = pitcher.__dict__[key]
                average_pitcher.__dict__[key] /= len(all_pitchers)
        return average_pitcher

    def initialize(self, n_left, n_right):
        self.n_batters_left = float(n_left)
        self.n_batters_right = float(n_right)
        self.n_batters = self.n_batters_left + self.n_batters_right

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

        self.average_lefty = self._generate_average_pitcher('L')
        self.average_righty = self._generate_average_pitcher('R')

    @property
    def n_left(self):
        return len([p for p in self.pitchers if p.throws == 'L'])

    @property
    def n_right(self):
        return len([p for p in self.pitchers if p.throws == 'R'])

class HOF(object):
    def __init__(self, workbook_name=None, seasons=None):
        workbook = xlrd.open_workbook('2014_HOF.xlsx')
        batter_sheet = workbook.sheet_by_name('Batters - Strat Card Data')
        pitcher_sheet = workbook.sheet_by_name('Pitchers - Strat Card Data')

        self.hof_pitchers = HOFPitchers(pitcher_sheet, seasons)
        self.hof_batters = HOFBatters(batter_sheet, seasons)
        self.hof_batters.initialize(self.hof_pitchers.n_left, self.hof_pitchers.n_right)
        self.hof_pitchers.initialize(self.hof_batters.n_left, self.hof_batters.n_right)

    @property
    def pitchers(self):
        return self.hof_pitchers.pitchers

    @property
    def batters(self):
        return self.hof_batters.batters

    @property
    def average_lefty_pitcher(self):
        return self.hof_pitchers.average_lefty

    @property
    def average_righty_pitcher(self):
        return self.hof_pitchers.average_righty
