class AddressNode:
	def __init__(self, p, succ):
		self.principal = p
		self.successors = succ
	
class AddressDAG:
	def __init__(self, root, principal_map):
		self.root = root
		self.principal_map = principal_map
	
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
	return count;

def DAG_to_string(dag):
	node_dict = {}
	final_count = build_node_list(dag.root, node_dict, -1)
	line_dict = {}
	for node, index in node_dict.items():
		successors = ''.join(['%i ' % node_dict[succ] for succ in node.successors])
		line_dict[index] = ('%s %s- ' % (node.principal, successors))
	res = line_dict[-1]
	for index in range(0,final_count):
		res = res + '\n' + line_dict[index]
	return res

# examples
dag_str = "DAG 0 1 - \n AD 2 - \n IP 2 - \n HID 3 - \n CID"
dag=parse_DAG(dag_str)
print(dag_str)
print
print(DAG_to_string(dag))

print

dag2_str = "DAG 2 0 - \n AD1 2 1 - \n HID1 2 - \n SID1 5 3 - \n AD2 5 4 - \n HID2 5 - \n SID2"
dag2 = parse_DAG(dag2_str)
print dag2_str
print
print(DAG_to_string(dag2))
