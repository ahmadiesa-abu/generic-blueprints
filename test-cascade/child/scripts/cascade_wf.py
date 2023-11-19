from cloudify.workflows import ctx

graph = ctx.graph_mode()
sequence = graph.sequence()

for instance in ctx.node_instances:
    sequence.add(
        instance.execute_operation(
            'test.whatever'))

graph.execute()