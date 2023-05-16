class Node:
    def __init__(self, question, yes_node=None, no_node=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node

    def is_leaf(self):
        return self.yes_node is None and self.no_node is None


class BotConversation:
    def __init__(self):
        self.root = Node("Avez-vous une question spécifique ?",
                         yes_node=Node("Quelle est votre question ?", yes_node=Node("Réponse à votre question")),
                         no_node=Node("Quel sujet vous intéresse ?", yes_node=Node("Réponse au sujet 1"), no_node=Node("Réponse au sujet 2")))

        self.current_node = self.root

    def reset(self):
        self.current_node = self.root

    def speak_about(self, topic):
        def traverse(node):
            if node is None:
                return False
            elif node.question.lower() == topic.lower():
                return True
            else:
                return traverse(node.yes_node) or traverse(node.no_node)

        return traverse(self.root)

    def get_next_question(self):
        if self.current_node.is_leaf():
            return None
        return self.current_node.question

    def process_answer(self, answer):
        if answer.lower() == "yes":
            self.current_node = self.current_node.yes_node
        elif answer.lower() == "no":
            self.current_node = self.current_node.no_node
