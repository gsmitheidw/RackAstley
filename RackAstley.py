import pyperclip
import yaml

def render_device(name, size):
    size_str = f"{{{size}U}}"
    pad_left = 3
    pad_right = 1
    inner_width = 24
    size_pos = inner_width - len(size_str) - pad_right
    dash_fill = size_pos - pad_left - len(name)

    if dash_fill < 0:
        inner_width = pad_left + len(name) + dash_fill + len(size_str) + pad_right
        size_pos = inner_width - len(size_str) - pad_right
        dash_fill = 0

    top = (
        "┌"
        + "─" * pad_left
        + name
        + "─" * dash_fill
        + size_str
        + "─" * pad_right
        + "┐"
    )
    bottom = f"└{'─' * inner_width}┘"

    if size == 1:
        eq_count = (inner_width - len(name) - len(size_str)) // 2
        left_eq = eq_count
        right_eq = inner_width - len(name) - len(size_str) - left_eq
        line = (
            "〘"
            + "=" * left_eq
            + name
            + "=" * right_eq
            + size_str
            + "═"
            + "〙"
        )
        return line
    elif size == 2:
        return f"{top}\n{bottom}"
    else:
        middle_line = f"│{' ' * inner_width}│"
        body = "\n".join([middle_line] * (size - 2))
        return f"{top}\n{body}\n{bottom}"

def render_blank_rack(height, title):
    out = [f"[RACK {title}]"]
    for u in range(height, 0, -1):
        out.append(f"[{u:02d}]")
    return "\n".join(out)

def validate_rack(rack):
    height = rack['height']
    occupied = set()

    for dev in rack['devices']:
        name = dev['name']
        pos = dev['position']
        size = dev.get('size', 1)

        if pos < 1 or pos + size - 1 > height:
            raise ValueError(f"{name} does not fit in rack")

        for u in range(pos, pos + size):
            if u in occupied:
                raise ValueError(f"U{u} already occupied (conflict: {name})")
            occupied.add(u)

def render_rack_from_yaml(rack):
    height = rack['height']
    title = rack.get('name', 'Unnamed')
    lines = ["" for _ in range(height)]

    # Fill lines top-down
    fill = [''] * height
    for dev in rack['devices']:
        name = dev['name']
        pos = dev['position']
        size = dev.get('size', 1)
        rendered = render_device(name, size).splitlines()

        for i in range(size):
            line_index = height - (pos + size - 1) + i
            fill[line_index] = rendered[i] if i < len(rendered) else ""

    out = [f"[RACK {title}]"]
    for i in range(height):
        u = height - i
        line = fill[i] or ""
        out.append(f"[{u:02d}] {line}")
    return "\n".join(out)

def main():
    while True:
        print("\033[32mRackAstley:\n\033[0mNever gonna mislabel your gear.\n")
        print("🧱 1. Print single rack device")
        print("🏗  2. Print blank rack")
        print("📄 3. Load rack from YAML")
        print("✖  q. Quit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Device name: ").strip()
            size = int(input("Device size (U): ").strip())
            out = render_device(name, size)
            print("\n" + out)
            pyperclip.copy(out)
            print("\n[Copied to clipboard]")

        elif choice == "2":
            height = int(input("Rack height (U): ").strip())
            title = input("Rack title: ").strip()
            out = render_blank_rack(height, title)
            print("\n" + out)
            pyperclip.copy(out)
            print("\n[Copied to clipboard]")

        elif choice == "3":
            path = input("YAML file path: ").strip()
            try:
                with open(path, 'r') as f:
                    rack = yaml.safe_load(f)['rack']
                    validate_rack(rack)
                    out = render_rack_from_yaml(rack)
                    print("\n" + out)
                    pyperclip.copy(out)
                    print("\n[Copied to clipboard]")
            except Exception as e:
                print(f"\n❗ Error: {e}")

        elif choice in ("3", "q"):
            break
        else:
            print("❗Invalid choice. Try again.")

if __name__ == "__main__":
    main()

