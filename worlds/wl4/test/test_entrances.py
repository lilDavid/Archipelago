from . import WL4TestBase


REQUIRED_JEWELS = 3


class TestEntrances(WL4TestBase):
    options = {'required_jewels': REQUIRED_JEWELS}

    def test_entry_levels(self):
        self.starting_regions = ['Hall of Hieroglyphs (entrance)']
        self.run_entrance_tests([
            ['Hall of Hieroglyphs Gate', False, []],
            ['Hall of Hieroglyphs Gate', False, [], ['Dash Attack']],
            ['Hall of Hieroglyphs Gate', False, [], ['Progressive Grab']],
            ['Hall of Hieroglyphs Gate', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Hall of Hieroglyphs Gate', True,
             ['Dash Attack', 'Progressive Grab', 'Progressive Ground Pound', 'Progressive Ground Pound']],
        ])

    def test_emerald_levels(self):
        self.starting_regions = ['Palm Tree Paradise (entrance)', 'Wildflower Fields (entrance)',
                                 'Mystic Lake (entrance)', 'Monsoon Jungle (entrance)']
        self.run_entrance_tests([
            ['Palm Tree Paradise Gate', True, []],

            ['Wildflower Fields Gate', False, []],
            ['Wildflower Fields Gate', False, [], ['Swim']],
            ['Wildflower Fields Gate', False,
             ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['Wildflower Fields Gate', True,
             ['Swim', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Mystic Lake Gate', False, []],
            ['Mystic Lake Gate', False, [], ['Swim']],
            ['Mystic Lake Gate', False, [], ['Head Smash']],
            ['Mystic Lake Gate', True, ['Swim', 'Head Smash']],

            ['Monsoon Jungle Gate', False, []],
            ['Monsoon Jungle Gate', False, [], ['Progressive Ground Pound']],
            ['Monsoon Jungle Gate', True, ['Progressive Ground Pound']],
        ])

    def test_ruby_levels(self):
        self.starting_regions = ['The Curious Factory (entrance)', 'The Toxic Landfill (entrance)',
                                 '40 Below Fridge (entrance)', 'Pinball Zone (entrance)']
        self.run_entrance_tests([
            ['The Curious Factory Gate', True, []],

            ['The Toxic Landfill Gate', False, []],
            ['The Toxic Landfill Gate', False, [], ['Dash Attack']],
            ['The Toxic Landfill Gate', False, [], ['Head Smash']],
            ['The Toxic Landfill Gate', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['The Toxic Landfill Gate', True,
             ['Dash Attack', 'Head Smash', 'Progressive Ground Pound', 'Progressive Ground Pound']],

            ['40 Below Fridge Gate', False, []],
            ['40 Below Fridge Gate', False, ['Progressive Ground Pound'], ['Progressive Ground Pound']],
            ['40 Below Fridge Gate', True, ['Progressive Ground Pound', 'Progressive Ground Pound']],

            ['Pinball Zone', False, []],
            ['Pinball Zone', False, [], ['Progressive Grab']],
            ['Pinball Zone', False, [], ['Progressive Ground Pound']],
            ['Pinball Zone', False, [], ['Head Smash']],
            ['Pinball Zone', True,
             ['Progressive Grab', 'Progressive Ground Pound', 'Head Smash']],
        ])

    def test_topaz_levels(self):
        self.starting_regions = ['Toy Block Tower (entrance)', 'The Big Board (entrance)',
                                 'Doodle Woods (entrance)', 'Domino Row (entrance)']
        self.run_entrance_tests([
            ['Toy Block Tower Gate', False, []],
            ['Toy Block Tower Gate', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Toy Block Tower Gate', True, ['Progressive Grab', 'Progressive Grab']],

            ['The Big Board Gate', False, []],
            ['The Big Board Gate', False, [], ['Progressive Ground Pound']],
            ['The Big Board Gate', True, ['Progressive Ground Pound']],

            ['Doodle Woods', True, []],

            ['Domino Row', False, []],
            ['Domino Row', False, [], ['Swim']],
            ['Domino Row', True, ['Swim']],
        ])

    def test_sapphire_levels(self):
        self.starting_regions = ['Crescent Moon Village (entrance)', 'Arabian Night (entrance)',
                                 'Fiery Cavern (entrance)', 'Hotel Horror (entrance)']
        self.run_entrance_tests([
            ['Crescent Moon Village Gate', False, []],
            ['Crescent Moon Village Gate', False, [], ['Dash Attack']],
            ['Crescent Moon Village Gate', False, [], ['Head Smash']],
            ['Crescent Moon Village Gate', True, ['Dash Attack', 'Head Smash']],

            ['Arabian Night Gate', False, []],
            ['Arabian Night Gate', False, [], ['Swim']],
            ['Arabian Night Gate', True, ['Swim']],

            ['Fiery Cavern Gate', False, []],
            ['Fiery Cavern Gate', False, [], ['Dash Attack']],
            ['Fiery Cavern Gate', False, [], ['Progressive Ground Pound']],
            ['Fiery Cavern Gate', True, ['Dash Attack', 'Progressive Ground Pound']],

            ['Hotel Horror', False, []],
            ['Hotel Horror', False, ['Progressive Grab'], ['Progressive Grab']],
            ['Hotel Horror', True, ['Progressive Grab', 'Progressive Grab']],
        ])

    def test_golden_pyramid(self):
        self.starting_regions = ['Golden Passage (entrance)']
        self.run_entrance_tests([
            ['Golden Passage Gate', False, []],
            ['Golden Passage Gate', False, [], ['Swim']],
            ['Golden Passage Gate', False, [], ['Progressive Ground Pound']],
            ['Golden Passage Gate', False, [], ['Progressive Grab']],
            ['Golden Passage Gate', True, ['Swim', 'Progressive Ground Pound', 'Progressive Grab']],
        ])

    def test_bosses(self):
        self.starting_regions = ['Entry Minigame Shop', 'Emerald Minigame Shop',
                                 'Ruby Minigame Shop', 'Topaz Minigame Shop',
                                 'Sapphire Minigame Shop', 'Golden Minigame Shop']
        self.run_entrance_tests([
            ['Entry Minigame Shop -> Entry Passage Boss', False, []],
            ['Entry Minigame Shop -> Entry Passage Boss', False,
             [], ['Top Right Entry Jewel Piece']],
            ['Entry Minigame Shop -> Entry Passage Boss', False,
             [], ['Top Left Entry Jewel Piece']],
            ['Entry Minigame Shop -> Entry Passage Boss', False,
             [], ['Bottom Right Entry Jewel Piece']],
            ['Entry Minigame Shop -> Entry Passage Boss', False,
             [], ['Bottom Left Entry Jewel Piece']],
            ['Entry Minigame Shop -> Entry Passage Boss', True,
             ['Top Right Entry Jewel Piece', 'Top Left Entry Jewel Piece',
              'Bottom Right Entry Jewel Piece', 'Bottom Left Entry Jewel Piece']],

            ['Emerald Minigame Shop -> Emerald Passage Boss', False, []],
            ['Emerald Minigame Shop -> Emerald Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Top Right Emerald Piece'], ['Top Right Emerald Piece']],
            ['Emerald Minigame Shop -> Emerald Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Top Left Emerald Piece'], ['Top Left Emerald Piece']],
            ['Emerald Minigame Shop -> Emerald Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Right Emerald Piece'], ['Bottom Right Emerald Piece']],
            ['Emerald Minigame Shop -> Emerald Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Left Emerald Piece'], ['Bottom Left Emerald Piece']],
            ['Emerald Minigame Shop -> Emerald Passage Boss', True,
             REQUIRED_JEWELS * ['Top Right Emerald Piece', 'Top Left Emerald Piece',
                  'Bottom Right Emerald Piece', 'Bottom Left Emerald Piece']],

            ['Ruby Minigame Shop -> Ruby Passage Boss', False, []],
            ['Ruby Minigame Shop -> Ruby Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Top Right Ruby Piece'], ['Top Right Ruby Piece']],
            ['Ruby Minigame Shop -> Ruby Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Top Left Ruby Piece'], ['Top Left Ruby Piece']],
            ['Ruby Minigame Shop -> Ruby Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Right Ruby Piece'], ['Bottom Right Ruby Piece']],
            ['Ruby Minigame Shop -> Ruby Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Left Ruby Piece'], ['Bottom Left Ruby Piece']],
            ['Ruby Minigame Shop -> Ruby Passage Boss', True,
             REQUIRED_JEWELS * ['Top Right Ruby Piece', 'Top Left Ruby Piece',
                  'Bottom Right Ruby Piece', 'Bottom Left Ruby Piece']],

            ['Topaz Minigame Shop -> Topaz Passage Boss', False, []],
            ['Topaz Minigame Shop -> Topaz Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Top Right Topaz Piece'], ['Top Right Topaz Piece']],
            ['Topaz Minigame Shop -> Topaz Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Top Left Topaz Piece'], ['Top Left Topaz Piece']],
            ['Topaz Minigame Shop -> Topaz Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Right Topaz Piece'], ['Bottom Right Topaz Piece']],
            ['Topaz Minigame Shop -> Topaz Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Left Topaz Piece'], ['Bottom Left Topaz Piece']],
            ['Topaz Minigame Shop -> Topaz Passage Boss', True,
             REQUIRED_JEWELS * ['Top Right Topaz Piece', 'Top Left Topaz Piece',
                  'Bottom Right Topaz Piece', 'Bottom Left Topaz Piece']],

            ['Sapphire Minigame Shop -> Sapphire Passage Boss', False, []],
            ['Sapphire Minigame Shop -> Sapphire Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Top Right Sapphire Piece'], ['Top Right Sapphire Piece']],
            ['Sapphire Minigame Shop -> Sapphire Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Top Left Sapphire Piece'], ['Top Left Sapphire Piece']],
            ['Sapphire Minigame Shop -> Sapphire Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Right Sapphire Piece'], ['Bottom Right Sapphire Piece']],
            ['Sapphire Minigame Shop -> Sapphire Passage Boss', False,
             (REQUIRED_JEWELS - 1) * ['Bottom Left Sapphire Piece'], ['Bottom Left Sapphire Piece']],
            ['Sapphire Minigame Shop -> Sapphire Passage Boss', True,
             REQUIRED_JEWELS * ['Top Right Sapphire Piece', 'Top Left Sapphire Piece',
                  'Bottom Right Sapphire Piece', 'Bottom Left Sapphire Piece']],

            ['Golden Minigame Shop -> Golden Pyramid Boss', False, []],
            ['Golden Minigame Shop -> Golden Pyramid Boss', False,
             [], ['Top Right Golden Jewel Piece']],
            ['Golden Minigame Shop -> Golden Pyramid Boss', False,
             [], ['Top Left Golden Jewel Piece']],
            ['Golden Minigame Shop -> Golden Pyramid Boss', False,
             [], ['Bottom Right Golden Jewel Piece']],
            ['Golden Minigame Shop -> Golden Pyramid Boss', False,
             [], ['Bottom Left Golden Jewel Piece']],
            ['Golden Minigame Shop -> Golden Pyramid Boss', True,
             ['Top Right Golden Jewel Piece', 'Top Left Golden Jewel Piece',
              'Bottom Right Golden Jewel Piece', 'Bottom Left Golden Jewel Piece']],
        ])