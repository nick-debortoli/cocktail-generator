import re
from ingredientList import get_ingredients
from preparationMethods import get_preparations
from ratingSystem import get_rating_system

class Cocktail(object):
    ML = 'milliliters'
    OZ = 'ounces'

    def __init__(self, name=None, creator='', ingredients=[], ethanol=0.0, sugar=0.0, acid=0.0, volume=0.0, units=None, dilution=0.0, sugar_acid_ratio=0.0):
        self._name = name
        self._creator = creator
        self._ingredients = ingredients
        self._ethanol = ethanol
        self._sugar = sugar
        self._acid = acid
        self._volume = volume
        self._units = units
        self._dilution = dilution
        self._sugar_acid_ratio = sugar_acid_ratio

    def set_creator(self, creator):
        self._creator = creator
    
    def get_creator(self):
        return self._creator

    def set_units(self, units):
        if (units == self.ML):
            self._units = self.ML
        elif (units == self.OZ):
            self._units = self.OZ

    def add_ingredient(self, ingredient, amount):
        self._volume += amount
        self._ingredients.append({'ingredient': ingredient, 'amount': amount})
    
    def calculate_specs(self):
        ethanol_sum = 0
        sugar_sum = 0
        acid_sum = 0

        for ingredient_and_amount in self._ingredients:
            ingredient = ingredient_and_amount['ingredient']
            amount = ingredient_and_amount['amount']

            ethanol_sum += ingredient.ethanol * amount
            sugar_sum += ingredient.sugar * amount
            acid_sum += ingredient.acid * amount

        self._ethanol = ethanol_sum / self._volume
        self._sugar = sugar_sum / self._volume
        self._acid = acid_sum / self._volume

    
    def add_preparation(self, dilution_function, preparation):
        pre_prep_volume = self._volume
        dilution_pct = dilution_function(self._ethanol)
        self._dilution = dilution_pct * 100
        self._volume += pre_prep_volume * dilution_pct 

        self._ethanol = self._ethanol * pre_prep_volume / self._volume
        self._sugar = self._sugar * pre_prep_volume / self._volume
        self._acid = self._acid * pre_prep_volume / self._volume

        self._sugar_acid_ratio = (self._sugar / self._acid)
        self._preparation = preparation

    
    def set_name(self, name):
        self._name = name
    
    def set_ratings(self, rating_system):
        ratings = {}
        sum_rating = 0
        rating_count = 6
        
        if (self._dilution < float(min(rating_system.dilution[self._preparation]))):
            ratings['dilution'] = 'Underdiluted'
        elif (self._dilution > float(max(rating_system.dilution[self._preparation]))):
            ratings['dilution'] = 'Overdiluted'
        else: 
            ratings['dilution'] = 'Good'
            sum_rating += 1
        
        if (self._volume < min(rating_system.volume[self._preparation])):
            ratings['volume'] = 'Not enough volume'
        elif (self._volume > max(rating_system.volume[self._preparation])):
            ratings['volume'] = 'Too much volume'
        else: 
            ratings['volume'] = 'Good'
            sum_rating += 1
        
        if (self._ethanol < min(rating_system.ethanol[self._preparation])):
            ratings['ethanol'] = 'Not enough ethanol'
        elif (self._ethanol > max(rating_system.ethanol[self._preparation])):
            ratings['ethanol'] = 'Too much ethanol'
        else: 
            ratings['ethanol'] = 'Good'
            sum_rating += 1
        
        if (self._sugar < min(rating_system.sugar[self._preparation])):
            ratings['sugar'] = 'Not enough sugar'
        elif (self._sugar > max(rating_system.sugar[self._preparation])):
            ratings['sugar'] = 'Too much sugar'
        else: 
            ratings['sugar'] = 'Good'
            sum_rating += 1
        
        if (self._acid < min(rating_system.acid[self._preparation])):
            ratings['acid'] = 'Not enough acid'
        elif (self._acid > max(rating_system.acid[self._preparation])):
            ratings['acid'] = 'Too much acid'
        else: 
            ratings['acid'] = 'Good'
            sum_rating += 1
        
        if (self._sugar_acid_ratio < min(rating_system.sugar_acid_ratio[self._preparation])):
            ratings['sugar_acid_ratio'] = 'Too much acid'
        elif (self._sugar_acid_ratio > max(rating_system.sugar_acid_ratio[self._preparation])):
            ratings['sugar_acid_ratio'] = 'Too much sugar'
        else: 
            ratings['sugar_acid_ratio'] = 'Good'
            sum_rating += 1
        
        self._ratings = ratings
        self._overall = ( sum_rating / rating_count ) * 10
        
       

    def output(self):
        if (self._name == None):
            self._name = 'cocktail'

        print('\n\nHere is your ' + self._name + '!')
        print('\nIngredients:')

        for ingredient in self._ingredients:
            print(str(ingredient['amount']) + ' ' + self._units + ' of ' + ingredient['ingredient'].name)

        print('Total Volume (with dilution):', str(round(self._volume, 2)), self._units, '-', self._ratings['volume'])
        print('\nDilution:', round(self._dilution, 2), '%', '-', self._ratings['dilution'])
        print('Ethanol (ABV%):', round(self._ethanol, 2), '%', '-', self._ratings['ethanol'])
        print('Sugar (g/100ml):', round(self._sugar, 2), '-', self._ratings['sugar'])
        print('Acid (%):', round(self._acid, 2), '%', '-', self._ratings['acid'])
        print('Sugar-Acid ratio:', round(self._sugar_acid_ratio, 2), '-', self._ratings['sugar_acid_ratio'])
        print('\nRating:', str(round(self._overall, 2)) + '/10.0')
      
