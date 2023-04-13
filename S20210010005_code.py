grammar = {}
grammarSize = int(
    input("Please enter the number of productions in your Grammar: "))

for i in range(grammarSize):
    prodRule = input(
        f"Please enter your {i+1} Production Rule in Format(i.e S->A/BC/epsilon/b): ")
    var, rules = prodRule.split("->")
    splitedRules = rules.split("/")
    rulesSet = set(splitedRules)
    grammar.update({var: rulesSet})


terminals = set()
variables = set()
nullables = set()
lhsVariables = set()
ReachableStates = set()
generatingSymbols = set()
states = set()
nonGenerating = set()
nonReachable = set()
notUsedVariables = set()
queue = []


def findTerminalsAndVariables(grammar):
    for i in grammar.values():
        for j in i:
            for k in j:
                if(k.islower() and j != 'epsilon'):
                    terminals.add(k)
                if(k.isupper()):
                    variables.add(k)

    for i in grammar.keys():
        if(i.isupper()):
            variables.add(i)
            lhsVariables.add(i)


def removeEpsilonProdRule2(grammar, nullables):
    while(queue):
        queue.pop()
        for y in grammar:
            for j in grammar[y]:
                checkSubSet = set()
                for k in j:
                    checkSubSet.add(k)
                find = True
                for k in j:
                    if k not in nullables:
                        find = False
                        break
                if find == True:
                    if y not in nullables:
                        queue.append(y)
                    nullables.add(y)


def removeEpsilonProdRule1(grammar):
    for y in grammar:
        for j in grammar[y]:
            if(j == 'epsilon'):
                queue.append(y)
                nullables.add(y)
    removeEpsilonProdRule2(grammar, nullables)


def removeEpsilonProdRule4(j, y, grammar):
    if(len(j) == 0):
        return
    else:
        for k in range(len(j)):
            if j[k] in nullables:
                if len(j[:k]+j[k+1:]):
                    grammar[y].add(j[:k]+j[k+1:])
                    removeEpsilonProdRule4(j[:k]+j[k+1:], y, grammar)


def removeEpsilonProdRule3(grammar):
    for y in grammar:
        for j in grammar[y].copy():
            removeEpsilonProdRule4(j, y, grammar)


def removeEpsilonProdRule5(grammar):
    for i in grammar.values():
        i.discard("epsilon")


def removeUnitProduction(grammar):
    check = True
    while (check == True):
        check = False
        for y in grammar:
            for j in grammar[y]:
                if j in lhsVariables:
                    if len(j) == 1 and j.isupper():
                        check = True
                        grammar[y] = grammar[j] | grammar[y]
                        grammar[y].discard(j)


def removeNonReachable1(grammar, ReachableStates, states):
    if states in terminals:
        ReachableStates.add(states)
        return
    if states in ReachableStates:
        return
    ReachableStates.add(states)
    for y in grammar[states]:
        for k in y:
            removeNonReachable1(grammar, ReachableStates, k)


def removeNonGeneratingSymbols2(grammar, generatingSymbols):
    while(queue):
        queue.pop()
        for y in grammar:
            for j in grammar[y]:
                checkSubset = set()
                for k in j:
                    checkSubset.add(k)
                if checkSubset.issubset(generatingSymbols):
                    if y not in generatingSymbols:
                        queue.append(y)
                    generatingSymbols.add(y)


def removeNonGeneratingSymbols1(grammar, generatingSymbols):
    for y in grammar:
        for j in grammar[y]:
            if j in terminals or j == 'epsilon':
                queue.append(y)
                generatingSymbols.add(y)
    removeNonGeneratingSymbols2(grammar, generatingSymbols)


def removeNonGeneratingSymbols3(grammar, nonGenerating):
    removeNonGenerating = []
    for y in grammar:
        for j in grammar[y].copy():
            for k in j:
                if k in nonGenerating:
                    grammar[y].discard(j)
    for y in grammar:
        if y in nonGenerating:
            removeNonGenerating.append(y)
    for i in removeNonGenerating:
        del grammar[i]


def removeNonReachable2(grammar, nonReachable):
    removeNonReachable = []
    for y in grammar:
        for j in grammar[y].copy():
            for k in j:
                if k in nonReachable:
                    grammar[y].discard(j)
    for y in grammar:
        if y in nonReachable:
            removeNonReachable.append(y)
    for i in removeNonReachable:
        del grammar[i]


