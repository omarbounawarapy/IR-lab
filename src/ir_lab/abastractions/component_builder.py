from ir_lab.errors import ConfigError


class ComponentBuilder:

    @staticmethod
    def build(configs, registry):
        components = []

        for config in configs:
            try:
                component_type = config["type"]
            except KeyError:
                raise ConfigError(f"component config is missing a 'type' field: {config!r}")

            try:
                cls = registry[component_type]
            except KeyError:
                raise ConfigError(
                    f"unknown component type {component_type!r}; "
                    f"expected one of {sorted(registry)}"
                )

            kwargs = {
                k: v
                for k, v in config.items()
                if k != "type"
            }

            try:
                components.append(cls(**kwargs))
            except TypeError as e:
                raise ConfigError(f"invalid config for component {component_type!r}: {e}")

        return components
