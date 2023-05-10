class Ingredient:
    def __init__(self, props):
        self.name = props['name']
        self.ethanol = props['ethanol']
        self.sugar = props['sugar']
        self.acid = props['acid']
        self.id = props['id']

tequilaProps = {'name': 'tequila', 'ethanol': 40.0,'sugar': 0.0, 'acid': 0.0, 'id': 'tequila80'}
simpleProps = {'name': 'simple syrup', 'ethanol': 0.0,'sugar': 61.5, 'acid': 0.0, 'id': 'simpleSyrup'}
limeProps = {'name': 'lime juice', 'ethanol': 0.0,'sugar': 1.6, 'acid': 6.0, 'id': 'limeJuice'}

ingredientList = [Ingredient(tequilaProps), Ingredient(simpleProps), Ingredient(limeProps)]

def get_ingredients():
    return ingredientList