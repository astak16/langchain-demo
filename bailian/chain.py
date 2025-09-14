class Chainable:
    def __or__(self, other):
        return Chain([self, other])

    def process(self, data):
        raise NotImplementedError("子类必须实现 process 方法")

    def __call__(self, data):
        return self.process(data)


class Chain(Chainable):
    def __init__(self, steps):
        self.steps = steps

    def process(self, data):
        result = data
        for step in self.steps:
            result = step.process(result)
        return result

    def __or__(self, other):
        return Chain(self.steps + [other])


class AddNumber(Chainable):
    def __init__(self, number):
        self.number = number

    def process(self, data):
        return data + self.number


class MultiplyNumber(Chainable):
    def __init__(self, number):
        self.number = number

    def process(self, data):
        return data * self.number


# 可以这样链式调用
chain = AddNumber(5) | MultiplyNumber(2) | MultiplyNumber(2)

# # 等价于传统的嵌套调用
result = MultiplyNumber(2).process(
    MultiplyNumber(2).process((AddNumber(5).process(10)))
)

print("链式调用结果:", chain(10))
print("传统调用结果:", result)
