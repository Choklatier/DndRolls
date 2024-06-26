def read_rolls(file_path : str) -> dict:
    output = {}
    with open(file_path) as f: content = f.read()
    content = content.strip()
    for idx,elem in enumerate(content.split("#")[1:]):
        if idx % 2 == 0:
            session = elem
        else:
            output[session] = [int(x) for x in elem.split(",")]
    
    return output

if __name__ == "__main__":
    rolls = read_rolls("lucas.txt")
    print(rolls)