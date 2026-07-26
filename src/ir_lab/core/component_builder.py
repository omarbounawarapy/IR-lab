class ComponentBuilder:

    @staticmethod
    def build(configs, registry):
        components = []

        for config in configs:
            cls = registry[config["type"]]

            kwargs = {
                k: v
                for k, v in config.items()
                if k != "type"
            }

            components.append(cls(**kwargs))

        return components