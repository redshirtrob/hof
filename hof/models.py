import xlrd

class DataSource(object):
    def __init__(self, workbook, batter_sheet, pitcher_sheet, seasons):
        self.workbook = workbook
        self.batter_sheet = batter_sheet
        self.pitcher_sheet = pitcher_sheet
        self.seasons = seasons

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
            if key in kls.Meta.excel_map:
                kls.__dict__[kls.Meta.excel_map[key]] = value
        return kls

class HOFModel(BaseModel):
    @property
    def eligible_season(self):
        if type(self.id) is float:
            return str(int(self.id)).split('-')[0]
        else:
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
        self.is_reference = False

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
            'vsR Ballpark Diamonds' : 'vs_r_ballpark_diamonds',
        }

    def __repr__(self):
        if self.is_reference:
            return '{}: {}: {}: {}: {} {:6.2f}'.format(self.eligible_season, self.bats, self.name, self.pos_to_use, self.ops_plus, self.ballpark_diamonds_adj)
        else:
            return '{}: {}: {}: {}: {} {:6.2f}'.format(self.eligible_season, self.bats, self.name, self.pos_to_use, self.ops_plus_adj, self.ballpark_diamonds_adj)

    @property
    def vs_l_slg(self):
        return self.vs_l_single + 2*self.vs_l_double + 3*self.vs_l_triple + 4*self.vs_l_home_run

    @property
    def vs_r_slg(self):
        return self.vs_r_single + 2*self.vs_r_double + 3*self.vs_r_triple + 4*self.vs_r_home_run

    @property
    def ops_plus(self):
        return int(self.left_weight*self.vs_l_ops_plus + self.right_weight*self.vs_r_ops_plus)

    @property
    def ops_plus_adj(self):
        return int(self.left_weight*self.vs_l_ops_plus_adj + self.right_weight*self.vs_r_ops_plus_adj)

    @property
    def vs_l_weak(self):
        l, r = self.power_lr.split('/')
        return l == 'W'

    @property
    def vs_r_weak(self):
        l, r = self.power_lr.split('/')
        return r == 'W'

    @property
    def ballpark_diamonds_adj(self):
        return self.left_weight*self.vs_l_ballpark_diamonds + self.right_weight*self.vs_r_ballpark_diamonds

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

    def vs_l_obp_adj(self, lefty):
        # Batter roll
        batter_vs_l_obp = self.vs_l_obp

        # Pitcher roll
        if self.bats == 'L': # Lefty vs. Lefty
            pitcher_vs_l_obp = lefty.vs_l_obp
        elif self.bats == 'R' or self.bats == 'S': # Righty vs. Lefty
            pitcher_vs_l_obp = lefty.vs_r_obp

        return (batter_vs_l_obp + pitcher_vs_l_obp) / 2.0

    def vs_r_obp_adj(self, righty):
        # Batter roll
        batter_vs_r_obp = self.vs_r_obp

        # Pitcher roll
        if self.bats == 'L' or self.bats == 'S': # Lefty vs. Righty
            pitcher_vs_r_obp = righty.vs_l_obp
        elif self.bats == 'R': # Righty vs. Righty
            pitcher_vs_r_obp = righty.vs_r_obp

        return (batter_vs_r_obp + pitcher_vs_r_obp) / 2.0

    def vs_l_slg_adj(self, lefty):
        # Batter roll
        batter_vs_l_slg = self.vs_l_slg

        # Pitcher roll
        if self.bats == 'L': # Lefty vs. Lefty
            pitcher_vs_l_slg = lefty.vs_l_slg
            if self.vs_l_weak:
                pitcher_vs_l_slg -= 3*lefty.vs_l_home_run
        elif self.bats == 'R' or self.bats == 'S': # Righty vs. Lefty
            pitcher_vs_l_slg = lefty.vs_r_slg
            if self.vs_l_weak:
                pitcher_vs_l_slg -= 3*lefty.vs_r_home_run

        return (batter_vs_l_slg + pitcher_vs_l_slg) / 2.0

    def vs_r_slg_adj(self, righty):
        # Batter roll
        batter_vs_r_slg = self.vs_r_slg

        # Pitcher roll
        if self.bats == 'L' or self.bats == 'S': # Lefty vs. Righty
            pitcher_vs_r_slg = righty.vs_l_slg
            if self.vs_r_weak:
                pitcher_vs_r_slg -= 3*righty.vs_l_home_run
        elif self.bats == 'R': # Righty vs. Righty
            pitcher_vs_r_slg = righty.vs_r_slg
            if self.vs_r_weak:
                pitcher_vs_r_slg -= 3*righty.vs_r_home_run

        return (batter_vs_r_slg + pitcher_vs_r_slg) / 2.0

