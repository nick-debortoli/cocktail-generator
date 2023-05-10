class RatingSystem:
    def __init__(self):
        self.dilution = {'built': [24, 24], 'shaken': [51, 60], 'stirred': [41, 49], 'shaken_egg': [46, 49], 'carbonated': [0, 0] }
        self.volume = {'built': [2.9, 3.1], 'shaken': [5.2, 5.9], 'stirred': [4.3, 4.75], 'shaken_egg': [6.6, 7], 'carbonated': [5, 6] }
        self.ethanol = {'built': [27, 32], 'shaken': [15, 20], 'stirred': [21, 29], 'shaken_egg': [12, 15], 'carbonated': [14, 16] }
        self.sugar = {'built': [7, 8], 'shaken': [5, 8.9], 'stirred': [3.7, 5.6], 'shaken_egg': [6.7, 9], 'carbonated': [5, 7.5] }
        self.acid = {'built': [0, 0], 'shaken': [0.76, 0.94], 'stirred': [0, 0.20], 'shaken_egg': [0.49, 0.68], 'carbonated': [0.38, 0.51] }
        self.sugar_acid_ratio = {'built': [7.5, 11], 'shaken': [7.5, 11], 'stirred': [7.5, 11], 'shaken_egg': [7.5, 11], 'carbonated': [7.5, 0.51] }


def get_rating_system():
    return RatingSystem()