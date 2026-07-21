

class BooleanRPNTransformer:
    def __init__(self):
        self.operators = {
            'AND': 1,
            'OR': 1,
            'NOT': 2
        }

    def transform(self,query: Query) -> BooleanRPNQuery:
        input = query.data
        holding_stack = []
        output_stack = []
        for token in input:
            if token not in self.operators:
                output_stack.append(token)
            else:
                while (holding_stack and holding_stack[-1] != '(' and
                       self.operators[holding_stack[-1]] >= self.operators[token]):
                    output_stack.append(holding_stack.pop())
                holding_stack.append(token)
        while holding_stack:
            output_stack.append(holding_stack.pop())

        return BooleanRPNQuery(output_stack)
    