class HOFBatters(object):
    def __init__(self, data_sources, players=None):
        self.batters = []
        for ds in data_sources:
            workbook = xlrd.open_workbook(ds.workbook)
            sheet = workbook.sheet_by_name(ds.batter_sheet)
            
            key_row = sheet.row(0)
            key_list = [sheet.cell_value(0, col_index) for col_index in xrange(sheet.ncols)]

            tmp_batters = []
            for row in xrange(1, sheet.nrows):
                value_list = [sheet.cell_value(row, col_index) for col_index in xrange(sheet.ncols)]
                batter = BatterModel.from_list(key_list, value_list)
                tmp_batters.append(batter)

            if ds.seasons is not None and len(ds.seasons):
                self.batters += [b for b in tmp_batters if (b.eligible_season in ds.seasons) and (players is None or b.id not in players)]

        self._generate_ops_plus()
        self.average_lefty = self._generate_average_batter('L')
        self.average_righty = self._generate_average_batter('R')

    def _generate_ops_plus(self):
        sum_vs_l_obp = sum_vs_r_obp = 0.0
        sum_vs_l_slg = sum_vs_r_slg = 0.0
        for batter in self.batters:
            sum_vs_l_obp += batter.vs_l_obp
            sum_vs_r_obp += batter.vs_r_obp
            sum_vs_l_slg += batter.vs_l_slg
            sum_vs_r_slg += batter.vs_r_slg
        self.vs_l_lg_obp = sum_vs_l_obp / len(self.batters)
        self.vs_r_lg_obp = sum_vs_r_obp / len(self.batters)
        self.vs_l_lg_slg = sum_vs_l_slg / len(self.batters)
        self.vs_r_lg_slg = sum_vs_r_slg / len(self.batters)

        for batter in self.batters:
            batter.vs_l_ops_plus = 100 * ((batter.vs_l_obp/self.vs_l_lg_obp) + (batter.vs_l_slg/self.vs_l_lg_slg) - 1)
            batter.vs_r_ops_plus = 100 * ((batter.vs_r_obp/self.vs_r_lg_obp) + (batter.vs_r_slg/self.vs_r_lg_slg) - 1)

    def _generate_ops_plus_adj(self, average_lefty, average_righty):
        self.average_pitcher_left = average_lefty
        self.average_pitcher_right = average_righty

        sum_vs_l_obp = sum_vs_r_obp = 0.0
        sum_vs_l_slg = sum_vs_r_slg = 0.0
        for batter in self.batters:
            batter.left_weight = self.n_pitchers_left/self.n_pitchers
            batter.right_weight = self.n_pitchers_right/self.n_pitchers

            if self.average_pitcher_left is not None:
                sum_vs_l_obp += batter.vs_l_obp_adj(self.average_pitcher_left)
                sum_vs_l_slg += batter.vs_l_slg_adj(self.average_pitcher_left)
            if self.average_pitcher_right is not None:
                sum_vs_r_obp += batter.vs_r_obp_adj(self.average_pitcher_right)
                sum_vs_r_slg += batter.vs_r_slg_adj(self.average_pitcher_right)

        self.vs_l_lg_obp = sum_vs_l_obp / len(self.batters)
        self.vs_r_lg_obp = sum_vs_r_obp / len(self.batters)
        self.vs_l_lg_slg = sum_vs_l_slg / len(self.batters)
        self.vs_r_lg_slg = sum_vs_r_slg / len(self.batters)

        for batter in self.batters:
            if self.average_pitcher_left is not None:
                vs_l_obp = batter.vs_l_obp_adj(self.average_pitcher_left)
                vs_l_slg = batter.vs_l_slg_adj(self.average_pitcher_left)
                batter.vs_l_ops_plus_adj = 100 * ((vs_l_obp/self.vs_l_lg_obp) + (vs_l_slg/self.vs_l_lg_slg) - 1)
            else:
                batter.vs_l_ops_plus_adj = 0

            if self.average_pitcher_right is not None:
                vs_r_obp = batter.vs_r_obp_adj(self.average_pitcher_right)
                vs_r_slg = batter.vs_r_slg_adj(self.average_pitcher_right)
                batter.vs_r_ops_plus_adj = 100 * ((vs_r_obp/self.vs_r_lg_obp) + (vs_r_slg/self.vs_r_lg_slg) - 1)
            else:
                batter.vs_r_ops_plus_adj = 0

    def _generate_average_batter(self, bats):
        average_batter = BatterModel()
        average_batter.is_reference = True
        average_batter.__dict__['id'] = bats
        average_batter.__dict__['name'] = 'Average {}'.format(bats)
        average_batter.__dict__['bats'] = bats
        average_batter.__dict__['pos_to_use'] = 'N/A'

        all_batters = [b for b in self.batters if b.bats == bats]
        rep_batter = all_batters[0]
        for key in vars(rep_batter):
            if key.startswith("vs_"):
                for batter in all_batters:
                    if key in average_batter.__dict__:
                        average_batter.__dict__[key] += batter.__dict__[key]
                    else:
                        average_batter.__dict__[key] = batter.__dict__[key]
                average_batter.__dict__[key] /= len(all_batters)
        return average_batter

    def initialize(self, n_left, n_right, average_lefty, average_righty):
        self.n_pitchers_left = float(n_left)
        self.n_pitchers_right = float(n_right)
        self.n_pitchers = self.n_pitchers_left + self.n_pitchers_right
        self._generate_ops_plus_adj(average_lefty, average_righty)

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
        self.left_weight = 0.5
        self.right_weight = 0.5
        self.is_reference = False

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
        if self.is_reference:
            return '{}: {}: {}: {}'.format(self.eligible_season, self.throws, self.name, self.ops_plus)
        else:
            return '{}: {}: {}: {}'.format(self.eligible_season, self.throws, self.name, self.ops_plus_adj)

    @property
    def vs_l_slg(self):
        return self.vs_l_single + 2*self.vs_l_double + 3*self.vs_l_triple + 4*self.vs_l_home_run

    @property
    def vs_r_slg(self):
        return self.vs_r_single + 2*self.vs_r_double + 3*self.vs_r_triple + 4*self.vs_r_home_run

    @property
    def ops_plus(self):
        return int(self.left_weight*self.vs_l_ops_plus + self.right_weight*self.vs_r_ops_plus)

    @property
    def ops_plus_adj(self):
        return int(self.left_weight*self.vs_l_ops_plus_adj + self.right_weight*self.vs_r_ops_plus_adj)

    def field_rating(self):
        return PitcherModel.field_rating(self.field_rating)

    def error_rating(self):
        return PitcherModel.error_rating(self.field_rating)

    def vs_l_obp_adj(self, lefty):
        # Pitcher roll
        pitcher_vs_l_obp = self.vs_l_obp

        # Batter roll
        if self.throws == 'L':
            batter_vs_l_obp = lefty.vs_l_obp
        else:
            batter_vs_l_obp = lefty.vs_r_obp

        return (pitcher_vs_l_obp + batter_vs_l_obp) / 2.0

    def vs_r_obp_adj(self, righty):
        # Pitcher roll
        pitcher_vs_r_obp = self.vs_r_obp

        # Batter roll
        if self.throws == 'L':
            batter_vs_r_obp = righty.vs_l_obp
        else:
            batter_vs_r_obp = righty.vs_r_obp

        return (pitcher_vs_r_obp + batter_vs_r_obp) / 2.0

    def vs_l_slg_adj(self, lefty):
        # Pitcher roll
        pitcher_vs_l_slg = self.vs_l_slg

        # Batter roll
        if self.throws == 'L':
            batter_vs_l_slg = lefty.vs_l_slg
        else:
            batter_vs_l_slg = lefty.vs_r_slg

        return (pitcher_vs_l_slg + batter_vs_l_slg) / 2.0

    def vs_r_slg_adj(self, righty):
        # Pitcher roll
        pitcher_vs_r_slg = self.vs_r_slg

        # Batter roll
        if self.throws == 'L':
            batter_vs_r_slg = righty.vs_r_slg
        else:
            batter_vs_r_slg = righty.vs_l_slg

        return (pitcher_vs_r_slg + batter_vs_r_slg) / 2.0

