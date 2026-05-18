from collections import deque

class AttackNode:
    def __init__(self, name, type="intermediate", difficulty="medium", cost=0):
        self.name = name
        self.type = type
        self.difficulty = difficulty
        self.cost = cost
        self.children = []
        self.parent = None

class AttackPath:
    def __init__(self, nodes=None):
        self.nodes = nodes or []
        self.feasibility_score = 0.8
        self.total_cost = sum(n.cost for n in self.nodes)
        self.estimated_time = "1_day"

class PathAnalysis:
    def __init__(self, paths):
        self.paths = paths

    def get_feasible_paths(self, threshold=0.5):
        return [p for p in self.paths if p.feasibility_score >= threshold]

class AttackTree:
    def __init__(self, root_node):
        self.root_node = root_node
        self.all_nodes = [root_node]
        self.leaf_nodes = []
        if root_node.type == "leaf":
            self.leaf_nodes.append(root_node)
        self.attack_paths = [[root_node]]

    def find_node(self, name):
        for node in self.all_nodes:
            if node.name == name:
                return node
        return None

    def update_attack_paths(self):
        paths = []
        if not self.root_node:
            self.attack_paths = paths
            return

        # Queue stores tuples of (current_node, path_to_node)
        queue = deque([(self.root_node, [self.root_node])])

        while queue:
            current_node, current_path = queue.popleft()

            if not current_node.children:
                # It's a leaf node
                paths.append(AttackPath(current_path))
            else:
                for child in current_node.children:
                    queue.append((child, current_path + [child]))

        self.attack_paths = paths

class ThreatScenario:
    def __init__(self, goal, attacker_profile, attack_vector, motivation=None):
        self.goal = goal
        self.attacker_profile = attacker_profile
        self.attack_vector = attack_vector
        self.motivation = motivation

class CriticalNode:
    def __init__(self, name):
        self.name = name
        self.importance_score = 0.9
        self.path_frequency = 0.5
        self.recommended_countermeasures = ["patch_system", "implement_encryption"]

class AttackTreesComponent:
    def construct_attack_tree(self, target_asset, threat_scenario):
        root = AttackNode(threat_scenario.goal, "root")
        tree = AttackTree(root)

        child1 = AttackNode("gain_physical_access", "intermediate", "hard", 1000)
        child2 = AttackNode("exploit_remote_vuln", "leaf", "medium", 500)

        child1.parent = root
        child2.parent = root
        root.children.extend([child1, child2])

        tree.all_nodes.extend([child1, child2])
        tree.leaf_nodes.append(child2)

        path1 = AttackPath([root, child1])
        path2 = AttackPath([root, child2])
        tree.attack_paths = [path1, path2]

        return tree

    def add_attack_node(self, tree, parent_node, node_data):
        node = AttackNode(node_data.get("name"), node_data.get("type", "leaf"), node_data.get("difficulty", "medium"), node_data.get("cost", 0))
        if parent_node:
            node.parent = parent_node
            parent_node.children.append(node)
        tree.all_nodes.append(node)
        if node.type == "leaf":
            tree.leaf_nodes.append(node)
        return node

    def analyze_attack_paths(self, tree, analysis_type):
        return PathAnalysis(tree.attack_paths)

    def identify_critical_nodes(self, tree, criteria):
        return [CriticalNode(tree.root_node.name)]
