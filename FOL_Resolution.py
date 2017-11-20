import copy

def main():
    global current_query
    text_file = open("input.txt", "r")
    output_file = open('output.txt', 'w')
    queries = read_queries(text_file)
    kb = read_kb(text_file)
    working_kb = copy.deepcopy(kb)
    result = []
    for q in queries:
        current_query = negation_of(q)
        if FOL_resolution(current_query, working_kb):
            #print(q + "TRUE")
            s = "TRUE"
        else:
            #print(q + "FALSE")
            s = "FALSE"
        result.append(s)
    print(*result, sep = "\n")
    for i in result:
        output_file.write(i+"\n")


FAILURE = "failure"
dict_clauses= {}
resolved = []
def FOL_resolution(query, KB):
    matching_clause = []
    query_to_resolve = []
    if not query:
        return False

    sub_queries = query.split("|")
    for sub_query in sub_queries:
        matching_clause = find_matching_predicate(sub_query, KB)
        if matching_clause:
            query_to_resolve.append(sub_query)
            query_to_resolve.append(query)
            break;

    if not matching_clause:
        return False

    list_of_matched_clauses = []
    resolvent, theta = FOL_resolve(query_to_resolve, matching_clause)
    list_of_matched_clauses.append(matching_clause[1])
    if negation_of(query_to_resolve[0]) not in dict_clauses.keys():
        dict_clauses.update({negation_of(query_to_resolve[0]): list_of_matched_clauses})
    else:
        existing_list = dict_clauses.get(negation_of(query_to_resolve[0]))
        if matching_clause[1] not in existing_list:
            existing_list.append(matching_clause[1])
        dict_clauses[negation_of(query_to_resolve[0])] = existing_list

    if FAILURE in theta:
        if resolved:
            resolved.pop()
        if resolved and FOL_resolution(resolved.pop(), KB):
            return True
        elif not resolved and FOL_resolution(current_query, KB):
            return True
        else:
            return False

    if resolvent == '' and FAILURE not in theta:
        return True
    elif resolvent != '' and not KB:
        return False
    if resolvent not in KB:
        KB.append(resolvent)
        resolved.append(resolvent)
    return FOL_resolution(resolvent, KB)


def FOL_resolve(query, matching_clause):
    theta = {}
    literals = []
    clause_1 = []
    clause_2 = []

    if not query[1] and not matching_clause[1]:
        return '', []
    unify(negation_of(query[0]), matching_clause[0], theta)
    if FAILURE in theta:
        return '', theta
    if query[1]:
        clause_1 = query[1].split("|")
        clause_1.remove(query[0])
    if matching_clause[1]:
        clause_2 = matching_clause[1].split("|")
        clause_2.remove(matching_clause[0])
    for literal in clause_1:
        literals.append(substitute(literal, theta))
    for literal in clause_2:
        substituted = substitute(literal, theta)
        if substituted not in literals:
            literals.append(substituted)
    resolvent = "|".join(literals)

    return resolvent, theta


def find_matching_predicate(query, KB):
    matched_clause = []
    to_search = negation_of(query)
    for sentence in KB:
        literals = sentence.split("|")
        for literal in literals:
            if to_search == literal or ((get_predicate(literal) == get_predicate(to_search)) and (len(get_args(to_search).split(",")) == len(get_args(literal).split(",")))):
                if not (dict_clauses and to_search in dict_clauses and sentence in dict_clauses.get(to_search)) and not (dict_clauses and sentence in dict_clauses and to_search in dict_clauses.get(literal)):
                    matched_clause.append(literal)
                    matched_clause.append(sentence)
                    return matched_clause

    return matched_clause


def unify(x, y, theta):
    if theta:
        if FAILURE in theta:
            return theta
    if x == y:
        return theta
    if is_variable(x):
        unify_var(x, y, theta)
    elif is_variable(y):
        unify_var(y, x, theta)
    elif is_compound(x) and is_compound(y):
        unify(get_predicate(x), get_predicate(y), theta)
        return unify(get_args(x), get_args(y), theta)
    elif is_list(x) and is_list(y):
        first_a, rest_a = split_list(x)
        first_b, rest_b = split_list(y)
        unify(first_a, first_b, theta)
        return unify(rest_a, rest_b, theta)
    else:
        theta[FAILURE] = FAILURE
        return theta


def unify_var(var, x, theta):
    if var in theta.keys():
        return unify(theta[var], x, theta)
    elif occur_check(var, x, theta):
        theta[FAILURE] = FAILURE
    else:
        x = substitute(x, theta)
        theta[var] =  x


def occur_check(var, x, s):
    if var == x:
        return True
    elif is_variable(x) and x in s:
        return occur_check(var, s[x], s)
    elif is_compound(x):
        return (occur_check(var, get_predicate(x), s) or
                occur_check(var, get_args(x), s))
    else:
        return False


def is_compound(x):
    if "(" in x:
        return True
    else:
        return False


def get_args(a):
    if is_compound(a):
        return a[a.find("(")+1:len(a)-1]


def get_predicate(a):
    return a[0:a.find("(")]


def is_list(x):
    if "," in x:
        return True


def split_list(x):
    if "(" in x[0:x.find(",")]:
        return x[0:x.find(")")+1], x[x.find(")")+2:len(x)]
    else:
        return x[0:x.find(",")], x[x.find(",")+1:len(x)]


def is_variable(x):
    if len(x) == 1 and x.islower() and not is_list(x) and not is_compound(x):
        return True
    elif x[0].islower() and not is_list(x) and not is_compound(x):
        return True
    else:
        return False


def negation_of(literal):
    if literal[0] == "~":
        return literal[1:]
    else:
        return "~" + literal


def is_fact(goal):
    for i in get_args(goal).split(","):
        if is_variable(i):
            return False
    return True


def get_variable(str_args):
    args = str_args.split(",")
    for arg in args:
        if not is_variable(arg):
            args.remove(arg)
    return args


def substitute(statement, subst):
    if is_compound(statement):
        for i in get_variable(get_args(statement)):
            if i in subst.keys():
                statement = replace_var_val(statement, i, subst[i])
    return statement


def replace_var_val(x, var, val):
    if is_compound(x):
        u_arg = []
        for arg in get_args(x).split(","):
            if is_variable(arg) and arg == var:
                u_arg.append(val)
            elif is_compound(arg):
                u_arg.append(replace_var_val(arg, var, val))
            else:
                u_arg.append(arg)
        x = get_predicate(x)+"("+",".join(u_arg)+")"
    return x


# Reading the input file
def read_queries(text_file):
    queries = []
    for i in range(int(text_file.readline())):
        queries.append(text_file.readline().strip())
    return queries


def read_kb(text_file):
    kb = []
    for i in range(int(text_file.readline())):
        st = text_file.readline().strip()
        st = st.replace(" ", "")
        clause = standardize(st, i)
        kb.append(clause)
    return kb


def standardize(clause, i):
    l = []
    literals = clause.split("|")
    for literal in literals:
        args = get_args(literal).split(",")
        arg = []
        for v in args:
            if is_variable(v):
                arg.append(v + str(i))
            else:
                arg.append(v)
        l.append(get_predicate(literal) + "("+",".join(arg)+")")
    std_clause = "|".join(l)
    return std_clause


main()
