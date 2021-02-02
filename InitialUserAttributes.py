class User:

    def __init__(self):
        self.name = ''
        self.weight = -1
        self.height = -1
        self.gender = ''
        self.age = ''
        self.sleep_time = -1
        self.wake_time = -1
        self.collect_information()

    def __repr__(self):
        return f'Name: {self.name}, Gender: {self.gender}, Age: {self.age}, Weight: {self.weight}, Height: {self.height}'

    def input_numerical_stat(self, stat, unit, lower, upper):
        while True:
            try:
                statistic = float(input(f'Enter {stat} ({unit}) : '))
                if statistic > upper or statistic < lower:
                    print(f'Invalid input, please re-enter {stat}. Value must be from 0-{upper}.')
                    continue
                break
            except ValueError:
                print(f'Invalid input, please re-enter {stat}. Value must be from 0-{upper}.')
                continue
        return statistic
    
    
    def personal_info(self):
        while True:
            name = input('Enter name: ').strip()
            if name == '':
                print('Invalid input, name cannot consist only of spaces.')
                continue
            break

        genders = {'m','f','male','female'}
        while True:
            gender = input('Enter gender (M/F): ').strip().lower()
            if gender not in genders:
                print('Invalid input, re-enter your gender.')
                continue
            break

        return (name,gender)
        

    def collect_information(self):
        numerical_statistics = [('age', 'years', 0, 150), ('height','cm', 0,400), ('weight','kg', 0,1000)]
        personal = self.personal_info()
        self.name = personal[0]
        self.gender = personal[1]

        for stat in numerical_statistics:
            if stat[0] == 'age':
                self.age = int(self.input_numerical_stat(stat[0],stat[1],stat[2],stat[3]))
            else:
                setattr(self,stat[0],self.input_numerical_stat(stat[0],stat[1],stat[2],stat[3]))


    def enter_sleep(self):
        self.sleep_time = input("Enter sleep timing: ")
        self.wake_time = input("Enter waking time: ")


##x = User()
##print(x)
