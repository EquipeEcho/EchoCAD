from pathlib import Path


TEXT_LAYER = "arq - textos"
WALL_LAYER = "arq - alvenaria alta"
OPENING_LAYER = "arq - esquadrias"


def br_number(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def pair(code: int, value: object) -> list[str]:
    return [str(code), str(value)]


def mtext_entity(x: float, y: float, text: str) -> list[str]:
    lines = ["0", "MTEXT"]
    lines += pair(8, TEXT_LAYER)
    lines += pair(10, x)
    lines += pair(20, y)
    lines += pair(30, 0)
    lines += pair(40, 0.25)
    lines += pair(1, text)
    return lines


def line_entity(layer: str, x1: float, y1: float, x2: float, y2: float) -> list[str]:
    lines = ["0", "LINE"]
    lines += pair(8, layer)
    lines += pair(10, x1)
    lines += pair(20, y1)
    lines += pair(30, 0)
    lines += pair(11, x2)
    lines += pair(21, y2)
    lines += pair(31, 0)
    return lines


def room_entities(room: dict) -> list[str]:
    x = room["x"]
    y = room["y"]
    width = room["width"]
    depth = room["depth"]
    area = width * depth
    perimeter = 2 * (width + depth)
    pd = room.get("pd", 3.0)

    text_lines = [room["name"]]
    if room.get("subtitle"):
        text_lines.append(f"({room['subtitle']})")
    text_lines.extend(
        [
            f"{br_number(area)} m\xb2",
            f"P = {br_number(perimeter)} m",
            f"PD = {br_number(pd)} m",
        ]
    )

    entities = mtext_entity(x + 0.35, y + depth - 0.55, "\\P".join(text_lines))

    # Room rectangle.
    entities += line_entity(WALL_LAYER, x, y, x + width, y)
    entities += line_entity(WALL_LAYER, x + width, y, x + width, y + depth)
    entities += line_entity(WALL_LAYER, x + width, y + depth, x, y + depth)
    entities += line_entity(WALL_LAYER, x, y + depth, x, y)

    for opening in room.get("openings", []):
        ox1, oy1, ox2, oy2 = opening
        entities += line_entity(OPENING_LAYER, x + ox1, y + oy1, x + ox2, y + oy2)

    return entities


def build_dxf(rooms: list[dict]) -> str:
    lines = [
        "0",
        "SECTION",
        "2",
        "HEADER",
        "9",
        "$ACADVER",
        "1",
        "AC1009",
        "0",
        "ENDSEC",
        "0",
        "SECTION",
        "2",
        "ENTITIES",
    ]

    for room in rooms:
        lines.extend(room_entities(room))

    lines.extend(["0", "ENDSEC", "0", "EOF"])
    return "\n".join(lines) + "\n"


SIMPLE_ROOMS = [
    {
        "name": "SALA ADMINISTRATIVA",
        "subtitle": "ADMINISTRATIVO",
        "x": 0.0,
        "y": 0.0,
        "width": 4.0,
        "depth": 3.0,
        "pd": 3.0,
        "openings": [(1.4, 0.0, 2.4, 0.0)],
    },
    {
        "name": "BANHEIRO",
        "subtitle": "SERVICO",
        "x": 5.0,
        "y": 0.0,
        "width": 2.0,
        "depth": 2.0,
        "pd": 2.8,
        "openings": [(0.6, 0.0, 1.4, 0.0)],
    },
    {
        "name": "COPA",
        "subtitle": "APOIO",
        "x": 0.0,
        "y": 4.0,
        "width": 3.0,
        "depth": 2.5,
        "pd": 3.0,
        "openings": [(1.0, 0.0, 1.9, 0.0)],
    },
]


COMPLETE_ROOMS = [
    {
        "name": "SALA DE REUNIAO",
        "subtitle": "ADMINISTRATIVO",
        "x": 0.0,
        "y": 0.0,
        "width": 5.0,
        "depth": 4.0,
        "pd": 3.1,
        "openings": [(2.0, 0.0, 3.0, 0.0), (5.0, 1.4, 5.0, 2.8)],
    },
    {
        "name": "ALOJAMENTO",
        "subtitle": "USO COLETIVO",
        "x": 6.0,
        "y": 0.0,
        "width": 6.0,
        "depth": 4.0,
        "pd": 3.0,
        "openings": [(2.2, 0.0, 3.2, 0.0), (6.0, 1.2, 6.0, 2.4)],
    },
    {
        "name": "BANHEIRO",
        "subtitle": "SERVICO",
        "x": 13.0,
        "y": 0.0,
        "width": 2.4,
        "depth": 2.2,
        "pd": 2.8,
        "openings": [(0.7, 0.0, 1.5, 0.0)],
    },
    {
        "name": "COPA",
        "subtitle": "APOIO",
        "x": 0.0,
        "y": 5.0,
        "width": 3.5,
        "depth": 3.0,
        "pd": 3.0,
        "openings": [(1.1, 0.0, 2.0, 0.0)],
    },
    {
        "name": "CIRCULACAO",
        "subtitle": "ACESSO",
        "x": 4.5,
        "y": 5.0,
        "width": 7.0,
        "depth": 1.8,
        "pd": 3.0,
        "openings": [(0.8, 0.0, 1.8, 0.0), (5.0, 1.8, 6.0, 1.8)],
    },
    {
        "name": "RESERVA TECNICA",
        "subtitle": "APOIO",
        "x": 12.5,
        "y": 4.0,
        "width": 3.0,
        "depth": 2.5,
        "pd": 3.0,
        "openings": [(1.0, 0.0, 1.8, 0.0)],
    },
]


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    files = {
        "exemplo_memorial_simples.dxf": SIMPLE_ROOMS,
        "exemplo_memorial_completo.dxf": COMPLETE_ROOMS,
    }

    for filename, rooms in files.items():
        path = output_dir / filename
        path.write_text(build_dxf(rooms), encoding="windows-1252")
        print(f"Gerado: {path}")


if __name__ == "__main__":
    main()