class App:
    ML = 'milliliters'
    OZ = 'ounces'

    OZ_OPTIONS = ['ounces', 'ounce', 'oz', 'us oz']
    ML_OPTIONS = ['ml', 'milliliters', 'milliliter', 'millilitres', 'millilitre']

    INGREDIENT_QUERY = 'ingredients'
    NO_OPTIONS = ['n', 'no']

    ingredients = get_ingredients()
    preparations = get_preparations()
    rating_system = get_rating_system()

    def __init__(self):
        print('Welcome to the cocktail calculator!')
        self.cocktail = Cocktail()
        self.main()

    
    def dash_to_unit(self, amount):
        amount = amount.replace('dashes', '').repace('dash', '')

        if (self._units == self.OZ):
            return 0.027 * float(amount)
        elif (self._units == self.ML):
            return 0.8 * float(amount)
    
    def barspoon_to_unit(self, amount):
        amount = amount.replace('barspoon', '').repace('barspoons', '')

        if (self._units == self.OZ):
            return 0.125 * float(amount)
        elif (self._units == self.ML):
            return 4 * float(amount)
    
    def set_units(self, units):
        units = units.lower()

        if (units in self.OZ_OPTIONS):
            self._units = self.OZ
            self.cocktail.set_units(self.OZ)
        elif (units in self.ML_OPTIONS):
            self._units = self.ML
            self.cocktail.set_units(self.ML)
        else:
            new_units = input('Oops! Try again. Acceptable unit are ounces (oz) or milliliters (ml).. ')
            self.set_units(new_units)

    def ask_for_ingredients(self):
        ingredient = input('Enter your ingredient (or type "done" to finish): ')
        self.set_ingredients(ingredient)

    def set_ingredients(self, ingredient):
        if (ingredient == self.INGREDIENT_QUERY):
            print('The available ingredients are: ')
            self.ask_for_ingredients()
        elif (ingredient == 'done'):
            self.cocktail.calculate_specs()
            self.ask_for_preparation()
        else:
            ingredient_index = -1
            for index, ingredient_obj in enumerate(self.ingredients):
                if (ingredient in ingredient_obj.name):
                    ingredient_index = index
                    ingredient = ingredient_obj
                    break
            
            if (ingredient_index >= 0):
                amount = input('How much ' + ingredient.name + ' would you like to add (in ' + self._units + ', dashes, or barspoons)? ')

                if ('dash' in amount):
                    amount = self.dash_to_unit(amount)
                elif ('barspoon' in amount):
                    amount = self.barspoon_to_unit(amount)
                else: 
                    amount = float(amount.split(' ')[0])

                self.cocktail.add_ingredient(ingredient, amount)
                self.ask_for_ingredients()
            else:
                new_ingredient = input('That ingredient is not currently in our catalog. Please choose another. ')
                self.set_ingredients(new_ingredient)

    def ask_for_preparation(self):
        preparation = input('How will you prepare your cocktail? ')
        self.set_preparation(preparation)

    def set_preparation(self, preparation):
        preparation_index = -1
        for index, preparation_obj in enumerate(self.preparations):
            if (preparation in preparation_obj.name):
                preparation_index = index
                preparation = preparation_obj
                break
        
        if (preparation_index >= 0):
            dilution_function = preparation.get_dilution_function()
            self.cocktail.add_preparation(dilution_function, preparation.name)

            
        else:
            new_preparation = input('That preparation is not currently in our catalog. Please choose another. ')
            self.set_preparation(new_preparation)

        self.set_name()
    
    def set_name(self):
        name = input('What would you like to name your cocktail? (Type "none" to skip naming) ')

        if (name != 'none'):
            self.cocktail.set_name(name)
        
        self.finish_cocktail()

    def finish_cocktail(self):
        self.cocktail.set_ratings(self.rating_system)
        self.cocktail.output()
        
    def main(self):
        cocktail = self.cocktail
        name = input('Please tell us your name. ').strip()
        cocktail.set_creator(name)

        # Get units for the cocktail
        units = input('Hi, ' + cocktail.get_creator() + '! To start, please enter your desired units: ')
        self.set_units(units)

        # Get ingredients and ammounts for cocktial
        print('\nPlease list the ingredients of your cocktail in ' + self._units + '. If your amount is in dashes or barspoons, please type out "dashes" or "barspoons."  For list of possible ingredients, type "ingredients".')
        self.ask_for_ingredients()


if __name__ == "__main__":
   app = App()
