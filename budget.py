class Category:
  def __init__(self,category):
    self.ledger = []
    self.category = category

  def __str__(self):
    title_string = self.category
    while len(title_string) < 30:
      title_string = "*" + title_string + "*"
    if len(title_string) > 30:
      title_string = title_string[0:len(title_string) - 1]
    for transaction in self.ledger:
      description = transaction["description"]
      amount = str(transaction["amount"])
      check_for_decimal = str(amount).split('.')
      if len(check_for_decimal) < 2:
        amount += '.00'
      elif len(check_for_decimal[1]) < 2:
        amount += '0'
      if len(description) + len(amount) > 29:
        description = description[0:30 - (len(amount) + 1)]
      spaces = ''
      num_of_spaces = 30 - (len(amount) + len(description))
      for space in range(num_of_spaces):
        spaces += ' ' 
      title_string += f'\n{description}{spaces}{amount}'
    total = str(self.get_balance())
    if len(total.split('.')) < 2:
      total += '.00'
    elif len(total.split('.')[1]) < 2:
      total += '0'
    title_string += f'\nTotal: {total}'
    return title_string

  def deposit(self,amount,description=''):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self,amount,description=''):
    sufficient_funds = self.check_funds(amount)
    if sufficient_funds:
      self.ledger.append({"amount": amount * -1, "description": description})
      return True
    else:
      return False

  def get_balance(self):
    balance = 0
    for transaction in self.ledger:
      balance += transaction["amount"]
    return balance
    
  def transfer(self,amount,category):
    sufficient_funds = self.check_funds(amount)
    if sufficient_funds:
      self.ledger.append({"amount": amount * -1, "description": f'Transfer to {category.category}'})
      category.deposit(amount,f'Transfer from {self.category}')
      return True
    else:
      return False
      
  def check_funds(self,amount):
    amount = amount * -1
    balance = self.get_balance()
    if balance + amount >= 0:
      return True
    else: 
      return False
      
def create_spend_chart(categories):
  result = 'Percentage spent by category\n'
  x_axis = '    '
  total_spent = 0
  total_spent_per_category = []
  longest_category = 0
  for category in categories:
    if len(category.category) > longest_category:
      longest_category = len(category.category)
    amount = 0
    x_axis += '---'
    for transaction in category.ledger:
      if transaction["amount"] < 0:
        amount += transaction["amount"]
        amount = round(amount,2)
        total_spent += transaction["amount"]
        total_spent = round(total_spent,2)
    total_spent_per_category.append({"category": category.category,       "amount": amount})
  for i in range(100,-1,-10):
    line = ''
    category_line = ''
    y_axis_label = str(i)
    while len(y_axis_label) < 3:
      y_axis_label = ' ' + y_axis_label
    result += y_axis_label + '| ' 
    for category in total_spent_per_category:
      amount = category["amount"]
      amount_percentage_of_total = int((amount / total_spent) * 10) * 10
      if amount_percentage_of_total >= i:
        result += 'o  '
      else:
        result += '   '    
    result += f'\n' 
  result += f'{x_axis}-'
  for i in range(longest_category):
    line = '\n     '
    for category in categories:
      if len(category.category) > i:
        line += f'{category.category[i]}  '
      else:
        line += '   '
    result += line
  return result      