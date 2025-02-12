"""
temporary script used to find node corresponding to negamax value
hardcode for loop layers according to depth
"""

def temp1(cur_node,e):
    for d1 in cur_node.children:
        if d1.turn*(1-2*d1.risk)==e:
            return d1

def temp2(cur_node,e):
    for d1 in cur_node.children:
        if d1.turn*(1-2*d1.risk)==e:
            return d1
        for d2 in d1.children:
            if d2.turn*(1-2*d2.risk)==e:
                return d2