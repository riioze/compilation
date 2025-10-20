from optimizer import *

NF = {
    # Operateurs binaires
    "nd_or" : {"prefix" : "","suffix" : "or"},
    "nd_and" : {"prefix" : "","suffix" : "and"},
    "nd_iseq" : {"prefix" : "","suffix" : "cmpeq"},
    "nd_isnoteq" : {"prefix" : "","suffix" : "cmpne"},
    "nd_isinfeq" : {"prefix" : "","suffix" : "cmple"},
    "nd_issupeq" : {"prefix" : "","suffix" : "cmpge"},
    "nd_isinf" : {"prefix" : "","suffix" : "cmplt"},
    "nd_issup" : {"prefix" : "","suffix" : "cmpgt"},
    "nd_plus" : {"prefix" : "","suffix" : "add"},
    "nd_minus" : {"prefix" : "","suffix" : "sub"},
    "nd_mult" : {"prefix" : "","suffix" : "mul"},
    "nd_div" : {"prefix" : "","suffix" : "div"},
    "nd_mod" : {"prefix" : "","suffix" : "mod"},

    # Operateurs unaires
    "nd_not" : {"prefix" : "", "suffix" : "not"},
    "nd_neg" : {"prefix" : "push 0", "suffix" : "sub"},

    # Instructions
    "nd_debug" : {"prefix" : "", "suffix" : "dbg"},
    "nd_drop" : {"prefix" : "", "suffix" : "drop 1"},
    "nd_block" : {"prefix" : "", "suffix" : ""},
    "nd_seq" : {"prefix" : "", "suffix" : ""},
    "nd_return" : {"prefix": "", "suffix":"ret"},
    "nd_ind" : {"prefix":"", "suffix":"read"},

    "nd_recv" : {"prefix":"","suffix":"recv"},
    "nd_send" : {"prefix":"","suffix":"send"},
}


global n_label,l_label
n_label = 0
l_label = 0

def gencode(optimizer:Optimizer,file):
    
    tree = optimizer.next_tree()
    gennode(tree,file)

def gennode(node:Node,file):

    global n_label,l_label

    node_type = node.node_type
    if node_type in NF:
        prefix = NF[node_type]["prefix"]
        if prefix: print(prefix, file=file)
        for child in node.children:
            gennode(child,file=file)
        print(NF[node_type]["suffix"],file=file)
        return

    match node.node_type:
        case "nd_const":
            print(f"push {node.node_value}",file=file)
        
        case "nd_ref":
            assert node.index != -1, "Index not set"
            print(f"get {node.index}",file=file)
        
        case "nd_decl":
            pass

        case "nd_affect":
            gennode(node.children[1],file)
            print("dup",file=file)
            identifier = node.children[0]
            if identifier.node_type == "nd_ind":
                gennode(identifier.children[0],file=file)
                print("write",file=file)
            else:
                assert identifier.index >= 0, f"index not set {str(identifier)}"
                print(f"set {identifier.index}",file=file)
        
        case "nd_cond":
            gennode(node.children[0],file=file)
            n_label+=1
            label = n_label
            print(f"jumpf l{label}a",file=file)
            gennode(node.children[1],file=file)
            print(f"jump l{label}b",file=file)
            print(f".l{label}a",file=file)
            if len(node.children) == 3:
                gennode(node.children[2],file=file)
            print(f".l{label}b",file=file)

        case "nd_loop":
            tmp = l_label
            n_label+=1
            l_label = n_label
            print(f".l{l_label}a",file=file)
            for child in node.children: gennode(child,file=file)
            print(f"jump l{l_label}a",file=file)
            print(f".l{l_label}b",file=file)
            l_label = tmp

        case "nd_break":
            print(f"jump l{l_label}b",file=file)
        
        case "nd_continue":
            print(f"jump l{l_label}c",file=file)
        
        case "nd_target":
            print(f".l{l_label}c",file=file)

        case "nd_func":
        
            print(f".{node.node_string}",file=file)
            print(f"resn {node.node_value}",file=file)

            instruction = node.children[-1]
            gennode(instruction,file=file)

            print("push 0",file=file)
            print("ret",file=file)
        
        case "nd_call":

            print(f"prep {node.children[0].node_string}",file=file)
            for child in node.children[1:]:
                gennode(child,file=file)
            print(f"call {len(node.children)-1}",file=file)

        case "nd_adr":
            print("prep start",file=file)
            print("swap",file=file)
            print("drop 1",file=file)
            print("push 1",file=file)
            print("sub",file=file)
            print(f"push {node.children[0].index}",file=file)
            print("sub",file=file)


        
        case other:
            raise ValueError(f"node_type {other} at pos {node.node_pos} unknown")