def convertCFGToCNF(grammar):
    check = True
    addedVariables = []
    while(check):
        check = False
        for y in grammar:
            for j in grammar[y]:
                if(len(j) >= 3):
                    check = True
                    update = j[0]+notUsedVariables[0]
                    addedVariables.append([notUsedVariables[0], j[1:]])
                    grammar[y].add(update)
                    notUsedVariables.pop(0)
                    grammar[y].discard(j)
    for i in addedVariables:
        temp = set()
        temp.add(i[1])
        grammar.update({i[0]: temp})
    check = True
    addNewVariables = []
    while (check):
        check = False
        for y in grammar:
            for j in grammar[y]:
                if len(j) > 1:
                    if(j[0] == j[1] and j[1].islower() and j[0].islower()):
                        check = True
                        update = notUsedVariables[0]+notUsedVariables[0]
                        grammar[y].add(update)
                        grammar[y].discard(j)
                        addNewVariables.append([notUsedVariables[0], j[0]])
                        notUsedVariables.pop(0)
                    if(j[0].isupper() and j[1].islower()):
                        check = True
                        update = j[0]+notUsedVariables[0]
                        grammar[y].add(update)
                        grammar[y].discard(j)
                        addNewVariables.append([notUsedVariables[0], j[1]])
                        notUsedVariables.pop(0)
                    if(j[0].islower() and j[1].isupper()):
                        check = True
                        update = notUsedVariables[0]+j[1]
                        grammar[y].add(update)
                        grammar[y].discard(j)
                        addNewVariables.append([notUsedVariables[0], j[0]])
                        notUsedVariables.pop(0)
    for i in addNewVariables:
        temp = set()
        temp.add(i[1])
        grammar.update({i[0]: temp})


def cyk(grammar, string):
    n = len(string)
    table = [[set() for _ in range(n-i)] for i in range(n)]
    for i in range(n):
        for y in grammar:
            if string[i] in grammar[y]:
                table[i][0].add(y)
    for j in range(1, n):
        for i in range(n - j):
            for k in range(j):
                for y in grammar:
                    for r in grammar[y]:
                        if len(r) == 2 and r[0] in table[i][k] and r[1] in table[i+k+1][j-k-1]:
                            table[i][j].add(y)
    print(table)

    if "S" in table[0][n-1]:
        return True
    else:
        return False


# Finding Terminal and Variable
findTerminalsAndVariables(grammar)

# Removing Epsilon Production
removeEpsilonProdRule1(grammar)
removeEpsilonProdRule3(grammar)
removeEpsilonProdRule5(grammar)

# Removing Unit Production
removeUnitProduction(grammar)

# Removing Generating Symbols
generatingSymbols = generatingSymbols | terminals
generatingSymbols.add("S")
removeNonGeneratingSymbols1(grammar, generatingSymbols)
states = variables | terminals
nonGenerating = states - generatingSymbols
removeNonGeneratingSymbols3(grammar, nonGenerating)

# Removing Non Reachable Symbols
removeNonReachable1(grammar, ReachableStates, 'S')
states = variables | terminals
nonReachable = states - ReachableStates
removeNonReachable2(grammar, nonReachable)

# Converting From CFG to CNF Form
notUsedVariables = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']) - variables
notUsedVariables = list(notUsedVariables)
convertCFGToCNF(grammar)

print("Nullables: ", nullables)
print("Terminals: ", terminals)
print("Variables: ", variables)
print("Non Generating Symbols: ", nonGenerating)
print("Non Reachable: ", nonReachable)

formattedGrammar = {}
for lhsTerminals, prodRules in grammar.items():
    productions_list = list(prodRules)
    productions_str = "/".join(productions_list)
    formattedGrammar[lhsTerminals] = productions_str

# Print the new formatted grammar
print("After converting CFG to CNF we get the following grammar: ")
for lhsTerminals, prodRules in formattedGrammar.items():
    print(f"{lhsTerminals} -> {prodRules}")


# Checking for the String if it is in the Grammar using CYK Algorithm
inputString = input(
    "Please Enter the string to check if it is the language of the grammar provided by you: ")
if cyk(grammar, inputString):
    print('True, The input string can be generated by the given grammar')
else:
    print('False, The input string cannot be generated by the given grammar')
