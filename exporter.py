import json


def export_json(
    graph,
    path
):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            graph.to_dict(),
            f,
            indent=2
        )


def export_mermaid(
    graph,
    path
):

    lines = ["graph TD"]

    for source, targets in graph.edges.items():

        for target in targets:

            lines.append(
                f'"{source}" --> "{target}"'
            )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(lines)
        )