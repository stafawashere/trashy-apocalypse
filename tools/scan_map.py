from PIL import Image

CELL = 8
MIN_CLASS_FRACTION = 0.5
MIN_COMPONENT_CELLS = {"wall": 4, "crate": 4, "pipe": 6}

WALL_COLORS = {
    (157, 155, 141), (118, 117, 106), (191, 188, 169),
    (218, 214, 194), (85, 85, 76),
}
CRATE_COLORS = {
    (141, 92, 47), (173, 122, 68), (106, 67, 34), (61, 40, 20),
}
PIPE_COLORS = {
    (84, 91, 99), (124, 131, 139), (48, 53, 58), (214, 85, 58),
}


def near(color, palette, tolerance=14):
    r, g, b = color
    for pr, pg, pb in palette:
        if abs(r - pr) <= tolerance and abs(g - pg) <= tolerance and abs(b - pb) <= tolerance:
            return True
    return False


def classify_pixel(color):
    if near(color, WALL_COLORS):
        return "wall"
    if near(color, CRATE_COLORS):
        return "crate"
    if near(color, PIPE_COLORS):
        return "pipe"
    return None


def classify_cells(image):
    width, height = image.size
    pixels = image.load()
    cols = width // CELL
    rows = height // CELL
    grid = [[None] * cols for _ in range(rows)]
    cell_area = CELL * CELL

    for row in range(rows):
        for col in range(cols):
            counts = {"wall": 0, "crate": 0, "pipe": 0}
            for dy in range(CELL):
                for dx in range(CELL):
                    label = classify_pixel(pixels[col * CELL + dx, row * CELL + dy])
                    if label:
                        counts[label] += 1
            best_label = max(counts, key=counts.get)
            if counts[best_label] >= cell_area * MIN_CLASS_FRACTION:
                grid[row][col] = best_label
    drop_small_components(grid)
    return grid


def drop_small_components(grid):
    rows = len(grid)
    cols = len(grid[0])
    seen = [[False] * cols for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] is None or seen[row][col]:
                continue
            label = grid[row][col]
            component = []
            stack = [(row, col)]
            seen[row][col] = True
            while stack:
                r, c = stack.pop()
                component.append((r, c))
                for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and grid[nr][nc] == label:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            if len(component) < MIN_COMPONENT_CELLS[label]:
                for r, c in component:
                    grid[r][c] = None


def merge_rects(grid, label):
    rows = len(grid)
    cols = len(grid[0])
    used = [[False] * cols for _ in range(rows)]
    rects = []

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != label or used[row][col]:
                continue
            end_col = col
            while end_col + 1 < cols and grid[row][end_col + 1] == label and not used[row][end_col + 1]:
                end_col += 1
            end_row = row
            while end_row + 1 < rows and all(
                grid[end_row + 1][c] == label and not used[end_row + 1][c]
                for c in range(col, end_col + 1)
            ):
                end_row += 1
            for r in range(row, end_row + 1):
                for c in range(col, end_col + 1):
                    used[r][c] = True
            rects.append([
                col * CELL, row * CELL,
                (end_col - col + 1) * CELL, (end_row - row + 1) * CELL,
            ])
    return rects


def render_overlay(image, rect_groups, out_path):
    from PIL import ImageDraw
    overlay = image.convert("RGBA").copy()
    draw = ImageDraw.Draw(overlay, "RGBA")
    fills = {
        "wall": (255, 0, 0, 110),
        "crate": (255, 220, 0, 110),
        "pipe": (0, 120, 255, 110),
    }
    for label, rects in rect_groups.items():
        for left, top, width, height in rects:
            draw.rectangle(
                [left, top, left + width - 1, top + height - 1],
                fill=fills[label], outline=(255, 255, 255, 200),
            )
    overlay.save(out_path)


def format_rects(rects):
    lines = []
    for start in range(0, len(rects), 4):
        chunk = ", ".join(str(r) for r in rects[start:start + 4])
        lines.append(f"    {chunk},")
    return "\n".join(lines)


def main():
    image = Image.open("assets/background.png").convert("RGB")
    grid = classify_cells(image)
    groups = {label: merge_rects(grid, label) for label in ("wall", "crate", "pipe")}
    for label, rects in groups.items():
        print(f"{label}: {len(rects)} rects")
    render_overlay(image, groups, "tools/scan_overlay.png")
    with open("tools/scan_output.py", "w") as out:
        out.write("WALL_RECTS = [\n" + format_rects(groups["wall"]) + "\n]\n\n")
        out.write("CRATE_RECTS = [\n" + format_rects(groups["crate"]) + "\n]\n\n")
        out.write("PIPE_RECTS = [\n" + format_rects(groups["pipe"]) + "\n]\n")


if __name__ == "__main__":
    main()