class HOFPitchers(object):
    def __init__(self, data_sources, players=None):
        self.pitchers = []
        for ds in data_sources:
            workbook = xlrd.open_workbook(ds.workbook)
            sheet = workbook.sheet_by_name(ds.pitcher_sheet)
            
            key_row = sheet.row(0)
            key_list = [sheet.cell_value(0, col_index) for col_index in xrange(sheet.ncols)]

            tmp_pitchers = []
            for row in xrange(1, sheet.nrows):
                value_list = [sheet.cell_value(row, col_index) for col_index in xrange(sheet.ncols)]
                pitcher = PitcherModel.from_list(key_list, value_list)
                tmp_pitchers.append(pitcher)

            if ds.seasons is not None and len(ds.seasons):
                self.pitchers += [p for p in tmp_pitchers if (p.eligible_season in ds.seasons) and (players is None or p.id not in players)]

        self._generate_ops_plus()
        self.average_lefty = self._generate_average_pitcher('L')
        self.average_righty = self._generate_average_pitcher('R')
        
    def _generate_ops_plus(self):
        sum_vs_l_obp = sum_vs_r_obp = 0.0
        sum_vs_l_slg = sum_vs_r_slg = 0.0
        for pitcher in self.pitchers:
            sum_vs_l_obp += pitcher.vs_l_obp
            sum_vs_r_obp += pitcher.vs_r_obp
            sum_vs_l_slg += pitcher.vs_l_slg
            sum_vs_r_slg += pitcher.vs_r_slg
        self.vs_l_lg_obp = sum_vs_l_obp / len(self.pitchers)
        self.vs_r_lg_obp = sum_vs_r_obp / len(self.pitchers)
        self.vs_l_lg_slg = sum_vs_l_slg / len(self.pitchers)
        self.vs_r_lg_slg = sum_vs_r_slg / len(self.pitchers)

        for pitcher in self.pitchers:
            pitcher.vs_l_ops_plus = 100 * ((pitcher.vs_l_obp/self.vs_l_lg_obp) + (pitcher.vs_l_slg/self.vs_l_lg_slg) - 1)
            pitcher.vs_r_ops_plus = 100 * ((pitcher.vs_r_obp/self.vs_r_lg_obp) + (pitcher.vs_r_slg/self.vs_r_lg_slg) - 1)

    def _generate_ops_plus_adj(self, average_lefty, average_righty):
        self.average_batter_left = average_lefty
        self.average_batter_right = average_righty

        sum_vs_l_obp = sum_vs_r_obp = 0.0
        sum_vs_l_slg = sum_vs_r_slg = 0.0
        for pitcher in self.pitchers:
            pitcher.left_weight = self.n_batters_left/self.n_batters
            pitcher.right_weight = self.n_batters_right/self.n_batters

            sum_vs_l_obp += pitcher.vs_l_obp_adj(self.average_batter_left)
            sum_vs_r_obp += pitcher.vs_r_obp_adj(self.average_batter_right)
            sum_vs_l_slg += pitcher.vs_l_slg_adj(self.average_batter_left)
            sum_vs_r_slg += pitcher.vs_r_slg_adj(self.average_batter_right)

        self.vs_l_lg_obp = sum_vs_l_obp / len(self.pitchers)
        self.vs_r_lg_obp = sum_vs_r_obp / len(self.pitchers)
        self.vs_l_lg_slg = sum_vs_l_slg / len(self.pitchers)
        self.vs_r_lg_slg = sum_vs_r_slg / len(self.pitchers)

        for pitcher in self.pitchers:
            vs_l_obp = pitcher.vs_l_obp_adj(self.average_batter_left)
            vs_l_slg = pitcher.vs_l_slg_adj(self.average_batter_left)
            pitcher.vs_l_ops_plus_adj = 100 * ((vs_l_obp/self.vs_l_lg_obp) + (vs_l_slg/self.vs_l_lg_slg) - 1)

            vs_r_obp = pitcher.vs_r_obp_adj(self.average_batter_right)
            vs_r_slg = pitcher.vs_r_slg_adj(self.average_batter_right)
            pitcher.vs_r_ops_plus_adj = 100 * ((vs_r_obp/self.vs_r_lg_obp) + (vs_r_slg/self.vs_r_lg_slg) - 1)

    def _generate_average_pitcher(self, throws):
        average_pitcher = PitcherModel()
        average_pitcher.is_reference = True
        average_pitcher.__dict__['id'] = throws
        average_pitcher.__dict__['name'] = 'Average {}'.format(throws)
        average_pitcher.__dict__['throws'] = throws

        all_pitchers = [p for p in self.pitchers if p.throws == throws]
        if len(all_pitchers) == 0:
            return None
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

    def initialize(self, n_left, n_right, average_lefty, average_righty):
        self.n_batters_left = float(n_left)
        self.n_batters_right = float(n_right)
        self.n_batters = self.n_batters_left + self.n_batters_right
        self._generate_ops_plus_adj(average_lefty, average_righty)

    @property
    def n_left(self):
        return len([p for p in self.pitchers if p.throws == 'L'])

    @property
    def n_right(self):
        return len([p for p in self.pitchers if p.throws == 'R'])

class HOF(object):
    def __init__(self, data_sources=None, batters=None, pitchers=None):
        self.hof_pitchers = HOFPitchers(data_sources, pitchers)
        self.hof_batters = HOFBatters(data_sources, batters)

        self.hof_pitchers.initialize(self.hof_batters.n_left, self.hof_batters.n_right, self.hof_batters.average_lefty, self.hof_batters.average_righty)
        self.hof_batters.initialize(self.hof_pitchers.n_left, self.hof_pitchers.n_right, self.hof_pitchers.average_lefty, self.hof_pitchers.average_righty)

    @property
    def batters(self):
        return self.hof_batters.batters

    @property
    def average_lefty_batter(self):
        return self.hof_batters.average_lefty

    @property
    def average_righty_batter(self):
        return self.hof_batters.average_righty

    @property
    def pitchers(self):
        return self.hof_pitchers.pitchers

    @property
    def average_lefty_pitcher(self):
        return self.hof_pitchers.average_lefty

    @property
    def average_righty_pitcher(self):
        return self.hof_pitchers.average_righty
