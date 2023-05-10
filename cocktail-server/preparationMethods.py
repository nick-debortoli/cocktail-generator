class Preparation:
     def __init__(self, props):
        self.name = props['name']
        self.first_term = props['first_term']
        self.second_term = props['second_term']
        self.third_term = props['third_term']
    
     def get_dilution_function(self):
         
         def dilution_function(ethanol):
              ethanol_pct = ethanol / 100
              dilution_pct = (self.first_term*ethanol_pct**2 + self.second_term*ethanol_pct + self.third_term) #/ 100
              return dilution_pct
         
         return dilution_function
             
shakenProps = {'name': 'shaken', 'first_term':-1.567, 'second_term': 1.742, 'third_term': 0.203}
preparationList = [Preparation(shakenProps)]

def get_preparations():
    return preparationList