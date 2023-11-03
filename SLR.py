# Importing the tabulate library
from tabulate import tabulate

# CLOSURE Function
def CLOSURE(closureI, G, added):
  newAdded = {}
  for key in added:
    for val in added[key]:
      dot_index = val.find('.')
      if dot_index != -1 and dot_index < len(val) - 1 and val[dot_index + 1].isupper() and val[dot_index + 1] != key:
        rhsList = []
        lhs = val[dot_index + 1]
        if lhs in G:
          for i in G[lhs]:
            rhsList.append('.' + i)
        newAdded[lhs] = rhsList
  if newAdded != {}:
    added = newAdded
    closureI.update(added)
    CLOSURE(closureI, G, added)
  return closureI

# Finding all possible GOTO functions
def Find_All_GOTO(I):
  XList = []
  for key in I:
    for val in I[key]:
      dot_index = val.find('.')
      if dot_index != -1 and dot_index < len(val) - 1:
        X = val[dot_index + 1]
        if X not in XList:
          XList.append(X)
  return XList

# GOTO Function
def GOTO(I, X, G):
  prodn = {}
  for key in I:
    prodnList = []
    for val in I[key]:
      dot_index = val.find('.')
      if dot_index != -1 and dot_index < len(val) - 1:
        x = val[dot_index + 1]
        if x == X:
          prod = val[:dot_index] + X + '.' + val[dot_index + 2:]
          prodnList.append(prod)
      if prodnList != []:
        prodn[key] = prodnList
  return CLOSURE(prodn, G, prodn)  

# Filling the shift actions in the action table and goto table entries
def Fill_ShiftAction_Goto(I, C, G, actionList, gotoList):
  indIi = C.index(I)
  for key in I:
    for val in I[key]:
      dot_index = val.find('.')
      if dot_index != -1 and dot_index < len(val) - 1:
        X = val[dot_index + 1]
        goto = GOTO(I, X, G)
        for J in C:
          if goto == J:
            indIj = C.index(J)
        if X.isupper():
          entry = [indIi, X, indIj]
          gotoList.append(entry)
        else:
          entry = [indIi, X, 'shift ' + str(indIj)]
          actionList.append(entry)

# Finding all the states of the parser
def Items(G):
  C = []
  closure = {}
  closure['S'] = G['S']
  added = closure
  closure = CLOSURE(closure, G, added)
  C.append(closure)
  for I in C:
    XList = Find_All_GOTO(I)
    for X in XList:
      newI = GOTO(I, X, G)
      if newI not in C and newI != {}:
        C.append(newI)
  return C

# FIRST Function
def FIRST(X, G):
  first = set()
  if not X.isupper():
    first.add(X)
  else:
    for val in G[X]:
      if val == '\u03B5':
        first.add('\u03B5')
      elif val[0] != X:
        firstY1 = FIRST(val[0], G)
        first.update(firstY1)  
        if '\u03B5' in firstY1 and val[:-1] != val[0]:
          first.add(FIRST(val[1]), G)
          for i in range(1, len(val)):
            if val[:-1] != val[i-1]:
              if '\u03B5' in FIRST(val[i], G):
                continue
              else:
                break
          if i == len(val)-1:
            first.add('\u03B5')
  return first

# FOLLOW Function
def FOLLOW(B, G):
  follow = set()
  if B == 'S':
    follow.add('$')
  for key in G:
    for val in G[key]:
      if B in val:
        idx = val.index(B)
        if val[-1] == B and key != B:
          follow.update(FOLLOW(key, G))
        elif idx+1 < len(val):
          firstBeta = FIRST(val[idx+1], G)
          follow.update(firstBeta)
          if '\u03B5' in firstBeta and key != B:
            follow.update(FOLLOW(key, G))
  return follow     

# Updating the action list
def Update_Action_List(C, actionList, G, S):
  for i in range(len(C)):
    for key in C[i]:
      for val in C[i][key]:
        dot_index = val.find('.')
        if dot_index != -1 and dot_index == len(val) - 1:
          for b in FOLLOW(key, G):
            if val[:-1] == S:
              entry = [i, '$', 'accept']
              actionList.append(entry)
            else:
              entry = [i, b, 'reduce ' + key + ' -> ' + val[:-1]]
              actionList.append(entry)
    
# Filling the action table
def Fill_Action_Table(actionList, C, T):
  actionTable = [['error' for _ in T] for _ in C]
  for entry in actionList:
      a, b, c = entry
      if a < len(C) and b in T:
          row_index = a
          col_index = T.index(b)
          actionTable[row_index][col_index] = c
  return actionTable

# Filling the goto table
def Fill_Goto_Table(actionList, C, NT):
  gotoTable = [['error' for _ in NT] for _ in C]
  for entry in actionList:
      a, b, c = entry
      if a < len(C) and b in NT:
          row_index = a
          col_index = NT.index(b)
          gotoTable[row_index][col_index] = c
  return gotoTable

# def Parse(ip, data, actionList, gotoList):
#   stack = '0'
#   prev = ''
#   for j in range(len(ip)):
#     for entry in actionList:
#       a, b, c = entry
#       if a == stack[:-1] and b == ip[j]:
#         data.append([a, c, data[j:]])
#         prev = c
#         break
#       else:
#         return False

# Terminals => Small alphabets & characters , Non-terminals => Capital alphabets
# id => i , epsilon => \u03B5 (unicode)

# Defining the augmented grammar
augGrammar = {
    'S': ['.E'],
    'E': ['E+T', 'T'],
    'T': ['T*F', 'F'],
    'F': ['i']
}

grammar = {
    'S': ['E'],
    'E': ['E+T', 'T'],
    'T': ['T*F', 'F'],
    'F': ['i']
}

T = set()
NT = list(augGrammar)

for key in augGrammar:
  for val in augGrammar[key]:
    for X in val:
      if X not in NT and X != '.':
        T.add(X)

T = list(T)
T.append('$')
actionList = []
gotoList = []
firstList = []
followList = []
C = Items(augGrammar)

# Printing the sets of terminals, non terminals and the grammar
print('\nTerminals: ', T)
print('Non terminals: ', NT)
print('Grammar: ', grammar)

# Printing all the states of the parser
print('\nStates of the Parser:-') 
for i in range(len(C)):
  print('I', i, ': ', C[i], sep = '')

# Printing the FIRST-FOLLOW Table
print('\nFIRST - FOLLOW Table:-')
for B in NT:
  firstList.append(FIRST(B, grammar))
  followList.append(FOLLOW(B, grammar))
FirstFollowList = []
for i, B in enumerate(NT):
    FirstFollowList.append([B, firstList[i], followList[i]])
headers = ['Non-Terminal', 'FIRST', 'FOLLOW']
print(tabulate(FirstFollowList, headers=headers, tablefmt='grid'))

for I in C:
  Fill_ShiftAction_Goto(I, C, grammar, actionList, gotoList)
Update_Action_List(C, actionList, augGrammar, 'E')

actionTable = Fill_Action_Table(actionList, C, T)
gotoTable = Fill_Goto_Table(gotoList, C, NT)

# Display the table using tabulate
print('\nACTION Table:-')
print(tabulate(actionTable, headers=T, showindex=list(range(len(C))), tablefmt='grid'))
print('\nGOTO table:-')
print(tabulate(gotoTable, headers=NT, showindex=list(range(len(C))), tablefmt='grid'))