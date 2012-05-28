
class Person:
    pass
person_styles = {
    'A':'rd',
    'B':'gd',
    'C':'bd',
    'D':'cd',
    'E':'md',
    'F':'yd',
    'G':'kd',
    'H':'wd',
    
    'I':'ro',
    'J':'ro',
    'K':'ro',
    'L':'ro',
    'M':'ro',
    'N':'ro',
    'O':'ro',
    'P':'ro',
    'Q':'ro',
    'R':'ro',
    'S':'ro'
    
    
}
class Persons:
    def __init__(self,exp_list):
        self.list = []
        self.exp_list = exp_list
        for exp_index in range(len(exp_list)):
            person_id = exp_list[exp_index][0]
            if not self.list or person.id != person_id:
                person = Person()
                person.id = person_id
                person.min_index = exp_index
                self.list.append(person)
            person.max_index = exp_index
    def plot(self,plt,x,y):
        for person in self.list:
            plt.plot(
                x[person.min_index:person.max_index+1],
                y[person.min_index:person.max_index+1],
                person_styles[person.id]
            )
        for i,v in enumerate(self.exp_list): plt.annotate(v,(x[i],y[i]));
            
            