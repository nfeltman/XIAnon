class AddressNode:
	def __init__(self, p, succ):
		self.principal = p
		self.successors = succ
	
class AddressDAG:
	def __init__(self, root, principal_map):
		self.root = root
		self.principal_map = principal_map

def get_last_node(dag):
	node = dag.root
	while len(node.successors) > 0:
		node = node.successors[0]
	return node

def get_last_princ(dag):
	return get_last_node(dag).principal
	
def parse_DAG(str):
	nodes = {}
	count=-1;
	for line in str.splitlines():
		tokens = line.strip().split(" ")
		princ = tokens.pop(0)
		succ = []
		for token in tokens:
			if(token != '-'):
				succ.append(int(token))
		nodes[count] = AddressNode(princ,succ)
		count = count + 1
	principal_map = {}
	for node in nodes.values():
		node.successors = [nodes[i] for i in node.successors]
		principal_map[node.principal] = node
	return AddressDAG(nodes[-1],principal_map)

# internal function, not sure how to do that
def build_node_list(node, node_list, count):
	if not (node in node_list):
		node_list[node] = count;
		count = count + 1;
		for sub_node in node.successors:
			count = build_node_list(sub_node, node_list, count)
	return count

def DAG_root_to_string(dag_root):
	node_dict = {}
	final_count = build_node_list(dag_root, node_dict, -1)
	line_dict = {}
	for node, index in node_dict.items():
		successors = ''.join(['%i ' % node_dict[succ] for succ in node.successors])
		line_dict[index] = ('%s %s- ' % (node.principal, successors))
	res = line_dict[-1]
	for index in range(0,final_count):
		res = res + '\n' + line_dict[index]
	return res;

def DAG_to_string(dag):
		return DAG_root_to_string(dag.root)

def create_subDAG(dag, prin_name):
	to_str = DAG_root_to_string(dag.principal_map[prin_name])
	first_space = to_str.index(' ')
	return parse_DAG("DAG"+to_str[first_space:])

def append_dag(dag1, dag2):
	dag1_sink = get_last_node(dag1)
	dag1_sink.successors += dag2.root.successors
	dag1.principal_map = dict(dag1.principal_map.items() + dag2.principal_map.items())
	
# examples
##dag_str = "DAG 0 1 - \n AD 2 - \n IP 2 - \n HID 3 - \n CID"
##dag=parse_DAG(dag_str)
##print(dag_str)
##print()
##print(DAG_to_string(dag))
##
##print()
##
##dag2_str = "DAG 2 0 - \n AD1 2 1 - \n HID1 2 - \n SID1 5 3 - \n AD2 5 4 - \n HID2 5 - \n SID2"
##dag2 = parse_DAG(dag2_str)
##print(dag2_str)
##print()
##print(DAG_to_string(dag2))
##print()
##print(DAG_to_string(create_subDAG(dag2,'AD1')))
##print()
##print(get_last_princ(dag2))
